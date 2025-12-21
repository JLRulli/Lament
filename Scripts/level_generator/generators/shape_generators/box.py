"""
Box (Arena) shape generator

Generates enclosed combat arenas with multiple platform levels for enemy encounters.
"""
import random
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.room_template import RoomTemplate
from utils.tile_constants import *
import config


def generate(difficulty: int, size: str, features: list, 
             entrance_dir: str = 'left', exit_dir: str = 'right') -> RoomTemplate:
    """
    Generate a box arena room template
    
    Args:
        difficulty: Difficulty level (1-10)
        size: Arena size ("small", "medium", "large")
        features: List of features to include (e.g., ["spikes", "platforms"])
        entrance_dir: Direction of entrance door ('left', 'right', 'up', 'down')
        exit_dir: Direction of exit door ('left', 'right', 'up', 'down')
    
    Returns:
        Generated RoomTemplate
    
    Raises:
        ValueError: If entrance_dir == exit_dir (cannot have same-side entrance/exit)
    """
    # Validate: entrance and exit cannot be the same direction
    if entrance_dir == exit_dir:
        raise ValueError(f"Box entrance and exit cannot be same direction: {entrance_dir}")
    # Get dimensions from config
    width, height = config.SIZE_DIMENSIONS["box"][size]
    
    # Create room template
    room = RoomTemplate(width, height, "box")
    room.metadata["difficulty"] = difficulty
    room.metadata["length"] = size
    room.metadata["tags"] = features.copy()
    
    # Create enclosed arena (will clear door areas later)
    _create_boundary(room, entrance_dir, exit_dir)
    
    # Add platform levels
    if "platforms" in features:
        _add_platform_levels(room, difficulty)
    
    # Add hazards
    if "spikes" in features:
        _add_hazards(room, difficulty)
    
    # Add entry and exit doors
    _add_doors(room, entrance_dir, exit_dir)
    
    # Add spawn zones
    _add_spawn_zones(room, difficulty)
    
    return room


def _create_boundary(room: RoomTemplate, entrance_dir: str, exit_dir: str) -> None:
    """
    Create perimeter walls and floor
    
    Args:
        room: Room template to modify
        entrance_dir: Entrance direction (affects which walls to create)
        exit_dir: Exit direction (affects which walls to create)
    """
    # Floor (unless door is on bottom)
    if entrance_dir != 'down' and exit_dir != 'down':
        for x in range(room.width):
            room.set_tile(x, room.height - 1, GROUND)
    else:
        # Partial floor, leaving space for door
        mid_width = room.width // 2
        for x in range(room.width):
            if entrance_dir == 'down' and abs(x - mid_width) <= 2:
                continue  # Leave space for entrance
            if exit_dir == 'down' and abs(x - mid_width) <= 2:
                continue  # Leave space for exit
            room.set_tile(x, room.height - 1, GROUND)
    
    # Ceiling (unless door is on top)
    if entrance_dir != 'up' and exit_dir != 'up':
        for x in range(room.width):
            room.set_tile(x, 0, WALL)
    else:
        # Partial ceiling, leaving space for door
        mid_width = room.width // 2
        for x in range(room.width):
            if entrance_dir == 'up' and abs(x - mid_width) <= 2:
                continue  # Leave space for entrance
            if exit_dir == 'up' and abs(x - mid_width) <= 2:
                continue  # Leave space for exit
            room.set_tile(x, 0, WALL)
    
    # Left wall (unless door is on left)
    if entrance_dir != 'left' and exit_dir != 'left':
        for y in range(room.height):
            room.set_tile(0, y, WALL)
    else:
        # Partial wall, leaving space for door
        mid_height = room.height // 2
        for y in range(room.height):
            if entrance_dir == 'left' and abs(y - mid_height) <= 1:
                continue  # Leave space for entrance
            if exit_dir == 'left' and abs(y - mid_height) <= 1:
                continue  # Leave space for exit
            room.set_tile(0, y, WALL)
    
    # Right wall (unless door is on right)
    if entrance_dir != 'right' and exit_dir != 'right':
        for y in range(room.height):
            room.set_tile(room.width - 1, y, WALL)
    else:
        # Partial wall, leaving space for door
        mid_height = room.height // 2
        for y in range(room.height):
            if entrance_dir == 'right' and abs(y - mid_height) <= 1:
                continue  # Leave space for entrance
            if exit_dir == 'right' and abs(y - mid_height) <= 1:
                continue  # Leave space for exit
            room.set_tile(room.width - 1, y, WALL)


