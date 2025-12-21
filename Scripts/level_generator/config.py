"""
Global configuration for Level Generator Tool
"""

# Tile rendering (for preview only)
PREVIEW_TILE_SIZE = 32  # pixels per tile in preview images

# Game tile size (for UE5 export later)
GAME_TILE_SIZE = 64  # UE5 units

# Default room dimensions
DEFAULT_ROOM_WIDTH = 32
DEFAULT_ROOM_HEIGHT = 18

# Difficulty-based parameters
PLATFORM_COUNT_PER_DIFFICULTY = 0.5  # e.g., diff 6 = 3 platforms
GAP_FREQUENCY_PER_DIFFICULTY = 0.03  # e.g., diff 5 = 0.15 (15% chance per section) - Reduced for more continuous terrain
SPIKE_DENSITY_PER_DIFFICULTY = 0.15  # Spike placement density multiplier

# Jump mechanics (for validation)
MAX_JUMP_DISTANCE = 5  # tiles (horizontal)
MAX_JUMP_HEIGHT = 4    # tiles (vertical)

# Player dimensions (Week 4 - for collision detection)
PLAYER_WIDTH = 1              # Player occupies 1 tile width
PLAYER_HEIGHT = 2             # Player is 2 tiles tall
PLAYER_HEADROOM = 1           # Need 1 tile buffer above head
PLAYER_TOTAL_HEIGHT = 3       # Total clearance needed (HEIGHT + HEADROOM)

# Platform spacing constraints (Week 4)
MIN_PLATFORM_VERTICAL_SPACING = 4  # Minimum gap between stacked platforms
                                   # (3 tiles for player + 1 for platform thickness)

# Visual settings for preview
SHOW_GRID = True
SHOW_METADATA = True
GRID_COLOR = (200, 200, 200)
GRID_LINE_WIDTH = 1

# Door colors
DOOR_ENTRY_COLOR = (0, 255, 0)      # Green
DOOR_EXIT_COLOR = (0, 100, 255)     # Blue
DOOR_HIGHLIGHT_WIDTH = 3

# Metadata banner
METADATA_BANNER_HEIGHT = 40
METADATA_BG_COLOR = (240, 240, 240)
METADATA_TEXT_COLOR = (0, 0, 0)

# Size definitions
SIZE_DIMENSIONS = {
    "horizontal_right": {
        "short": (32, 18),   # Increased from 20 - now supports slopes
        "medium": (48, 18),  # Increased from 32 - more terrain variety
        "long": (64, 18)     # Increased from 48 - extended for complex terrain
    },
    "horizontal_left": {
        "short": (32, 18),   # Increased from 20 - now supports slopes
        "medium": (48, 18),  # Increased from 32 - more terrain variety
        "long": (64, 18)     # Increased from 48 - extended for complex terrain
    },
    "vertical_up": {
        "short": (20, 24),
        "medium": (20, 32),
        "long": (24, 48)
    },
    "vertical_down": {
        "short": (20, 24),
        "medium": (20, 32),
        "long": (24, 48)
    },
    "box": {
        "small": (24, 18),
        "medium": (32, 20),
        "large": (40, 24)
    },
    "staircase": {
        "short": (24, 24),
        "medium": (32, 32),
        "long": (48, 48)
    },
    "zigzag": {
        "short": (24, 24),
        "medium": (32, 32),
        "long": (40, 40)
    }
}
