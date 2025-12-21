"""
World structure generator for multi-level generation

Generates complete worlds with difficulty progression and thematic variety.
"""
import random
from typing import List, Dict, Any
from generators.room_generator import generate_room
from validation.validator_simple import validate_room_simple
from validation.quality import score_room_quality
from validation.spawn_zones import assign_spawn_zones_to_room
from entities.enemy_placer import place_enemies, get_enemy_distribution_stats
from entities.obstacle_placer import place_obstacles, add_save_point, get_obstacle_distribution_stats


class LevelConfig:
    """Configuration for a single level"""
    
    def __init__(
        self,
        level_id: str,
        difficulty: int,
        shape_type: str = None,
        size: str = 'medium',
        entrance_dir: str = None,
        exit_dir: str = None,
        slope_count: int = 2,
        max_elevation_change: int = 8,
        obstacle_theme: str = 'mixed',
        obstacle_density: str = 'normal',
        enemy_density: float = 1.0,
        include_save_point: bool = False
    ):
        self.level_id = level_id
        self.difficulty = max(1, min(10, difficulty))
        self.shape_type = shape_type or random.choice(['horizontal_right', 'vertical_up', 'box'])
        self.size = size
        self.entrance_dir = entrance_dir
        self.exit_dir = exit_dir
        self.slope_count = slope_count
        self.max_elevation_change = max_elevation_change
        self.obstacle_theme = obstacle_theme
        self.obstacle_density = obstacle_density
        self.enemy_density = enemy_density
        self.include_save_point = include_save_point


class WorldConfig:
    """Configuration for a complete world"""
    
    def __init__(
        self,
        world_name: str,
        level_count: int = 7,
        difficulty_curve: str = 'linear',
        horizontal_vertical_ratio: float = 0.5,
        slope_count: int = 2,
        max_elevation_change: int = 8,
        predominance: str = None  # Deprecated, use horizontal_vertical_ratio instead
    ):
        self.world_name = world_name
        self.level_count = level_count
        self.difficulty_curve = difficulty_curve
        self.slope_count = max(0, slope_count)  # Number of slopes in horizontal rooms
        self.max_elevation_change = max(0, max_elevation_change)  # Max elevation change in tiles
        
        # Support both new ratio system and old predominance system
        if predominance is not None:
            # Convert old predominance to ratio
            ratio_map = {'horizontal': 0.2, 'vertical': 0.8, 'mixed': 0.5}
            self.horizontal_vertical_ratio = ratio_map.get(predominance, 0.5)
        else:
            self.horizontal_vertical_ratio = max(0.0, min(1.0, horizontal_vertical_ratio))


def calculate_difficulty_curve(level_index: int, total_levels: int, curve_type: str = 'linear') -> int:
    """
    Calculate difficulty for a specific level based on progression curve
    
    Args:
        level_index: 0-based level index
        total_levels: Total number of levels
        curve_type: 'linear', 'spike', 'plateau'
    
    Returns:
        Difficulty value (1-10)
    """
    progress = level_index / max(1, total_levels - 1)  # 0.0 to 1.0
    
    if curve_type == 'linear':
        # Straight progression from 1 to 10
        difficulty = 1 + int(progress * 9)
    
    elif curve_type == 'spike':
        # Easy → Hard → Medium pattern
        if progress < 0.3:
            difficulty = 1 + int(progress * 3 / 0.3)  # 1-4
        elif progress < 0.7:
            difficulty = 4 + int((progress - 0.3) * 6 / 0.4)  # 4-10
        else:
            difficulty = 10 - int((progress - 0.7) * 5 / 0.3)  # 10-5
    
    elif curve_type == 'plateau':
        # Gradual steps with plateaus
        if progress < 0.25:
            difficulty = 2
        elif progress < 0.5:
            difficulty = 4
        elif progress < 0.75:
            difficulty = 7
        else:
            difficulty = 9
    
    else:
        difficulty = 5
    
    return max(1, min(10, difficulty))


