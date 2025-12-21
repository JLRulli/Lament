"""
Room variation generator - Creates variations of base templates
"""
import random
import copy
from typing import List
from utils.room_template import RoomTemplate
from utils.tile_constants import (
    EMPTY, GROUND, WALL, PLATFORM_ONEWAY, SPIKE, 
    SLOPE_UP_RIGHT, SLOPE_UP_LEFT, SLOPE_DOWN_RIGHT, SLOPE_DOWN_LEFT,
    is_platform, is_hazard, is_slope
)


def swap_platform_positions(room: RoomTemplate, swap_probability: float = 0.3) -> RoomTemplate:
    """
    Create variation by swapping platform positions vertically
    
    Strategy:
    - Find all platforms in the room
    - Randomly select pairs of platforms at similar X positions
    - Swap their Y positions (vertical heights)
    - Maintain structural integrity (don't create impossible jumps)
    
    Args:
        room: Base room template
        swap_probability: Chance to swap each platform pair (0.0-1.0)
    
    Returns:
        New room template with swapped platforms
    """
    variant = room.copy()
    
    # Find all platform positions
    platforms = []
    for y in range(room.height):
        for x in range(room.width):
            if is_platform(room.tiles[y][x]):
                platforms.append((x, y))
    
    if len(platforms) < 2:
        return variant  # Not enough platforms to swap
    
    # Group platforms by X-region (within 3 tiles)
    swapped = set()
    for i, (x1, y1) in enumerate(platforms):
        if (x1, y1) in swapped:
            continue
        
        # Find nearby platforms in X direction
        candidates = []
        for j, (x2, y2) in enumerate(platforms):
            if i != j and (x2, y2) not in swapped:
                if abs(x2 - x1) <= 3 and abs(y2 - y1) >= 2:  # Nearby in X, different in Y
                    candidates.append((x2, y2))
        
        # Randomly swap with one candidate
        if candidates and random.random() < swap_probability:
            x2, y2 = random.choice(candidates)
            
            # Swap the platforms
            variant.tiles[y1][x1] = EMPTY
            variant.tiles[y2][x2] = EMPTY
            variant.tiles[y2][x1] = PLATFORM_ONEWAY
            variant.tiles[y1][x2] = PLATFORM_ONEWAY
            
            swapped.add((x1, y1))
            swapped.add((x2, y2))
    
    return variant


def substitute_obstacles(room: RoomTemplate, substitution_rate: float = 0.4) -> RoomTemplate:
    """
    Create variation by substituting obstacle types
    
    Strategy:
    - Replace spikes with empty space (make easier)
    - Replace empty floor sections with spikes (make harder)
    - Maintain overall difficulty tier
    
    Args:
        room: Base room template
        substitution_rate: Fraction of obstacles to substitute (0.0-1.0)
    
    Returns:
        New room template with substituted obstacles
    """
    variant = room.copy()
    
    # Find all spikes
    spikes = []
    for y in range(room.height):
        for x in range(room.width):
            if variant.tiles[y][x] == SPIKE:
                spikes.append((x, y))
    
    # Find potential spike locations (empty spaces on ground/platform)
    empty_on_ground = []
    for y in range(1, room.height):
        for x in range(room.width):
            if variant.tiles[y][x] == EMPTY:
                # Check if there's solid ground below
                below = variant.tiles[y-1][x] if y > 0 else EMPTY
                if below in [GROUND, WALL, PLATFORM_ONEWAY]:
                    empty_on_ground.append((x, y))
    
    # Remove some spikes
    spikes_to_remove = random.sample(spikes, min(len(spikes), int(len(spikes) * substitution_rate)))
    for x, y in spikes_to_remove:
        variant.tiles[y][x] = EMPTY
    
    # Add some new spikes
    spikes_to_add = random.sample(
        empty_on_ground, 
        min(len(empty_on_ground), int(len(spikes_to_remove) * 0.7))  # Add fewer than removed
    )
    for x, y in spikes_to_add:
        variant.tiles[y][x] = SPIKE
    
    return variant


def mirror_horizontal(room: RoomTemplate) -> RoomTemplate:
    """
    Create variation by mirroring room horizontally (flip left-right)
    
    Strategy:
    - Flip entire tilemap horizontally
    - Reverse slope orientations appropriately
    - Update door connections (entrance <-> exit positions)
    
    Args:
        room: Base room template
    
    Returns:
        New room template mirrored horizontally
    """
    variant = room.copy()
    
    # Create mirrored tilemap
    mirrored_tiles = []
    for y in range(room.height):
        row = []
        for x in range(room.width - 1, -1, -1):  # Iterate backwards
            tile = room.tiles[y][x]
            
            # Flip slope orientations
            if tile == SLOPE_UP_RIGHT:
                tile = SLOPE_UP_LEFT
            elif tile == SLOPE_UP_LEFT:
                tile = SLOPE_UP_RIGHT
            elif tile == SLOPE_DOWN_RIGHT:
                tile = SLOPE_DOWN_LEFT
            elif tile == SLOPE_DOWN_LEFT:
                tile = SLOPE_DOWN_RIGHT
            
            row.append(tile)
        mirrored_tiles.append(row)
    
    variant.tiles = mirrored_tiles
    
    # Update door connections
    new_connections = {}
    for name, conn in room.connections.items():
        new_x = room.width - 1 - conn["position"]["x"]
        new_direction = conn["direction"]
        
        # Flip horizontal directions
        if new_direction == "left":
            new_direction = "right"
        elif new_direction == "right":
            new_direction = "left"
        
        new_connections[name] = {
            "position": {"x": new_x, "y": conn["position"]["y"]},
            "direction": new_direction,
            "type": conn["type"]
        }
    
    variant.connections = new_connections
    
    return variant


