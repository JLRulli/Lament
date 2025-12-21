"""
Obstacle placement system with theme and density control

Places obstacles (moving platforms, disappearing platforms, hazards) based on themes.
"""
import random
from typing import Dict, List, Any
from utils.tile_constants import SPIKE, PLATFORM_ONEWAY, GROUND, WALL, EMPTY


# Obstacle type definitions
OBSTACLE_TYPES = {
    'spike': {
        'category': 'hazard',
        'threat_level': 3,
        'placement': 'ground',  # On ground tiles
        'tile_id': SPIKE
    },
    'moving_platform': {
        'category': 'platform',
        'threat_level': 2,
        'placement': 'air',  # Floating in air
        'properties': {
            'speed': 'medium',
            'pattern': 'horizontal'
        }
    },
    'disappearing_platform': {
        'category': 'platform',
        'threat_level': 2,
        'placement': 'air',
        'properties': {
            'on_time': 2.0,
            'off_time': 1.5
        }
    },
    'falling_stalactite': {
        'category': 'hazard',
        'threat_level': 4,
        'placement': 'ceiling',  # Hangs from ceiling
        'properties': {
            'fall_delay': 0.5,
            'respawn_time': 5.0
        }
    },
    'drill': {
        'category': 'hazard',
        'threat_level': 5,
        'placement': 'wall',  # Attached to walls
        'properties': {
            'extend_distance': 3,
            'cycle_time': 2.0
        }
    }
}

# Theme definitions
OBSTACLE_THEMES = {
    'platforming': {
        'moving_platform': 0.5,
        'disappearing_platform': 0.3,
        'spike': 0.2
    },
    'hazards': {
        'spike': 0.5,
        'falling_stalactite': 0.3,
        'drill': 0.2
    },
    'mixed': {
        'spike': 0.3,
        'moving_platform': 0.25,
        'disappearing_platform': 0.2,
        'falling_stalactite': 0.15,
        'drill': 0.1
    },
    'combat': {
        # Fewer obstacles, focus on platforms for maneuvering
        'moving_platform': 0.6,
        'spike': 0.4
    },
    'minimal': {
        # Very sparse obstacles
        'spike': 0.7,
        'moving_platform': 0.3
    }
}

# Density levels
DENSITY_LEVELS = {
    'sparse': 0.5,
    'normal': 1.0,
    'dense': 1.5,
    'extreme': 2.0
}


