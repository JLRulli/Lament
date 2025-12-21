"""
Enemy placement system with difficulty-based density control

Places enemies in spawn zones based on room difficulty and theme.
"""
import random
from typing import Dict, List, Any


# Enemy type definitions
ENEMY_TYPES = {
    'light_walker': {
        'weight': 'light',
        'movement': 'ground',
        'threat_level': 1,
        'spawn_types': ['ground']
    },
    'medium_walker': {
        'weight': 'medium',
        'movement': 'ground',
        'threat_level': 3,
        'spawn_types': ['ground']
    },
    'heavy_walker': {
        'weight': 'heavy',
        'movement': 'ground',
        'threat_level': 5,
        'spawn_types': ['ground']
    },
    'light_flyer': {
        'weight': 'light',
        'movement': 'aerial',
        'threat_level': 2,
        'spawn_types': ['aerial']
    },
    'medium_flyer': {
        'weight': 'medium',
        'movement': 'aerial',
        'threat_level': 4,
        'spawn_types': ['aerial']
    },
    'wall_crawler': {
        'weight': 'medium',
        'movement': 'wall',
        'threat_level': 3,
        'spawn_types': ['wall']
    }
}

# Difficulty → Enemy density mapping
# Returns (min_enemies, max_enemies) based on room difficulty (1-10)
DIFFICULTY_DENSITY_MAP = {
    1: (1, 2),   # Very easy
    2: (1, 3),
    3: (2, 4),
    4: (2, 5),
    5: (3, 6),   # Normal
    6: (3, 7),
    7: (4, 8),
    8: (5, 10),
    9: (6, 12),
    10: (7, 15)  # Very hard
}

# Enemy distribution weights by difficulty
# Format: {difficulty: {'light': %, 'medium': %, 'heavy': %}}
DIFFICULTY_WEIGHT_MAP = {
    1: {'light': 100, 'medium': 0, 'heavy': 0},
    2: {'light': 90, 'medium': 10, 'heavy': 0},
    3: {'light': 80, 'medium': 20, 'heavy': 0},
    4: {'light': 70, 'medium': 30, 'heavy': 0},
    5: {'light': 60, 'medium': 35, 'heavy': 5},
    6: {'light': 50, 'medium': 40, 'heavy': 10},
    7: {'light': 40, 'medium': 45, 'heavy': 15},
    8: {'light': 30, 'medium': 50, 'heavy': 20},
    9: {'light': 20, 'medium': 50, 'heavy': 30},
    10: {'light': 10, 'medium': 50, 'heavy': 40}
}


def calculate_enemy_count(difficulty: int, room_size: str = 'medium') -> int:
    """
    Calculate how many enemies to place based on difficulty and room size
    
    Args:
        difficulty: Room difficulty (1-10)
        room_size: 'small', 'medium', 'large'
    
    Returns:
        Number of enemies to place
    """
    difficulty = max(1, min(10, difficulty))
    min_count, max_count = DIFFICULTY_DENSITY_MAP[difficulty]
    
    # Adjust for room size
    if room_size == 'small' or room_size == 'short':
        min_count = max(1, min_count - 1)
        max_count = max(2, max_count - 2)
    elif room_size == 'large' or room_size == 'long':
        min_count += 1
        max_count += 3
    
    return random.randint(min_count, max_count)


def select_enemy_type(difficulty: int, spawn_zone_type: str) -> str:
    """
    Select an enemy type based on difficulty and spawn zone type
    
    Args:
        difficulty: Room difficulty (1-10)
        spawn_zone_type: 'ground', 'aerial', 'wall'
    
    Returns:
        Enemy type string
    """
    difficulty = max(1, min(10, difficulty))
    weights = DIFFICULTY_WEIGHT_MAP[difficulty]
    
    # Get available enemies for this spawn zone type
    available_enemies = [
        enemy_id for enemy_id, data in ENEMY_TYPES.items()
        if spawn_zone_type in data['spawn_types']
    ]
    
    if not available_enemies:
        return None
    
    # Weight by difficulty preference
    weighted_enemies = []
    for enemy_id in available_enemies:
        enemy_weight = ENEMY_TYPES[enemy_id]['weight']
        weight_value = weights.get(enemy_weight, 0)
        
        # Add enemy multiple times based on weight
        weighted_enemies.extend([enemy_id] * weight_value)
    
    if not weighted_enemies:
        return random.choice(available_enemies)
    
    return random.choice(weighted_enemies)