def shift_vertical(room: RoomTemplate, max_shift: int = 2) -> RoomTemplate:
    """
    Create variation by vertically shifting platform/obstacle groups
    
    Strategy:
    - Identify groups of connected platforms/obstacles
    - Shift entire groups up or down by 1-2 tiles
    - Maintain floor integrity
    
    Args:
        room: Base room template
        max_shift: Maximum vertical shift in tiles
    
    Returns:
        New room template with shifted elements
    """
    variant = room.copy()
    
    # Find all platforms
    platforms = []
    for y in range(1, room.height):  # Don't shift ground floor
        for x in range(room.width):
            if is_platform(variant.tiles[y][x]):
                platforms.append((x, y))
    
    # Shift random platforms
    for x, y in platforms:
        if random.random() < 0.3:  # 30% chance to shift
            shift = random.randint(-max_shift, max_shift)
            new_y = max(1, min(room.height - 1, y + shift))
            
            if new_y != y and variant.tiles[new_y][x] == EMPTY:
                variant.tiles[y][x] = EMPTY
                variant.tiles[new_y][x] = PLATFORM_ONEWAY
    
    return variant


def add_random_noise(room: RoomTemplate, noise_level: float = 0.05) -> RoomTemplate:
    """
    Create variation by adding random small changes
    
    Strategy:
    - Randomly remove/add single tiles
    - Add/remove individual spikes
    - Minor adjustments for organic feel
    
    Args:
        room: Base room template
        noise_level: Fraction of tiles to potentially modify (0.0-1.0)
    
    Returns:
        New room template with noise added
    """
    variant = room.copy()
    
    total_tiles = room.width * room.height
    modifications = int(total_tiles * noise_level)
    
    for _ in range(modifications):
        x = random.randint(0, room.width - 1)
        y = random.randint(1, room.height - 1)  # Don't modify ground floor
        
        current = variant.tiles[y][x]
        
        # Small random changes
        if current == EMPTY and random.random() < 0.3:
            # Maybe add a platform
            if y > 0 and variant.tiles[y-1][x] == EMPTY:
                variant.tiles[y][x] = PLATFORM_ONEWAY
        elif current == SPIKE and random.random() < 0.5:
            # Maybe remove spike
            variant.tiles[y][x] = EMPTY
    
    return variant


def generate_variations(base_room: RoomTemplate, count: int = 5, 
                       variation_types: List[str] | None = None) -> List[RoomTemplate]:
    """
    Generate multiple variations from a base room template
    
    Strategy:
    - Apply different variation techniques
    - Combine techniques randomly
    - Ensure each variation is unique
    
    Args:
        base_room: Base template to create variations from
        count: Number of variations to generate
        variation_types: List of variation techniques to use
                        Options: 'swap_platforms', 'substitute_obstacles', 
                                'mirror', 'shift', 'noise', 'combined'
    
    Returns:
        List of room template variations (including base as first element)
    """
    if variation_types is None:
        variation_types = ['swap_platforms', 'substitute_obstacles', 'mirror', 'combined']
    
    variations = [base_room]  # Include base template
    
    # Define variation functions
    variation_funcs = {
        'swap_platforms': lambda r: swap_platform_positions(r, swap_probability=0.3),
        'substitute_obstacles': lambda r: substitute_obstacles(r, substitution_rate=0.4),
        'mirror': mirror_horizontal,
        'shift': lambda r: shift_vertical(r, max_shift=2),
        'noise': lambda r: add_random_noise(r, noise_level=0.05),
    }
    
    for i in range(count):
        variant = base_room.copy()
        
        # Randomly select variation type
        if 'combined' in variation_types and random.random() < 0.3:
            # Apply multiple variations
            num_variations = random.randint(2, 3)
            selected = random.sample([k for k in variation_funcs.keys()], 
                                   min(num_variations, len(variation_funcs)))
            for var_type in selected:
                variant = variation_funcs[var_type](variant)
        else:
            # Apply single variation
            available = [t for t in variation_types if t in variation_funcs]
            if available:
                var_type = random.choice(available)
                variant = variation_funcs[var_type](variant)
        
        # Update metadata
        variant.metadata['tags'] = variant.metadata.get('tags', []) + [f'variation_{i+1}']
        variant.id = variant._generate_id()  # New unique ID
        
        variations.append(variant)
    
    return variations


def create_difficulty_variant(base_room: RoomTemplate, target_difficulty: str) -> RoomTemplate:
    """
    Create variation targeting specific difficulty tier
    
    Args:
        base_room: Base template
        target_difficulty: Target tier ('EASY', 'NORMAL', 'HARD', 'EXPERT')
    
    Returns:
        Room template adjusted for target difficulty
    """
    variant = base_room.copy()
    
    if target_difficulty == 'EASY':
        # Remove spikes, add platforms
        for y in range(variant.height):
            for x in range(variant.width):
                if variant.tiles[y][x] == SPIKE:
                    variant.tiles[y][x] = EMPTY
    
    elif target_difficulty == 'EXPERT':
        # Add more spikes, remove some platforms
        variant = substitute_obstacles(variant, substitution_rate=0.6)
    
    return variant