def select_next_level_shape_and_directions(
    prev_exit_dir: str,
    horizontal_vertical_ratio: float,
    prev_shape: str = None
) -> tuple:
    """
    Select next level's shape type, entrance direction, and exit direction
    
    Args:
        prev_exit_dir: Previous level's exit direction ('left', 'right', 'up', 'down')
        horizontal_vertical_ratio: 0.0=horizontal, 1.0=vertical
        prev_shape: Previous shape to avoid repetition
    
    Returns:
        (shape_type, entrance_dir, exit_dir) tuple
        - shape_type: Name of shape generator to use
        - entrance_dir: Direction for entrance door  
        - exit_dir: Direction for exit door (None for non-box shapes)
    """
    # Map exit direction to required entrance direction (opposite)
    opposite_dir = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up'
    }
    
    required_entrance = opposite_dir[prev_exit_dir]
    
    # Determine if we're on horizontal or vertical axis
    is_horizontal_axis = prev_exit_dir in ['left', 'right']
    is_vertical_axis = prev_exit_dir in ['up', 'down']
    
    # Calculate probability of changing axis
    if is_horizontal_axis:
        # Currently horizontal, chance to go vertical based on ratio
        change_axis_probability = horizontal_vertical_ratio * 0.9  # 90% of ratio for variety
    else:
        # Currently vertical, chance to go horizontal based on (1 - ratio)
        change_axis_probability = (1.0 - horizontal_vertical_ratio) * 0.9
    
    # Decide if we change axis
    change_axis = random.random() < change_axis_probability
    
    if change_axis:
        # Use box to transition
        if is_horizontal_axis:
            # Going from horizontal to vertical
            exit_options = ['up', 'down']
        else:
            # Going from vertical to horizontal
            exit_options = ['left', 'right']
        
        exit_dir = random.choice(exit_options)
        return ('box', required_entrance, exit_dir)
    
    else:
        # Continue on same axis
        if required_entrance == 'left':
            shape = 'horizontal_right'
            actual_exit = 'right'
        elif required_entrance == 'right':
            shape = 'horizontal_left'
            actual_exit = 'left'
        elif required_entrance == 'down':
            shape = 'vertical_up'
            actual_exit = 'up'
        elif required_entrance == 'up':
            shape = 'vertical_down'
            actual_exit = 'down'
        else:
            # Fallback
            shape = 'horizontal_right'
            actual_exit = 'right'
        
        # Occasionally use box for variety even when staying on same axis
        if shape == prev_shape and random.random() < 0.3:
            # Insert box as variety
            if is_horizontal_axis:
                exit_dir = 'right' if required_entrance == 'left' else 'left'
            else:
                exit_dir = 'up' if required_entrance == 'down' else 'down'
            return ('box', required_entrance, exit_dir)
        
        return (shape, required_entrance, None)  # None for exit_dir (not box)


def select_size_for_difficulty(difficulty: int, shape_type: str) -> str:
    """
    Select appropriate size based on difficulty
    
    Args:
        difficulty: 1-10
        shape_type: Shape type
    
    Returns:
        Size string
    """
    if shape_type == 'box':
        if difficulty <= 3:
            return 'small'
        elif difficulty <= 7:
            return 'medium'
        else:
            return 'large'
    else:  # horizontal or vertical
        if difficulty <= 3:
            return 'short'
        elif difficulty <= 7:
            return 'medium'
        else:
            return 'long'