def calculate_obstacle_count(difficulty: int, room_width: int, room_height: int, density: str = 'normal') -> int:
    """
    Calculate how many obstacles to place
    
    Args:
        difficulty: Room difficulty (1-10)
        room_width: Room width in tiles
        room_height: Room height in tiles
        density: 'sparse', 'normal', 'dense', 'extreme'
    
    Returns:
        Number of obstacles to place
    """
    room_area = room_width * room_height
    
    # Base formula: More difficult rooms have more obstacles
    # Rough target: 1 obstacle per 40-60 tiles at difficulty 5
    base_density = difficulty / 200.0  # 0.05 at diff=10
    base_count = int(room_area * base_density)
    
    # Apply density multiplier
    multiplier = DENSITY_LEVELS.get(density, 1.0)
    final_count = int(base_count * multiplier)
    
    return max(1, min(final_count, room_area // 10))  # Cap at 1 per 10 tiles


def select_obstacle_by_theme(theme: str, allowed_types: List[str] = None) -> str:
    """
    Select an obstacle type based on theme
    
    Args:
        theme: Theme name ('platforming', 'hazards', etc.)
        allowed_types: List of allowed obstacle types (None = all)
    
    Returns:
        Obstacle type string
    """
    if theme not in OBSTACLE_THEMES:
        theme = 'mixed'
    
    weights = OBSTACLE_THEMES[theme]
    
    # Filter by allowed types
    if allowed_types:
        weights = {k: v for k, v in weights.items() if k in allowed_types}
    
    if not weights:
        return random.choice(list(OBSTACLE_TYPES.keys()))
    
    # Weighted random selection
    choices = []
    for obstacle_type, weight in weights.items():
        choices.extend([obstacle_type] * int(weight * 100))
    
    return random.choice(choices) if choices else list(weights.keys())[0]


def find_valid_obstacle_positions(room, obstacle_type: str, count: int) -> List[Dict[str, int]]:
    """
    Find valid positions to place obstacles
    
    Args:
        room: RoomTemplate object
        obstacle_type: Type of obstacle to place
        count: Number of positions needed
    
    Returns:
        List of position dicts {'x': int, 'y': int}
    """
    placement_type = OBSTACLE_TYPES[obstacle_type]['placement']
    positions = []
    
    if placement_type == 'ground':
        # Find ground tiles
        for y in range(room.height - 1, 0, -1):
            for x in range(1, room.width - 1):
                tile_below = room.get_tile(x, y)
                tile_at = room.get_tile(x, y - 1)
                if tile_below in [GROUND, PLATFORM_ONEWAY] and tile_at == EMPTY:
                    positions.append({'x': x, 'y': y - 1})
    
    elif placement_type == 'air':
        # Find empty air spaces above ground
        for y in range(room.height - 6, 5, -1):  # Middle sections
            for x in range(3, room.width - 3):
                tile_at = room.get_tile(x, y)
                if tile_at == EMPTY:
                    # Check there's ground below (within 4 tiles)
                    has_ground_below = False
                    for dy in range(1, 5):
                        if y + dy < room.height:
                            below_tile = room.get_tile(x, y + dy)
                            if below_tile in [GROUND, PLATFORM_ONEWAY]:
                                has_ground_below = True
                                break
                    if has_ground_below:
                        positions.append({'x': x, 'y': y})
    
    elif placement_type == 'ceiling':
        # Find ceiling positions
        for y in range(1, 5):  # Top few rows
            for x in range(2, room.width - 2):
                tile_at = room.get_tile(x, y)
                tile_above = room.get_tile(x, y - 1)
                tile_below = room.get_tile(x, y + 1)
                if tile_above in [WALL, GROUND] and tile_at == EMPTY and tile_below == EMPTY:
                    positions.append({'x': x, 'y': y})
    
    elif placement_type == 'wall':
        # Find wall positions
        for y in range(3, room.height - 3):
            for x in [1, room.width - 2]:  # Left and right walls
                tile_at = room.get_tile(x, y)
                if tile_at == WALL:
                    positions.append({'x': x, 'y': y})
    
    # Randomly sample positions
    if len(positions) > count:
        positions = random.sample(positions, count)
    
    return positions


def place_obstacles(
    room,
    difficulty: int = 5,
    theme: str = 'mixed',
    density: str = 'normal',
    allowed_types: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Place obstacles in a room based on theme and density
    
    Args:
        room: RoomTemplate object
        difficulty: Room difficulty (1-10)
        theme: Obstacle theme ('platforming', 'hazards', 'combat', 'mixed')
        density: Density level ('sparse', 'normal', 'dense', 'extreme')
        allowed_types: List of allowed obstacle types (None = all from theme)
    
    Returns:
        List of obstacle placement dicts
    """
    # Calculate obstacle count
    obstacle_count = calculate_obstacle_count(difficulty, room.width, room.height, density)
    
    placements = []
    
    # Place obstacles
    for _ in range(obstacle_count):
        obstacle_type = select_obstacle_by_theme(theme, allowed_types)
        
        # Find valid positions
        valid_positions = find_valid_obstacle_positions(room, obstacle_type, 1)
        
        if valid_positions:
            pos = valid_positions[0]
            
            placement = {
                'type': obstacle_type,
                'position': pos,
                'properties': OBSTACLE_TYPES[obstacle_type].get('properties', {}).copy(),
                'category': OBSTACLE_TYPES[obstacle_type]['category'],
                'threat_level': OBSTACLE_TYPES[obstacle_type]['threat_level']
            }
            
            placements.append(placement)
    
    return placements


def add_save_point(room, position: Dict[str, int] = None) -> Dict[str, Any]:
    """
    Add a save point to the room
    
    Args:
        room: RoomTemplate object
        position: Position dict {'x': int, 'y': int} or None for auto-placement
    
    Returns:
        Save point placement dict
    """
    if position is None:
        # Auto-place near middle of room on ground
        mid_x = room.width // 2
        
        # Find ground near middle
        for y in range(room.height - 1, room.height - 5, -1):
            for offset in range(5):
                for x in [mid_x + offset, mid_x - offset]:
                    if 0 < x < room.width - 1:
                        tile_below = room.get_tile(x, y)
                        tile_at = room.get_tile(x, y - 1)
                        if tile_below in [GROUND, PLATFORM_ONEWAY] and tile_at == EMPTY:
                            position = {'x': x, 'y': y - 1}
                            break
                if position:
                    break
            if position:
                break
        
        if position is None:
            # Fallback to room center
            position = {'x': mid_x, 'y': room.height - 3}
    
    return {
        'type': 'save_point',
        'position': position,
        'properties': {
            'checkpoint_id': f'cp_{room.id}',
            'healing': True
        }
    }


def get_obstacle_distribution_stats(placements: List[Dict]) -> Dict[str, int]:
    """
    Get statistics about obstacle distribution
    
    Args:
        placements: List of obstacle placement dicts
    
    Returns:
        Dict with counts by category
    """
    stats = {
        'total': len(placements),
        'hazard': 0,
        'platform': 0
    }
    
    for p in placements:
        category = p.get('category', 'unknown')
        stats[category] = stats.get(category, 0) + 1
    
    return stats