def place_enemies(room, difficulty: int = 5, density_multiplier: float = 1.0) -> List[Dict[str, Any]]:
    """
    Place enemies in a room based on spawn zones
    
    Args:
        room: RoomTemplate object
        difficulty: Room difficulty (1-10)
        density_multiplier: Multiplier for enemy count (0.5 = sparse, 1.0 = normal, 1.5 = dense)
    
    Returns:
        List of enemy placement dicts
    """
    # Get spawn zones from room
    enemy_zones = room.spawn_zones.get('enemies', [])
    
    if not enemy_zones:
        return []
    
    # Calculate enemy count
    room_size = room.metadata.get('size', room.metadata.get('length', 'medium'))
    base_count = calculate_enemy_count(difficulty, room_size)
    enemy_count = int(base_count * density_multiplier)
    enemy_count = max(1, enemy_count)  # At least 1 enemy
    
    # Select spawn zones (sample with replacement if needed)
    selected_zones = []
    if enemy_count <= len(enemy_zones):
        selected_zones = random.sample(enemy_zones, enemy_count)
    else:
        # More enemies than zones, reuse zones
        selected_zones = random.choices(enemy_zones, k=enemy_count)
    
    # Place enemies
    placements = []
    for zone in selected_zones:
        zone_type = zone.get('type', 'ground')
        enemy_type = select_enemy_type(difficulty, zone_type)
        
        if enemy_type:
            placement = {
                'type': enemy_type,
                'position': zone['position'].copy(),
                'zone_id': zone.get('id', 'unknown'),
                'properties': {
                    'threat_level': ENEMY_TYPES[enemy_type]['threat_level'],
                    'movement': ENEMY_TYPES[enemy_type]['movement'],
                    'spawn_zone_type': zone_type
                }
            }
            placements.append(placement)
    
    return placements


def apply_enemy_theme(placements: List[Dict], theme: str) -> List[Dict]:
    """
    Apply thematic filtering to enemy placements
    
    Args:
        placements: List of enemy placement dicts
        theme: 'aggressive', 'sparse', 'aerial_focus', 'ground_focus'
    
    Returns:
        Modified placements list
    """
    if theme == 'aggressive':
        # Increase medium/heavy enemies
        for p in placements:
            if random.random() < 0.3 and ENEMY_TYPES[p['type']]['weight'] == 'light':
                # Upgrade some light enemies to medium
                zone_type = p['properties']['spawn_zone_type']
                medium_options = [
                    eid for eid, data in ENEMY_TYPES.items()
                    if data['weight'] == 'medium' and zone_type in data['spawn_types']
                ]
                if medium_options:
                    p['type'] = random.choice(medium_options)
                    p['properties']['threat_level'] = ENEMY_TYPES[p['type']]['threat_level']
    
    elif theme == 'sparse':
        # Remove some enemies
        remove_count = len(placements) // 3
        if remove_count > 0:
            placements = placements[:-remove_count]
    
    elif theme == 'aerial_focus':
        # Filter to mostly aerial enemies
        placements = [p for p in placements if p['properties']['movement'] == 'aerial']
    
    elif theme == 'ground_focus':
        # Filter to mostly ground enemies
        placements = [p for p in placements if p['properties']['movement'] == 'ground']
    
    return placements


def get_enemy_distribution_stats(placements: List[Dict]) -> Dict[str, int]:
    """
    Get statistics about enemy distribution
    
    Args:
        placements: List of enemy placement dicts
    
    Returns:
        Dict with counts by weight category
    """
    stats = {'light': 0, 'medium': 0, 'heavy': 0, 'total': len(placements)}
    
    for p in placements:
        weight = ENEMY_TYPES[p['type']]['weight']
        stats[weight] = stats.get(weight, 0) + 1
    
    return stats