def generate_level_config(
    level_index: int,
    world_config: WorldConfig,
    prev_exit_dir: str = None,
    prev_shape: str = None
) -> tuple:
    """
    Generate configuration for a single level
    
    Args:
        level_index: 0-based level index
        world_config: World configuration
        prev_exit_dir: Previous level's exit direction (None for first level)
        prev_shape: Previous level's shape type
    
    Returns:
        Tuple of (LevelConfig, actual_exit_dir)
    """
    difficulty = calculate_difficulty_curve(
        level_index,
        world_config.level_count,
        world_config.difficulty_curve
    )
    
    # First level: always start with horizontal_right (conventional start)
    if level_index == 0:
        shape = 'horizontal_right'
        entrance_dir = 'left'
        exit_dir = None  # Not box, will be 'right' from generator
        actual_exit_dir = 'right'
    else:
        # Select based on previous exit direction
        shape, entrance_dir, exit_dir = select_next_level_shape_and_directions(
            prev_exit_dir,
            world_config.horizontal_vertical_ratio,
            prev_shape
        )
        
        # Determine actual exit direction
        if shape == 'box':
            actual_exit_dir = exit_dir
        elif shape == 'horizontal_right':
            actual_exit_dir = 'right'
        elif shape == 'horizontal_left':
            actual_exit_dir = 'left'
        elif shape == 'vertical_up':
            actual_exit_dir = 'up'
        elif shape == 'vertical_down':
            actual_exit_dir = 'down'
        else:
            # Fallback
            actual_exit_dir = 'right'
    
    size = select_size_for_difficulty(difficulty, shape)
    
    # Select theme based on difficulty and variety
    themes = ['platforming', 'hazards', 'mixed', 'combat']
    theme_index = level_index % len(themes)
    obstacle_theme = themes[theme_index]
    
    # Density increases with difficulty
    if difficulty <= 3:
        density = 'sparse'
    elif difficulty <= 7:
        density = 'normal'
    else:
        density = 'dense'
    
    # Enemy density also scales
    enemy_density = 0.7 + (difficulty / 10.0) * 0.6  # 0.7 to 1.3
    
    # Save points every 3 levels
    include_save_point = (level_index + 1) % 3 == 0 or level_index == 0
    
    level_id = f"{world_config.world_name}_L{level_index+1:02d}"
    
    level_config = LevelConfig(
        level_id=level_id,
        difficulty=difficulty,
        shape_type=shape,
        size=size,
        entrance_dir=entrance_dir,
        exit_dir=exit_dir,
        slope_count=world_config.slope_count,
        max_elevation_change=world_config.max_elevation_change,
        obstacle_theme=obstacle_theme,
        obstacle_density=density,
        enemy_density=enemy_density,
        include_save_point=include_save_point
    )
    
    return level_config, actual_exit_dir


def generate_populated_room(
    level_config: LevelConfig,
    max_attempts: int = 10
) -> Dict[str, Any]:
    """
    Generate a room with enemies and obstacles
    
    Args:
        level_config: Level configuration
        max_attempts: Max attempts to generate valid room
    
    Returns:
        Dict with room, validation, quality, entities
    """
    best_room = None
    best_quality = 0
    
    for attempt in range(max_attempts):
        # Generate base room
        room = generate_room(
            level_config.shape_type,
            level_config.difficulty,
            level_config.size,
            ['platforms', 'spikes', 'slopes'],
            entrance_dir=level_config.entrance_dir,
            exit_dir=level_config.exit_dir,
            slope_count=level_config.slope_count,
            max_elevation_change=level_config.max_elevation_change
        )
        
        # Validate
        validation = validate_room_simple(room, use_pathfinding=False)
        
        if not validation['valid']:
            continue
        
        # Assign spawn zones
        assign_spawn_zones_to_room(room)
        
        # Score quality
        quality = score_room_quality(room, validation)
        
        # Keep best
        if quality['overall'] > best_quality:
            best_quality = quality['overall']
            best_room = room
        
        # If we got a good one, use it
        if quality['overall'] >= 6.0:
            break
    
    if best_room is None:
        # Fallback to last attempt even if poor quality
        best_room = room
        validation = validate_room_simple(best_room, use_pathfinding=False)
        quality = score_room_quality(best_room, validation)
    
    # Place entities
    enemies = place_enemies(
        best_room,
        level_config.difficulty,
        level_config.enemy_density
    )
    
    obstacles = place_obstacles(
        best_room,
        level_config.difficulty,
        level_config.obstacle_theme,
        level_config.obstacle_density
    )
    
    # Add save point if needed
    save_point = None
    if level_config.include_save_point:
        save_point = add_save_point(best_room)
    
    # Package results
    result = {
        'level_id': level_config.level_id,
        'room': best_room,
        'validation': validation,
        'quality': quality,
        'entities': {
            'enemies': enemies,
            'obstacles': obstacles,
            'save_point': save_point
        },
        'stats': {
            'difficulty': level_config.difficulty,
            'shape': level_config.shape_type,
            'size': level_config.size,
            'quality_score': quality['overall'],
            'enemy_count': len(enemies),
            'obstacle_count': len(obstacles),
            'has_save_point': save_point is not None
        }
    }
    
    return result


