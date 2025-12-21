"""
Enemy spawn zone detection

Identifies safe areas for different enemy types.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tile_constants import EMPTY, GROUND, WALL, PLATFORM_ONEWAY, SPIKE
import config


def detect_spawn_zones(room):
    """
    Detect all types of spawn zones in a room
    
    Returns:
        dict: Spawn zones by type
    """
    zones = {
        'ground': detect_ground_zones(room),
        'aerial': detect_aerial_zones(room),
        'wall': detect_wall_zones(room)
    }
    
    return zones


def detect_ground_zones(room):
    """
    Detect safe ground areas for walking enemies
    
    Looks for:
    - Flat ground sections with no spikes
    - Minimum 3 tiles wide
    - Not too close to edges or pits
    
    Returns:
        list: List of ground zone dicts with position and size
    """
    zones = []
    
    # Scan each horizontal level
    for y in range(room.height - 1):
        # Check if this row has ground below
        has_ground_below = False
        for x in range(room.width):
            tile_below = room.get_tile(x, y + 1)
            if tile_below in [GROUND, WALL, PLATFORM_ONEWAY]:
                has_ground_below = True
                break
        
        if not has_ground_below:
            continue
        
        # Scan for continuous safe sections
        safe_start = None
        for x in range(room.width + 1):
            # Check if current position is safe
            is_safe = False
            if x < room.width:
                tile_at = room.get_tile(x, y)
                tile_below = room.get_tile(x, y + 1)
                is_safe = (
                    tile_at == EMPTY and  # Empty space to stand in
                    tile_below in [GROUND, WALL, PLATFORM_ONEWAY] and  # Solid below
                    tile_below != SPIKE  # No spikes
                )
                
                # Check 3-tile headroom (Week 4)
                # Y=0 is TOP, so we check y-1, y-2 (going upward)
                if is_safe:
                    has_headroom = True
                    for dy in range(config.PLAYER_TOTAL_HEIGHT):
                        check_y = y - dy  # UPWARD from feet
                        if check_y < 0:
                            break  # Top of room is OK
                        tile_above = room.get_tile(x, check_y)
                        if tile_above in [GROUND, WALL, PLATFORM_ONEWAY]:
                            has_headroom = False
                            break
                    is_safe = is_safe and has_headroom
            
            if is_safe:
                if safe_start is None:
                    safe_start = x
            else:
                if safe_start is not None:
                    width = x - safe_start
                    # Only record zones at least 3 tiles wide
                    if width >= 3:
                        zones.append({
                            'x': safe_start,
                            'y': y,
                            'width': width,
                            'height': 1,
                            'type': 'ground',
                            'allowed_enemies': ['light_walker', 'medium_walker', 'heavy_walker']
                        })
                    safe_start = None
    
    return zones


def detect_aerial_zones(room):
    """
    Detect open air spaces for flying enemies
    
    Looks for:
    - Large empty vertical spaces
    - Not blocked by platforms
    - Minimum 4x4 area
    
    Returns:
        list: List of aerial zone dicts
    """
    zones = []
    
    # Find large empty rectangles
    # Simple approach: scan for 4x4 empty blocks
    min_size = 4
    
    for y in range(0, room.height - min_size + 1, 2):  # Step by 2 to avoid overlap
        for x in range(0, room.width - min_size + 1, 2):
            # Check if this area is mostly empty
            empty_count = 0
            total_tiles = min_size * min_size
            
            for dy in range(min_size):
                for dx in range(min_size):
                    tile = room.get_tile(x + dx, y + dy)
                    if tile == EMPTY:
                        empty_count += 1
            
            # If 75%+ empty, it's a good aerial zone
            if empty_count / total_tiles >= 0.75:
                zones.append({
                    'x': x,
                    'y': y,
                    'width': min_size,
                    'height': min_size,
                    'type': 'aerial',
                    'allowed_enemies': ['light_flyer', 'medium_flyer']
                })
    
    return zones


def detect_wall_zones(room):
    """
    Detect wall surfaces for wall-crawling enemies
    
    Looks for:
    - Vertical wall sections
    - Minimum 3 tiles high
    - Adjacent to empty space
    
    Returns:
        list: List of wall zone dicts
    """
    zones = []
    
    # Scan vertical walls
    for x in range(room.width):
        wall_start = None
        
        for y in range(room.height + 1):
            # Check if current position is wall
            is_wall = False
            if y < room.height:
                tile = room.get_tile(x, y)
                is_wall = (tile == WALL)
                
                # Also check if there's empty space adjacent (wall-crawler needs room)
                if is_wall:
                    has_adjacent_empty = False
                    for dx in [-1, 1]:
                        nx = x + dx
                        if 0 <= nx < room.width:
                            if room.get_tile(nx, y) == EMPTY:
                                has_adjacent_empty = True
                    is_wall = is_wall and has_adjacent_empty
            
            if is_wall:
                if wall_start is None:
                    wall_start = y
            else:
                if wall_start is not None:
                    height = y - wall_start
                    # Only record walls at least 3 tiles high
                    if height >= 3:
                        zones.append({
                            'x': x,
                            'y': wall_start,
                            'width': 1,
                            'height': height,
                            'type': 'wall',
                            'allowed_enemies': ['wall_crawler']
                        })
                    wall_start = None
    
    return zones


def assign_spawn_zones_to_room(room):
    """
    Detect spawn zones and assign them to room template
    
    Updates room.spawn_zones in place
    
    Args:
        room: RoomTemplate to update
    """
    zones = detect_spawn_zones(room)
    
    # Clear existing spawn zones
    room.spawn_zones['enemies'] = []
    
    # Add ground zones
    for i, zone in enumerate(zones['ground']):
        room.spawn_zones['enemies'].append({
            'id': f'ground_{i}',
            'position': {'x': zone['x'] + zone['width'] // 2, 'y': zone['y']},
            'type': 'ground',
            'size': {'width': zone['width'], 'height': zone['height']},
            'allowed_enemies': zone['allowed_enemies']
        })
    
    # Add aerial zones
    for i, zone in enumerate(zones['aerial']):
        room.spawn_zones['enemies'].append({
            'id': f'aerial_{i}',
            'position': {'x': zone['x'] + zone['width'] // 2, 'y': zone['y'] + zone['height'] // 2},
            'type': 'aerial',
            'size': {'width': zone['width'], 'height': zone['height']},
            'allowed_enemies': zone['allowed_enemies']
        })
    
    # Add wall zones
    for i, zone in enumerate(zones['wall']):
        room.spawn_zones['enemies'].append({
            'id': f'wall_{i}',
            'position': {'x': zone['x'], 'y': zone['y'] + zone['height'] // 2},
            'type': 'wall',
            'size': {'width': zone['width'], 'height': zone['height']},
            'allowed_enemies': zone['allowed_enemies']
        })
    
    return zones
