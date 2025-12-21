"""
Horizontal Right shape generator

Generates left-to-right linear progression rooms with platforms, gaps, spikes, and slopes.
"""
import random
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.room_template import RoomTemplate
from utils.tile_constants import *
import config


def generate(difficulty: int, length: str, features: list, 
             slope_count: int = 2, max_elevation_change: int = 8) -> RoomTemplate:
    """
    Generate a horizontal right room template
    
    Args:
        difficulty: Difficulty level (1-10)
        length: Room length ("short", "medium", "long")
        features: List of features to include (e.g., ["spikes", "slopes", "platforms"])
        slope_count: Number of slopes to generate (0 for flat terrain)
        max_elevation_change: Maximum elevation change in tiles
    
    Returns:
        Generated RoomTemplate
    """
    # Get dimensions from config
    width, height = config.SIZE_DIMENSIONS["horizontal_right"][length]
    
    # Create room template
    room = RoomTemplate(width, height, "horizontal_right")
    room.metadata["difficulty"] = difficulty
    room.metadata["length"] = length
    room.metadata["tags"] = features.copy()
    
    # Generate base structure with terrain elevation
    # Use slope_count only if "slopes" feature is enabled
    actual_slope_count = slope_count if "slopes" in features else 0
    floor_data = _generate_base_floor(room, difficulty, actual_slope_count, max_elevation_change)
    floor_heights = floor_data['floor_heights']
    
    # Add platforms
    if "platforms" in features:
        _add_platforms(room, difficulty, floor_heights)
    
    # Add spikes
    if "spikes" in features:
        _add_spikes(room, difficulty)
    
    # Add walls on sides and top
    _add_boundary_walls(room)
    
    # Add entry and exit doors
    _add_doors(room, floor_data)
    
    # Add spawn zones
    _add_spawn_zones(room, difficulty)
    
    return room


