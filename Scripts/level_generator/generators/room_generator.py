"""
Room Generator Orchestrator

Central dispatcher that delegates room generation to shape-specific generators.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.room_template import RoomTemplate
from generators.shape_generators import horizontal_right, horizontal_left, vertical_up, vertical_down, box


def generate_room(shape_type: str, difficulty: int, size: str, 
                  features = None, entrance_dir = None, exit_dir = None,
                  slope_count: int = 2, max_elevation_change: int = 8) -> RoomTemplate:
    """
    Generate a room template with the specified parameters
    
    Args:
        shape_type: Type of room shape ("horizontal_right", "horizontal_left", "vertical_up", "vertical_down", "box")
        difficulty: Difficulty level (1-10)
        size: Room size ("short", "medium", "long" for directional shapes, or "small", "medium", "large" for box)
        features: List of features to include (default: ["platforms", "spikes", "slopes"])
        entrance_dir: Optional entrance direction (only used for box)
        exit_dir: Optional exit direction (only used for box)
        slope_count: Number of slopes to generate in horizontal rooms (default: 2)
        max_elevation_change: Maximum elevation change in tiles (default: 8)
    
    Returns:
        Generated RoomTemplate
    
    Raises:
        ValueError: If shape_type is unknown or if box has invalid entrance/exit directions
    """
    # Default features
    if features is None:
        features = ["platforms", "spikes", "slopes"]
    
    # Validate difficulty
    difficulty = max(1, min(10, difficulty))
    
    # Dispatch to appropriate generator
    if shape_type == "horizontal_right":
        return horizontal_right.generate(difficulty, size, features, slope_count, max_elevation_change)
    
    elif shape_type == "horizontal_left":
        return horizontal_left.generate(difficulty, size, features, slope_count, max_elevation_change)
    
    elif shape_type == "vertical_up":
        return vertical_up.generate(difficulty, size, features)
    
    elif shape_type == "vertical_down":
        return vertical_down.generate(difficulty, size, features)
    
    elif shape_type == "box":
        # Box requires direction parameters
        if entrance_dir is None:
            entrance_dir = 'left'  # default
        if exit_dir is None:
            exit_dir = 'right'  # default
        return box.generate(difficulty, size, features, entrance_dir, exit_dir)
    
    else:
        raise ValueError(f"Unknown shape type: {shape_type}. "
                        f"Available shapes: horizontal_right, horizontal_left, vertical_up, vertical_down, box")


def get_available_shapes() -> list:
    """
    Get list of available shape types
    
    Returns:
        List of shape type names
    """
    return ["horizontal_right", "horizontal_left", "vertical_up", "vertical_down", "box"]


def get_size_options(shape_type: str) -> list:
    """
    Get valid size options for a shape type
    
    Args:
        shape_type: Type of room shape
    
    Returns:
        List of valid size names for this shape
    """
    if shape_type == "box":
        return ["small", "medium", "large"]
    else:
        return ["short", "medium", "long"]
