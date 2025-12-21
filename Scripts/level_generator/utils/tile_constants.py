"""
Tile type constants and definitions for Level Generator
"""

# Tile type constants
EMPTY = 0
GROUND = 1
WALL = 2
PLATFORM_ONEWAY = 3
SPIKE = 4
PIT = 5  # For future use

# Slope tiles (45-degree angles)
SLOPE_UP_RIGHT = 10    # Ascending to the right: /
SLOPE_UP_LEFT = 11     # Ascending to the left: \
SLOPE_DOWN_RIGHT = 12  # Descending to the right: \
SLOPE_DOWN_LEFT = 13   # Descending to the left: /

# Tile legend for JSON export
TILE_LEGEND = {
    0: "empty",
    1: "ground",
    2: "wall",
    3: "platform_oneway",
    4: "spike",
    5: "pit",
    10: "slope_up_right",
    11: "slope_up_left",
    12: "slope_down_right",
    13: "slope_down_left"
}

# Color mapping for visualizer (RGB)
TILE_COLORS = {
    0: (255, 255, 255),      # Empty: white
    1: (101, 67, 33),        # Ground: brown
    2: (64, 64, 64),         # Wall: dark gray
    3: (135, 206, 250),      # Platform: light blue
    4: (255, 0, 0),          # Spike: red
    5: (0, 0, 0),            # Pit: black
    10: (101, 67, 33),       # Slopes: brown (same as ground)
    11: (101, 67, 33),       # Slopes: brown
    12: (101, 67, 33),       # Slopes: brown
    13: (101, 67, 33)        # Slopes: brown
}

# Helper functions
def is_solid(tile_id):
    """Check if tile is solid (blocks movement)"""
    return tile_id in [GROUND, WALL]

def is_hazard(tile_id):
    """Check if tile is a hazard (deals damage)"""
    return tile_id in [SPIKE, PIT]

def is_slope(tile_id):
    """Check if tile is a slope"""
    return tile_id in [SLOPE_UP_RIGHT, SLOPE_UP_LEFT, SLOPE_DOWN_RIGHT, SLOPE_DOWN_LEFT]

def is_platform(tile_id):
    """Check if tile is a platform (solid from top only)"""
    return tile_id == PLATFORM_ONEWAY

def get_tile_name(tile_id):
    """Get human-readable name for tile ID"""
    return TILE_LEGEND.get(tile_id, f"unknown_{tile_id}")