def _generate_base_floor(room: RoomTemplate, difficulty: int, 
                         slope_count: int, max_elevation_change: int) -> dict:
    """
    Generate base floor with elevation changes and strategic gaps
    
    Returns:
        dict with 'floor_heights' array (Y position for each X), 
        'entrance_y', and 'exit_y' for door placement
    """
    baseline_floor_y = room.height - 2  # Second from bottom
    
    # Initialize floor heights at baseline
    floor_heights = [baseline_floor_y] * room.width
    
    # Plan slopes if enabled - IMPROVED ALGORITHM
    slope_positions = []  # List of (start_x, direction, length)
    cumulative_elevation = 0  # Track cumulative elevation change
    
    if slope_count > 0 and room.width >= 20:  # Lowered minimum width requirement
        # Determine slope length based on room size
        if room.width <= 32:
            min_slope_len, max_slope_len = 3, 5
        elif room.width <= 48:
            min_slope_len, max_slope_len = 4, 6
        else:
            min_slope_len, max_slope_len = 5, 8
        
        # Grid-based placement for guaranteed slopes
        # Divide usable space into sections
        safety_margin_left = 4   # Reduced from 10 - just enough for door clearance
        safety_margin_right = 6  # Reduced from 15
        usable_width = room.width - safety_margin_left - safety_margin_right
        
        if usable_width >= min_slope_len * slope_count:
            # Enough space for all requested slopes
            section_width = usable_width // slope_count
            
            for i in range(slope_count):
                # Calculate section boundaries
                section_start = safety_margin_left + (i * section_width)
                section_end = section_start + section_width
                
                # Random slope length
                slope_length = random.randint(min_slope_len, max_slope_len)
                
                # Ensure slope fits in section
                max_start = section_end - slope_length
                if max_start < section_start:
                    max_start = section_start
                
                # Random position within section
                if max_start > section_start:
                    slope_x = random.randint(section_start, max_start)
                else:
                    slope_x = section_start
                
                # Random direction
                slope_direction = random.choice(['up', 'down'])
                
                # Calculate elevation change
                if slope_direction == 'up':
                    elevation_delta = -slope_length
                else:
                    elevation_delta = slope_length
                
                # Check elevation limit
                if abs(cumulative_elevation + elevation_delta) > max_elevation_change:
                    # Try opposite direction
                    slope_direction = 'down' if slope_direction == 'up' else 'up'
                    elevation_delta = -elevation_delta
                    
                    # If still exceeds, use shorter slope
                    if abs(cumulative_elevation + elevation_delta) > max_elevation_change:
                        slope_length = min(slope_length, max_elevation_change - abs(cumulative_elevation))
                        if slope_length < 3:
                            continue  # Skip if too short
                        elevation_delta = -slope_length if slope_direction == 'up' else slope_length
                
                # Record slope
                slope_positions.append((slope_x, slope_direction, slope_length))
                cumulative_elevation += elevation_delta
    
    # Apply slopes to floor_heights array (sorted by X position to prevent conflicts)
    slope_positions.sort(key=lambda s: s[0])  # Sort by slope_x
    
    for (slope_x, direction, length) in slope_positions:
        # Get starting height (from previous X position)
        start_height = floor_heights[slope_x - 1] if slope_x > 0 else baseline_floor_y
        
        if direction == 'up':
            # Upward slope: floor goes up (Y decreases)
            for i in range(length):
                x = slope_x + i
                if x < room.width:
                    new_y = start_height - i - 1
                    # Clamp to valid range (don't go above ceiling or below floor)
                    floor_heights[x] = max(1, min(room.height - 1, new_y))
            
            # Continue at new elevation for all X after slope
            new_height = floor_heights[slope_x + length - 1]
            for x in range(slope_x + length, room.width):
                floor_heights[x] = new_height
        
        elif direction == 'down':
            # Downward slope: floor goes down (Y increases)
            for i in range(length):
                x = slope_x + i
                if x < room.width:
                    new_y = start_height + i + 1
                    # Clamp to valid range
                    floor_heights[x] = max(1, min(room.height - 1, new_y))
            
            # Continue at new elevation for all X after slope
            new_height = floor_heights[slope_x + length - 1]
            for x in range(slope_x + length, room.width):
                floor_heights[x] = new_height
    
    # Place tiles based on floor_heights
    gap_probability = min(difficulty * config.GAP_FREQUENCY_PER_DIFFICULTY, 0.4)
    
    x = 0
    while x < room.width:
        # Decide if we should create a gap here (not on slopes)
        is_on_slope = any(slope_x <= x < slope_x + length 
                         for (slope_x, _, length) in slope_positions)
        
        if not is_on_slope and x > 5 and x < room.width - 5 and random.random() < gap_probability:
            # Create a gap
            gap_width = random.randint(2, min(4, 2 + difficulty // 3))
            
            # Mark gap by setting floor_heights to room.height (below view)
            for gx in range(x, min(x + gap_width, room.width)):
                floor_heights[gx] = room.height  # Below visible area = gap
            
            x += gap_width
        else:
            # Place floor tile
            floor_y = floor_heights[x]
            
            # Check if this is part of a slope
            slope_tile = None
            for (slope_x, direction, length) in slope_positions:
                if slope_x <= x < slope_x + length:
                    if direction == 'up':
                        slope_tile = SLOPE_UP_RIGHT
                    else:
                        slope_tile = SLOPE_DOWN_RIGHT
                    break
            
            # Place appropriate tile
            if floor_y < room.height:  # Not a gap
                if slope_tile:
                    room.set_tile(x, floor_y, slope_tile)
                else:
                    room.set_tile(x, floor_y, GROUND)
                
                # Fill ground below (foundation)
                for y in range(floor_y + 1, room.height):
                    room.set_tile(x, y, GROUND)
            
            x += 1
    
    # Return floor data
    entrance_floor = floor_heights[1] if 1 < len(floor_heights) else baseline_floor_y
    exit_floor = floor_heights[room.width - 2] if room.width - 2 < len(floor_heights) else baseline_floor_y
    
    return {
        'floor_heights': floor_heights,
        'entrance_y': max(1, min(room.height - 2, entrance_floor - 1)),  # Door above floor
        'exit_y': max(1, min(room.height - 2, exit_floor - 1))  # Door above floor
    }


def _add_platforms(room: RoomTemplate, difficulty: int, floor_heights: list) -> None:
    """
    Add floating platforms based on difficulty
    
    Platforms are positioned relative to local terrain elevation.
    Week 4: Enforces MIN_PLATFORM_VERTICAL_SPACING to ensure player clearance
    """
    platform_count = int(difficulty * config.PLATFORM_COUNT_PER_DIFFICULTY)
    
    # Track placed platforms to enforce spacing (Week 4)
    placed_platforms = []  # List of (x_start, x_end, y)
    
    for _ in range(platform_count):
        # Try up to 20 attempts to find valid position
        for attempt in range(20):
            # Random platform position
            platform_width = random.randint(3, 6)
            platform_x = random.randint(3, room.width - platform_width - 3)
            
            # Get local floor height at platform X position
            local_floor_y = floor_heights[platform_x]
            
            # Skip if this is a gap
            if local_floor_y >= room.height:
                continue
            
            # Position platform above local floor
            # Ensure we have enough room above the floor
            min_platform_y = max(1, local_floor_y - 10)
            max_platform_y = local_floor_y - 3
            
            if max_platform_y < min_platform_y:
                continue  # Not enough vertical space for platform
            
            platform_y = random.randint(min_platform_y, max_platform_y)
            
            # Week 4: Check vertical spacing from existing platforms
            too_close = False
            for (px_start, px_end, py) in placed_platforms:
                # If platforms overlap horizontally
                if not (platform_x + platform_width < px_start or platform_x > px_end):
                    # Check vertical distance
                    if abs(platform_y - py) < config.MIN_PLATFORM_VERTICAL_SPACING:
                        too_close = True
                        break
            
            if too_close:
                continue  # Try again
            
            # Check if area is clear
            clear = True
            for x in range(platform_x, platform_x + platform_width):
                if room.get_tile(x, platform_y) != EMPTY:
                    clear = False
                    break
            
            # Week 4: Also check headroom (3 tiles above platform)
            # Y=0 is TOP, so "above" means smaller Y values
            if clear:
                for x in range(platform_x, platform_x + platform_width):
                    for dy in range(1, config.PLAYER_TOTAL_HEIGHT + 1):
                        check_y = platform_y - dy  # Going UPWARD (toward Y=0)
                        if check_y >= 0:
                            tile = room.get_tile(x, check_y)
                            if tile in [GROUND, WALL, PLATFORM_ONEWAY]:
                                clear = False
                                break
                    if not clear:
                        break
            
            if clear:
                # Place platform
                for x in range(platform_x, platform_x + platform_width):
                    room.set_tile(x, platform_y, PLATFORM_ONEWAY)
                
                # Track this platform
                placed_platforms.append((platform_x, platform_x + platform_width, platform_y))
                break  # Success, move to next platform


def _add_spikes(room: RoomTemplate, difficulty: int) -> None:
    """Add spike hazards in pits and on platforms"""
    spike_density = difficulty * config.SPIKE_DENSITY_PER_DIFFICULTY
    floor_y = room.height - 2
    
    # Add spikes in pits (below gaps in floor)
    for x in range(room.width):
        # Check if this is a gap in the floor
        if room.get_tile(x, floor_y) == EMPTY:
            # Place spike at bottom of pit
            if random.random() < spike_density:
                room.set_tile(x, room.height - 1, SPIKE)
    
    # Add spikes on some platforms (higher difficulty)
    if difficulty >= 5:
        for y in range(floor_y - 10, floor_y):
            for x in range(room.width):
                # Check if there's a platform here
                if room.get_tile(x, y) == PLATFORM_ONEWAY:
                    # Small chance to add spike above platform
                    if random.random() < 0.1:
                        room.set_tile(x, y - 1, SPIKE)


def _add_boundary_walls(room: RoomTemplate) -> None:
    """Add walls on left, right, and top edges"""
    # Top wall
    for x in range(room.width):
        room.set_tile(x, 0, WALL)
    
    # Left wall (except door area)
    door_y = room.height // 2
    for y in range(room.height):
        if abs(y - door_y) > 1:  # Leave space for door
            room.set_tile(0, y, WALL)
    
    # Right wall (except door area)
    for y in range(room.height):
        if abs(y - door_y) > 1:  # Leave space for door
            room.set_tile(room.width - 1, y, WALL)


def _add_doors(room: RoomTemplate, floor_data: dict) -> None:
    """Add entry (left) and exit (right) doors at floor level"""
    # Use entrance/exit Y positions from floor terrain
    entrance_y = floor_data['entrance_y']
    exit_y = floor_data['exit_y']
    
    # Entry door (left side)
    room.add_connection("entrance", 0, entrance_y, "left")
    
    # Exit door (right side)
    room.add_connection("exit", room.width - 1, exit_y, "right")
    
    # Clear space around entrance door
    for dy in range(-1, 2):
        y = entrance_y + dy
        if 0 <= y < room.height:
            room.set_tile(0, y, EMPTY)
    
    # Clear space around exit door
    for dy in range(-1, 2):
        y = exit_y + dy
        if 0 <= y < room.height:
            room.set_tile(room.width - 1, y, EMPTY)
    
    # Add landing platforms near doors if needed
    entrance_floor_y = floor_data['floor_heights'][1]
    exit_floor_y = floor_data['floor_heights'][room.width - 2]
    
    if entrance_floor_y < room.height and room.get_tile(1, entrance_floor_y) == EMPTY:
        room.set_tile(1, entrance_floor_y, PLATFORM_ONEWAY)
    
    if exit_floor_y < room.height and room.get_tile(room.width - 2, exit_floor_y) == EMPTY:
        room.set_tile(room.width - 2, exit_floor_y, PLATFORM_ONEWAY)


def _add_spawn_zones(room: RoomTemplate, difficulty: int) -> None:
    """Mark zones for enemies and obstacles"""
    baseline_floor_y = room.height - 2
    
    # Add enemy spawn zones on platforms and flat ground
    num_enemy_zones = difficulty
    for _ in range(num_enemy_zones):
        x = random.randint(5, room.width - 5)
        y = random.randint(max(1, baseline_floor_y - 10), baseline_floor_y)
        
        # Check if there's a platform or ground below
        if room.get_tile(x, y + 1) in [GROUND, PLATFORM_ONEWAY]:
            room.add_enemy_zone(x, y, "ground")
    
    # Add obstacle slots
    num_obstacle_slots = difficulty // 2
    for _ in range(num_obstacle_slots):
        x = random.randint(5, room.width - 5)
        y = random.randint(max(1, baseline_floor_y - 8), baseline_floor_y)
        room.add_obstacle_slot(x, y)
