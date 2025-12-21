"""
Vertical Down shape generator

Generates top-to-bottom descending rooms with platforms and hazards.
Mirror of vertical_up with entrance on top and exit on bottom.
"""
import random
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.room_template import RoomTemplate
from utils.tile_constants import *
import config


def generate(difficulty: int, length: str, features: list) -> RoomTemplate:
    """
    Generate a vertical down room template
    
    Args:
        difficulty: Difficulty level (1-10)
        length: Room height ("short", "medium", "long")
        features: List of features to include (e.g., ["spikes", "platforms"])
    
    Returns:
        Generated RoomTemplate
    """
    # Get dimensions from config (use vertical_up dimensions)
    width, height = config.SIZE_DIMENSIONS["vertical_up"][length]
    
    # Create room template
    room = RoomTemplate(width, height, "vertical_down")
    room.metadata["difficulty"] = difficulty
    room.metadata["length"] = length
    room.metadata["tags"] = features.copy()
    
    # Generate descending path
    _generate_descent_walls(room, difficulty)
    
    # Add platforms for resting
    if "platforms" in features:
        _add_rest_platforms(room, difficulty)
    
    # Add spikes
    if "spikes" in features:
        _add_spikes(room, difficulty)
    
    # Add boundary walls
    _add_boundary_walls(room)
    
    # Add entry and exit doors
    _add_doors(room)
    
    # Add spawn zones
    _add_spawn_zones(room, difficulty)
    
    return room


def _generate_descent_walls(room: RoomTemplate, difficulty: int) -> None:
    """Generate alternating walls for controlled descent"""
    # Create vertical shaft with alternating wall sections
    
    # Left and right wall pattern
    section_height = 6  # Height of each wall section
    current_y = 5  # Start near top
    
    while current_y < room.height - 3:
        # Decide which side to place wall section
        side = random.choice(["left", "right"])
        
        # Wall section height varies
        wall_height = random.randint(4, section_height)
        
        if side == "left":
            # Place wall on left side
            for dy in range(wall_height):
                y = current_y + dy
                if y < room.height:
                    for x in range(0, room.width // 3):
                        room.set_tile(x, y, WALL)
        else:
            # Place wall on right side
            for dy in range(wall_height):
                y = current_y + dy
                if y < room.height:
                    for x in range(room.width - room.width // 3, room.width):
                        room.set_tile(x, y, WALL)
        
        current_y += wall_height + 2  # Move down with gap between sections


def _add_rest_platforms(room: RoomTemplate, difficulty: int) -> None:
    """
    Add platforms for player to rest during descent
    
    Week 4: Enforces MIN_PLATFORM_VERTICAL_SPACING for proper clearance
    """
    # Week 4: Use spacing constant instead of fixed interval
    platform_interval = max(config.MIN_PLATFORM_VERTICAL_SPACING, 
                           10 if difficulty < 5 else 8)
    
    for y in range(platform_interval, room.height - 5, platform_interval):
        # Place platform across middle section
        platform_width = random.randint(4, room.width // 2)
        platform_x = (room.width - platform_width) // 2
        
        # Check if area is clear
        clear = True
        for x in range(platform_x, platform_x + platform_width):
            if room.get_tile(x, y) != EMPTY:
                clear = False
                break
        
        # Week 4: Check headroom (3 tiles above platform)
        # Y=0 is TOP, so "above" means smaller Y values
        if clear:
            for x in range(platform_x, platform_x + platform_width):
                for dy in range(1, config.PLAYER_TOTAL_HEIGHT + 1):
                    check_y = y - dy  # Going UPWARD (toward Y=0)
                    if check_y >= 0:
                        tile = room.get_tile(x, check_y)
                        if tile in [GROUND, WALL, PLATFORM_ONEWAY]:
                            clear = False
                            break
                if not clear:
                    break
        
        if clear:
            for x in range(platform_x, platform_x + platform_width):
                room.set_tile(x, y, PLATFORM_ONEWAY)


def _add_spikes(room: RoomTemplate, difficulty: int) -> None:
    """Add spike hazards on walls and platforms"""
    spike_density = difficulty * 0.1
    
    # Add spikes on wall surfaces
    for y in range(room.height):
        for x in range(room.width):
            tile = room.get_tile(x, y)
            
            # If this is a wall tile adjacent to empty space, might add spike
            if tile == WALL:
                # Check if there's empty space to the right
                if x + 1 < room.width and room.get_tile(x + 1, y) == EMPTY:
                    if random.random() < spike_density:
                        room.set_tile(x + 1, y, SPIKE)
                
                # Check if there's empty space to the left
                if x - 1 >= 0 and room.get_tile(x - 1, y) == EMPTY:
                    if random.random() < spike_density:
                        room.set_tile(x - 1, y, SPIKE)


def _add_boundary_walls(room: RoomTemplate) -> None:
    """Add walls on outer edges"""
    # Top and bottom walls (except door areas)
    for x in range(room.width):
        room.set_tile(x, room.height - 1, GROUND)  # Bottom
        if x < room.width // 3 or x > room.width * 2 // 3:
            room.set_tile(x, 0, WALL)  # Top (partial)
    
    # Left and right walls
    for y in range(room.height):
        room.set_tile(0, y, WALL)
        room.set_tile(room.width - 1, y, WALL)


def _add_doors(room: RoomTemplate) -> None:
    """Add entry (top) and exit (bottom) doors - MIRRORED from vertical_up"""
    # Entry door (TOP center) - mirrored
    entry_x = room.width // 2
    entry_y = 0
    room.add_connection("entrance", entry_x, entry_y, "up")
    
    # Exit door (BOTTOM center) - mirrored
    exit_x = room.width // 2
    exit_y = room.height - 1
    room.add_connection("exit", exit_x, exit_y, "down")
    
    # Clear space around doors and add platforms
    for dx in range(-2, 3):
        x = entry_x + dx
        if 0 <= x < room.width:
            room.set_tile(x, entry_y, EMPTY)
            if entry_y + 1 < room.height:
                room.set_tile(x, entry_y + 1, PLATFORM_ONEWAY)
        
        x = exit_x + dx
        if 0 <= x < room.width:
            room.set_tile(x, exit_y, EMPTY)
            room.set_tile(x, exit_y - 1, PLATFORM_ONEWAY)


def _add_spawn_zones(room: RoomTemplate, difficulty: int) -> None:
    """Mark zones for enemies and obstacles"""
    num_enemy_zones = difficulty
    
    # Add aerial enemy zones (flying enemies)
    for _ in range(num_enemy_zones):
        x = random.randint(2, room.width - 3)
        y = random.randint(5, room.height - 5)
        
        if room.get_tile(x, y) == EMPTY:
            room.add_enemy_zone(x, y, "aerial", ["light_flyer"])
    
    # Add obstacle slots on platforms
    num_obstacle_slots = difficulty // 2
    for _ in range(num_obstacle_slots):
        x = random.randint(2, room.width - 3)
        y = random.randint(5, room.height - 5)
        room.add_obstacle_slot(x, y)