def generate_world(world_config: WorldConfig, verbose: bool = True) -> List[Dict[str, Any]]:
    """
    Generate a complete world with multiple levels
    
    Args:
        world_config: World configuration
        verbose: Print progress messages
    
    Returns:
        List of level dicts
    """
    if verbose:
        print("=" * 60)
        print(f"WORLD GENERATION: {world_config.world_name}")
        print("=" * 60)
        print(f"Levels: {world_config.level_count}")
        print(f"Difficulty Curve: {world_config.difficulty_curve}")
        ratio_pct = int(world_config.horizontal_vertical_ratio * 100)
        print(f"Horizontal/Vertical: {100-ratio_pct}%/{ratio_pct}%")
        print()
    
    levels = []
    prev_shape = None
    prev_exit_dir = None  # Track exit direction for connection matching
    
    for i in range(world_config.level_count):
        if verbose:
            print(f"Generating Level {i+1}/{world_config.level_count}...", end=' ')
        
        # Generate level config with direction tracking
        level_config, exit_dir = generate_level_config(
            i, 
            world_config, 
            prev_exit_dir, 
            prev_shape
        )
        
        # Generate populated room
        level_data = generate_populated_room(level_config)
        
        levels.append(level_data)
        prev_shape = level_config.shape_type
        prev_exit_dir = exit_dir  # Track for next iteration
        
        if verbose:
            stats = level_data['stats']
            print(f"✓ {stats['shape']} (Diff {stats['difficulty']}, "
                  f"Quality {stats['quality_score']:.1f}, "
                  f"{stats['enemy_count']} enemies, "
                  f"{stats['obstacle_count']} obstacles)")
    
    if verbose:
        print()
        print_world_summary(levels)
    
    return levels


def print_world_summary(levels: List[Dict[str, Any]]):
    """Print summary statistics for generated world"""
    print("=" * 60)
    print("WORLD SUMMARY")
    print("=" * 60)
    
    total_enemies = sum(len(lvl['entities']['enemies']) for lvl in levels)
    total_obstacles = sum(len(lvl['entities']['obstacles']) for lvl in levels)
    avg_quality = sum(lvl['quality']['overall'] for lvl in levels) / len(levels)
    save_point_count = sum(1 for lvl in levels if lvl['entities']['save_point'])
    
    print(f"Total Levels: {len(levels)}")
    print(f"Average Quality: {avg_quality:.2f}")
    print(f"Total Enemies: {total_enemies}")
    print(f"Total Obstacles: {total_obstacles}")
    print(f"Save Points: {save_point_count}")
    print()
    
    print("Difficulty Progression:")
    for i, lvl in enumerate(levels):
        print(f"  L{i+1:02d}: Difficulty {lvl['stats']['difficulty']}, "
              f"{lvl['stats']['shape']:18s}, Quality {lvl['stats']['quality_score']:.1f}")
    print()
    
    # Shape distribution
    shapes = {}
    for lvl in levels:
        shape = lvl['stats']['shape']
        shapes[shape] = shapes.get(shape, 0) + 1
    
    print("Shape Distribution:")
    for shape, count in sorted(shapes.items()):
        print(f"  {shape:20s}: {count} ({count/len(levels)*100:.1f}%)")
    print()