def _add_platform_levels(room: RoomTemplate, difficulty: int) -> None:
    """
    Add multiple platform tiers for vertical combat space
    
    Week 4: Enforces MIN_PLATFORM_VERTICAL_SPACING for proper clearance
    """
    # Number of platform levels based on difficulty
    num_levels = 2 if difficulty < 5 else 3
    
    floor_y = room.height - 1
    # Week 4: Ensure level spacing is at least MIN_PLATFORM_VERTICAL_SPACING
    level_spacing = max(config.MIN_PLATFORM_VERTICAL_SPACING,
                       (floor_y - 4) // (num_levels + 1))
    
    for i in range(1, num_levels + 1):
        level_y = floor_y - (i * level_spacing)
        
        # Decide platform layout for this level
        layout = random.choice(["split", "center", "edges"])
        
        if layout == "split":
            # Two platforms on left and right
            # Left platform
            left_width = random.randint(4, room.width // 3)
            for x in range(2, 2 + left_width):
                if x < room.width:
                    room.set_tile(x, level_y, PLATFORM_ONEWAY)
            
            # Right platform
            right_width = random.randint(4, room.width // 3)
            for x in range(room.width - 2 - right_width, room.width - 2):
                if x >= 0:
                    room.set_tile(x, level_y, PLATFORM_ONEWAY)
        
        elif layout == "center":
            # Single platform in center
            platform_width = random.randint(6, room.width // 2)
            platform_x = (room.width - platform_width) // 2
            for x in range(platform_x, platform_x + platform_width):
                room.set_tile(x, level_y, PLATFORM_ONEWAY)
        
        else:  # edges
            # Small platforms on far left and right edges
            for x in range(2, 5):
                room.set_tile(x, level_y, PLATFORM_ONEWAY)
            for x in range(room.width - 5, room.width - 2):
                room.set_tile(x, level_y, PLATFORM_ONEWAY)


def _add_hazards(room: RoomTemplate, difficulty: int) -> None:
    """Add spike hazards in corners and on some platforms"""
    floor_y = room.height - 1
    
    # Add spikes in corners at floor level
    if difficulty >= 3:
        # Bottom left corner
        for x in range(2, 4):
            room.set_tile(x, floor_y, SPIKE)
        
        # Bottom right corner
        for x in range(room.width - 4, room.width - 2):
            room.set_tile(x, floor_y, SPIKE)
    
    # Add spikes on some platforms (higher difficulty)
    if difficulty >= 6:
        for y in range(floor_y):
            for x in range(room.width):
                if room.get_tile(x, y) == PLATFORM_ONEWAY:
                    # Small chance to add spike below platform (hazard when dropping)
                    if random.random() < 0.1:
                        if y + 1 < room.height and room.get_tile(x, y + 1) == EMPTY:
                            room.set_tile(x, y + 1, SPIKE)


def _add_doors(room: RoomTemplate, entrance_dir: str, exit_dir: str) -> None:
    """
    Add entry and exit doors based on specified directions
    
    Args:
        room: Room template to modify
        entrance_dir: Entrance direction ('left', 'right', 'up', 'down')
        exit_dir: Exit direction ('left', 'right', 'up', 'down')
    """
    mid_width = room.width // 2
    mid_height = room.height // 2
    
    # Add entrance door based on direction
    if entrance_dir == 'left':
        room.add_connection("entrance", 0, mid_height, "left")
        # Clear space around door
        for dy in range(-1, 2):
            y = mid_height + dy
            if 0 <= y < room.height:
                room.set_tile(0, y, EMPTY)
                room.set_tile(1, y, EMPTY)
        # Add landing platform
        if mid_height + 2 < room.height:
            for x in range(2, 5):
                room.set_tile(x, mid_height + 1, PLATFORM_ONEWAY)
    
    elif entrance_dir == 'right':
        room.add_connection("entrance", room.width - 1, mid_height, "right")
        # Clear space around door
        for dy in range(-1, 2):
            y = mid_height + dy
            if 0 <= y < room.height:
                room.set_tile(room.width - 1, y, EMPTY)
                room.set_tile(room.width - 2, y, EMPTY)
        # Add landing platform
        if mid_height + 2 < room.height:
            for x in range(room.width - 5, room.width - 2):
                room.set_tile(x, mid_height + 1, PLATFORM_ONEWAY)
    
    elif entrance_dir == 'up':
        room.add_connection("entrance", mid_width, 0, "up")
        # Clear space around door
        for dx in range(-2, 3):
            x = mid_width + dx
            if 0 <= x < room.width:
                room.set_tile(x, 0, EMPTY)
                if 1 < room.height:
                    room.set_tile(x, 1, EMPTY)
        # Add landing platform
        for dx in range(-2, 3):
            x = mid_width + dx
            if 0 <= x < room.width and 2 < room.height:
                room.set_tile(x, 2, PLATFORM_ONEWAY)
    
    elif entrance_dir == 'down':
        room.add_connection("entrance", mid_width, room.height - 1, "down")
        # Clear space around door
        for dx in range(-2, 3):
            x = mid_width + dx
            if 0 <= x < room.width:
                room.set_tile(x, room.height - 1, EMPTY)
                if room.height - 2 >= 0:
                    room.set_tile(x, room.height - 2, EMPTY)
        # Add landing platform
        for dx in range(-2, 3):
            x = mid_width + dx
            if 0 <= x < room.width and room.height - 3 >= 0:
                room.set_tile(x, room.height - 3, PLATFORM_ONEWAY)
    
    # Add exit door based on direction
    if exit_dir == 'left':
        room.add_connection("exit", 0, mid_height, "left")
        # Clear space around door
        for dy in range(-1, 2):
            y = mid_height + dy
            if 0 <= y < room.height:
                room.set_tile(0, y, EMPTY)
                room.set_tile(1, y, EMPTY)
        # Add landing platform
        if mid_height + 2 < room.height:
            for x in range(2, 5):
                room.set_tile(x, mid_height + 1, PLATFORM_ONEWAY)
    
    elif exit_dir == 'right':
        room.add_connection("exit", room.width - 1, mid_height, "right")
        # Clear space around door
        for dy in range(-1, 2):
            y = mid_height + dy
            if 0 <= y < room.height:
                room.set_tile(room.width - 1, y, EMPTY)
                room.set_tile(room.width - 2, y, EMPTY)
        # Add landing platform
        if mid_height + 2 < room.height:
            for x in range(room.width - 5, room.width - 2):
                room.set_tile(x, mid_height + 1, PLATFORM_ONEWAY)
    
    elif exit_dir == 'up':
        room.add_connection("exit", mid_width, 0, "up")
        # Clear space around door
        for dx in range(-2, 3):
            x = mid_width + dx
            if 0 <= x < room.width:
                room.set_tile(x, 0, EMPTY)
                if 1 < room.height:
                    room.set_tile(x, 1, EMPTY)
        # Add landing platform
        for dx in range(-2, 3):
            x = mid_width + dx
            if 0 <= x < room.width and 2 < room.height:
                room.set_tile(x, 2, PLATFORM_ONEWAY)
    
    elif exit_dir == 'down':
        room.add_connection("exit", mid_width, room.height - 1, "down")
        # Clear space around door
        for dx in range(-2, 3):
            x = mid_width + dx
            if 0 <= x < room.width:
                room.set_tile(x, room.height - 1, EMPTY)
                if room.height - 2 >= 0:
                    room.set_tile(x, room.height - 2, EMPTY)
        # Add landing platform
        for dx in range(-2, 3):
            x = mid_width + dx
            if 0 <= x < room.width and room.height - 3 >= 0:
                room.set_tile(x, room.height - 3, PLATFORM_ONEWAY)


def _add_spawn_zones(room: RoomTemplate, difficulty: int) -> None:
    """Mark zones for enemies and obstacles"""
    # Dense enemy spawn zones for combat arena
    num_enemy_zones = difficulty * 2  # More enemies in arenas
    floor_y = room.height - 1
    
    # Add enemy zones on ground and platforms
    for _ in range(num_enemy_zones):
        x = random.randint(3, room.width - 3)
        y = random.randint(floor_y - 12, floor_y - 1)
        
        # Check if there's a platform or ground below
        if room.get_tile(x, y + 1) in [GROUND, PLATFORM_ONEWAY]:
            room.add_enemy_zone(x, y, "ground")
    
    # Fewer obstacle slots (combat-focused)
    num_obstacle_slots = max(1, difficulty // 3)
    for _ in range(num_obstacle_slots):
        x = random.randint(3, room.width - 3)
        y = random.randint(floor_y - 10, floor_y - 1)
        room.add_obstacle_slot(x, y, ["spike", "platform_oneway"])
