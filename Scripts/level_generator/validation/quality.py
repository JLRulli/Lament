"""
Quality scoring system for room templates

Scores rooms on multiple dimensions beyond just playable/unplayable.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tile_constants import EMPTY, GROUND, WALL, PLATFORM_ONEWAY, SPIKE, is_slope
from collections import Counter


def score_room_quality(room, validation_results):
    """
    Comprehensive quality scoring for a room
    
    Args:
        room: RoomTemplate
        validation_results: Results from validation
    
    Returns:
        dict: Quality scores in multiple dimensions
    """
    scores = {
        'variety': score_variety(room),
        'flow': score_flow(room, validation_results),
        'balance': score_balance(room),
        'visual_interest': score_visual_interest(room),
        'overall': 0.0
    }
    
    # Calculate overall score (weighted average)
    weights = {
        'variety': 0.25,
        'flow': 0.35,
        'balance': 0.25,
        'visual_interest': 0.15
    }
    
    scores['overall'] = sum(scores[key] * weights[key] for key in weights)
    
    # Add quality tier
    overall = scores['overall']
    if overall >= 8.0:
        scores['quality_tier'] = 'EXCELLENT'
    elif overall >= 6.5:
        scores['quality_tier'] = 'GOOD'
    elif overall >= 5.0:
        scores['quality_tier'] = 'ACCEPTABLE'
    elif overall >= 3.0:
        scores['quality_tier'] = 'POOR'
    else:
        scores['quality_tier'] = 'BAD'
    
    return scores


def score_variety(room):
    """
    Score platform variety and obstacle distribution
    
    Looks for:
    - Different platform heights
    - Varied gap widths
    - Mixed obstacle types
    
    Returns:
        float: Score from 0-10
    """
    score = 5.0  # Start at middle
    
    # Count platform heights
    platform_heights = set()
    for y in range(room.height):
        for x in range(room.width):
            if room.get_tile(x, y) == PLATFORM_ONEWAY:
                platform_heights.add(y)
    
    # More variety in platform heights is better
    height_count = len(platform_heights)
    if height_count >= 5:
        score += 2.0
    elif height_count >= 3:
        score += 1.0
    elif height_count <= 1:
        score -= 2.0
    
    # Check tile type diversity
    tile_types = set()
    for y in range(room.height):
        for x in range(room.width):
            tile = room.get_tile(x, y)
            if tile != EMPTY:
                tile_types.add(tile)
    
    # More tile types = more variety
    type_count = len(tile_types)
    if type_count >= 5:
        score += 2.0
    elif type_count >= 3:
        score += 1.0
    elif type_count <= 2:
        score -= 1.0
    
    # Check for slopes (adds variety)
    has_slopes = False
    for y in range(room.height):
        for x in range(room.width):
            if is_slope(room.get_tile(x, y)):
                has_slopes = True
                break
        if has_slopes:
            break
    
    if has_slopes:
        score += 1.0
    
    return max(0.0, min(10.0, score))


def score_flow(room, validation_results):
    """
    Score pacing and risk/reward balance
    
    Looks for:
    - Good path length (not too short, not too long)
    - Balanced challenge progression
    - Safe zones after difficult sections
    
    Returns:
        float: Score from 0-10
    """
    score = 5.0
    
    # Path length consideration
    if 'path_length' in validation_results:
        path_len = validation_results['path_length']
        expected_len = room.width * 0.8  # Expect path to use most of room width
        
        ratio = path_len / expected_len if expected_len > 0 else 0
        
        if 0.7 <= ratio <= 1.3:  # Good path length
            score += 2.0
        elif 0.5 <= ratio <= 1.5:  # Acceptable
            score += 1.0
        else:  # Too short or too long
            score -= 1.0
    
    # Spike density - should be challenging but not overwhelming
    spike_count = validation_results.get('spike_count', 0)
    total_tiles = room.width * room.height
    spike_density = spike_count / total_tiles if total_tiles > 0 else 0
    
    if 0.03 <= spike_density <= 0.08:  # Sweet spot
        score += 1.5
    elif spike_density < 0.02:  # Too easy
        score -= 0.5
    elif spike_density > 0.15:  # Too deadly
        score -= 2.0
    
    # Platform density - need enough rest points
    platform_count = validation_results.get('platform_count', 0)
    if room.shape_type in ['horizontal_right', 'horizontal_left']:
        expected_platforms = room.width / 4
    elif room.shape_type in ['vertical_up', 'vertical_down']:
        expected_platforms = room.height / 3
    else:  # box
        expected_platforms = max(room.width, room.height) / 4
    
    platform_ratio = platform_count / expected_platforms if expected_platforms > 0 else 0
    
    if 0.8 <= platform_ratio <= 1.5:
        score += 1.5
    elif platform_ratio < 0.5:
        score -= 1.0
    
    return max(0.0, min(10.0, score))


def score_balance(room):
    """
    Score overall balance of difficulty elements
    
    Looks for:
    - Not too crowded, not too empty
    - Reasonable obstacle placement
    - Symmetry where appropriate
    
    Returns:
        float: Score from 0-10
    """
    score = 5.0
    
    # Calculate empty space ratio
    empty_count = 0
    total_tiles = room.width * room.height
    
    for y in range(room.height):
        for x in range(room.width):
            if room.get_tile(x, y) == EMPTY:
                empty_count += 1
    
    empty_ratio = empty_count / total_tiles if total_tiles > 0 else 0
    
    # Sweet spot: 40-70% empty (allows movement but has structure)
    if 0.4 <= empty_ratio <= 0.7:
        score += 2.0
    elif 0.3 <= empty_ratio <= 0.8:
        score += 1.0
    elif empty_ratio < 0.2 or empty_ratio > 0.9:
        score -= 2.0
    
    # Check for clustering of hazards (bad)
    spike_clusters = count_spike_clusters(room)
    if spike_clusters == 0:
        score += 1.0  # No spikes or well-distributed
    elif spike_clusters <= 2:
        score += 0.5  # Some clustering is OK
    else:
        score -= 1.0  # Too much clustering
    
    return max(0.0, min(10.0, score))


def score_visual_interest(room):
    """
    Score visual variety and aesthetics
    
    Looks for:
    - Varied shapes and patterns
    - Non-repetitive layouts
    - Interesting silhouette
    
    Returns:
        float: Score from 0-10
    """
    score = 5.0
    
    # Check for repetitive patterns (bad)
    has_repetition = check_repetition(room)
    if not has_repetition:
        score += 2.0
    else:
        score -= 1.0
    
    # Check for vertical variety (platforms at different heights)
    vertical_levels = count_vertical_levels(room)
    if vertical_levels >= 4:
        score += 2.0
    elif vertical_levels >= 2:
        score += 1.0
    else:
        score -= 1.0
    
    # Check for interesting shapes (not just flat floor)
    has_interesting_shapes = check_for_interesting_shapes(room)
    if has_interesting_shapes:
        score += 1.0
    
    return max(0.0, min(10.0, score))


def count_spike_clusters(room):
    """Count groups of 3+ adjacent spikes (indicates poor distribution)"""
    visited = set()
    cluster_count = 0
    
    def flood_fill(x, y):
        """Count connected spikes"""
        if (x, y) in visited:
            return 0
        if not (0 <= x < room.width and 0 <= y < room.height):
            return 0
        if room.get_tile(x, y) != SPIKE:
            return 0
        
        visited.add((x, y))
        count = 1
        
        # Check 4-connected neighbors
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            count += flood_fill(x + dx, y + dy)
        
        return count
    
    for y in range(room.height):
        for x in range(room.width):
            if room.get_tile(x, y) == SPIKE and (x, y) not in visited:
                cluster_size = flood_fill(x, y)
                if cluster_size >= 3:
                    cluster_count += 1
    
    return cluster_count


def check_repetition(room):
    """Check if room has repetitive 3x3 patterns"""
    # Sample 3x3 patterns
    patterns = []
    
    for y in range(room.height - 2):
        for x in range(room.width - 2):
            pattern = tuple(
                room.get_tile(x + dx, y + dy)
                for dy in range(3)
                for dx in range(3)
            )
            patterns.append(pattern)
    
    # Count pattern frequency
    pattern_counts = Counter(patterns)
    
    # If any pattern appears more than 3 times, it's repetitive
    max_count = max(pattern_counts.values()) if pattern_counts else 0
    return max_count > 3


def count_vertical_levels(room):
    """Count distinct horizontal platforms/floors"""
    levels = set()
    
    for y in range(room.height):
        has_solid = False
        for x in range(room.width):
            tile = room.get_tile(x, y)
            if tile in [GROUND, PLATFORM_ONEWAY]:
                has_solid = True
                break
        if has_solid:
            levels.add(y)
    
    return len(levels)


def check_for_interesting_shapes(room):
    """Check if room has slopes, elevated platforms, or other non-flat features"""
    has_slopes = False
    has_elevated_platforms = False
    
    floor_y = room.height - 2
    
    for y in range(room.height):
        for x in range(room.width):
            tile = room.get_tile(x, y)
            
            if is_slope(tile):
                has_slopes = True
            
            if tile == PLATFORM_ONEWAY and y < floor_y - 2:
                has_elevated_platforms = True
    
    return has_slopes or has_elevated_platforms
