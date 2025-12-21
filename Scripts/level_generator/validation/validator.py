"""
Room validation system

Validates room templates for playability and assigns difficulty tiers.
"""
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tile_constants import EMPTY, GROUND, WALL, PLATFORM_ONEWAY, SPIKE, is_solid, is_slope
from validation.pathfinding import astar, has_path
import config


def validate_room(room):
    """
    Complete validation of room template
    
    Returns:
        dict: Validation results with tier assignment
    """
    results = {
        "valid": True,
        "tier": "NORMAL",
        "errors": [],
        "warnings": [],
        "max_gap_width": 0,
        "spike_count": 0,
        "platform_count": 0,
        "reachable": False
    }
    
    # Check 1: Reachability (entrance → exit)
    # NOTE: Using simple heuristic for Week 2 (A* needs more tuning)
    reachable, reason = check_reachability_simple(room)
    results["reachable"] = reachable
    if not reachable:
        results["errors"].append(f"Unreachable: {reason}")
        results["valid"] = False
        results["tier"] = "IMPOSSIBLE"
        return results
    
    # Check 2: Jump distances
    gaps_valid, gap_warnings, max_gap = check_jump_distances(room)
    results["max_gap_width"] = max_gap
    results["warnings"].extend(gap_warnings)
    if not gaps_valid:
        results["errors"].append("Impossible gaps detected")
        results["tier"] = "IMPOSSIBLE"
        return results
    
    # Check 3: Slope connections
    slopes_valid, slope_errors = check_slope_connections(room)
    if not slopes_valid:
        results["warnings"].extend(slope_errors)
    
    # Check 4: Spike fairness
    spikes_fair, spike_warnings, spike_count = check_spike_fairness(room)
    results["spike_count"] = spike_count
    results["warnings"].extend(spike_warnings)
    
    # Check 5: Count platforms
    results["platform_count"] = count_tiles(room, PLATFORM_ONEWAY)
    
    # Calculate difficulty tier
    results["tier"] = calculate_difficulty_tier(results)
    
    return results


def check_reachability_simple(room):
    """
    Simple heuristic check for reachability (not using A*)
    Week 2 simplified version - A* needs more tuning for Week 3
    
    Returns:
        (bool, str): (seems_reachable, reason)
    """
    entrance = room.connections.get("entrance")
    exit_door = room.connections.get("exit")
    
    if not entrance:
        return False, "No entrance door found"
    if not exit_door:
        return False, "No exit door found"
    
    # Simple heuristic: Check if there's enough floor coverage
    floor_y = room.height - 2
    ground_tiles = 0
    total_width = room.width
    
    for x in range(room.width):
        tile = room.get_tile(x, floor_y)
        if tile in [GROUND, PLATFORM_ONEWAY]:
            ground_tiles += 1
    
    coverage = ground_tiles / total_width if total_width > 0 else 0
    
    # If less than 30% floor coverage, probably impossible
    if coverage < 0.3:
        return False, f"Insufficient floor coverage: {coverage:.1%}"
    
    # Check that there are platforms near both doors
    entrance_x = entrance["position"]["x"]
    exit_x = exit_door["position"]["x"]
    
    # Check for platforms within 3 tiles of entrance
    has_platform_near_entrance = False
    for dx in range(-3, 4):
        x = entrance_x + dx
        if 0 <= x < room.width:
            tile = room.get_tile(x, floor_y)
            if tile in [GROUND, PLATFORM_ONEWAY]:
                has_platform_near_entrance = True
                break
    
    if not has_platform_near_entrance:
        return False, "No platform near entrance"
    
    # Check for platforms within 3 tiles of exit
    has_platform_near_exit = False
    for dx in range(-3, 4):
        x = exit_x + dx
        if 0 <= x < room.width:
            tile = room.get_tile(x, floor_y)
            if tile in [GROUND, PLATFORM_ONEWAY]:
                has_platform_near_exit = True
                break
    
    if not has_platform_near_exit:
        return False, "No platform near exit"
    
    return True, "Heuristic checks pass"


def check_reachability_astar(room):
    """
    Full A* pathfinding check for reachability
    TODO: Fix and enable in Week 3
    
    Returns:
        (bool, str): (is_reachable, reason)
    """
    entrance = room.connections.get("entrance")
    exit_door = room.connections.get("exit")
    
    if not entrance:
        return False, "No entrance door found"
    if not exit_door:
        return False, "No exit door found"
    
    start_x = entrance["position"]["x"]
    start_y = entrance["position"]["y"]
    goal_x = exit_door["position"]["x"]
    goal_y = exit_door["position"]["y"]
    
    # Find nearest valid standing position to entrance
    from validation.pathfinding import can_stand_at
    
    start = None
    for radius in range(5):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x, y = start_x + dx, start_y + dy
                if can_stand_at(room, x, y):
                    start = (x, y)
                    break
            if start:
                break
        if start:
            break
    
    if not start:
        return False, "No valid position near entrance"
    
    # Find nearest valid standing position to exit
    goal = None
    for radius in range(5):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x, y = goal_x + dx, goal_y + dy
                if can_stand_at(room, x, y):
                    goal = (x, y)
                    break
            if goal:
                break
        if goal:
            break
    
    if not goal:
        return False, "No valid position near exit"
    
    # Use A* pathfinding
    path = astar(room, start, goal)
    
    if path is None:
        return False, f"No path from {start} to {goal}"
    
    return True, f"Path exists ({len(path)} steps)"


def check_jump_distances(room, max_jump=None):
    """
    Check that all gaps are jumpable
    
    Only checks rows that have platforms (where players would walk)
    
    Returns:
        (bool, list, int): (all_valid, warnings, max_gap_width)
    """
    if max_jump is None:
        max_jump = config.MAX_JUMP_DISTANCE
    
    warnings = []
    max_gap_found = 0
    
    # Only scan rows that have some solid tiles (potential walking paths)
    for y in range(room.height):
        # Check if this row has any ground/platforms
        has_walkable = False
        for x in range(room.width):
            tile = room.get_tile(x, y + 1) if y + 1 < room.height else None
            if tile in [GROUND, WALL, PLATFORM_ONEWAY]:
                has_walkable = True
                break
        
        if not has_walkable:
            continue  # Skip empty rows
        
        # Scan for gaps in this row
        gap_start = None
        for x in range(room.width):
            tile = room.get_tile(x, y)
            
            is_empty = (tile == EMPTY or tile == SPIKE)
            
            if is_empty:
                if gap_start is None:
                    gap_start = x
            else:  # Solid tile
                if gap_start is not None:
                    gap_width = x - gap_start
                    max_gap_found = max(max_gap_found, gap_width)
                    
                    if gap_width > max_jump:
                        warnings.append(f"Impossible gap at row {y}, x={gap_start}: {gap_width} tiles (max: {max_jump})")
                        return False, warnings, gap_width
                    elif gap_width >= max_jump - 1:
                        warnings.append(f"Challenging gap at row {y}, x={gap_start}: {gap_width} tiles")
                    
                    gap_start = None
        
        # Check if row ended with a gap
        if gap_start is not None:
            gap_width = room.width - gap_start
            max_gap_found = max(max_gap_found, gap_width)
            if gap_width > max_jump:
                warnings.append(f"Impossible gap at row {y}, x={gap_start}: {gap_width} tiles (extends to edge)")
                return False, warnings, gap_width
    
    return True, warnings, max_gap_found


def check_slope_connections(room):
    """
    Validate slopes have proper connections
    
    Returns:
        (bool, list): (all_valid, errors)
    """
    errors = []
    
    for y in range(room.height):
        for x in range(room.width):
            tile = room.get_tile(x, y)
            
            if is_slope(tile):
                # Basic check: slopes should have some support
                # More detailed checks can be added later
                has_support = False
                
                # Check adjacent tiles for ground/platform
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < room.width and 0 <= ny < room.height:
                            neighbor = room.get_tile(nx, ny)
                            if neighbor in [GROUND, PLATFORM_ONEWAY]:
                                has_support = True
                                break
                
                if not has_support:
                    errors.append(f"Floating slope at ({x}, {y})")
    
    return len(errors) == 0, errors


def check_spike_fairness(room):
    """
    Check for unavoidable spike scenarios
    
    Returns:
        (bool, list, int): (is_fair, warnings, spike_count)
    """
    warnings = []
    spike_count = count_tiles(room, SPIKE)
    
    # For now, just count and warn if excessive
    # Future: check for unavoidable spikes in critical path
    
    total_tiles = room.width * room.height
    spike_density = spike_count / total_tiles if total_tiles > 0 else 0
    
    if spike_density > 0.15:  # More than 15% spikes
        warnings.append(f"Very high spike density: {spike_density:.1%}")
    elif spike_density > 0.10:
        warnings.append(f"High spike density: {spike_density:.1%}")
    
    return True, warnings, spike_count


def count_tiles(room, tile_type):
    """Count how many tiles of given type exist in room"""
    count = 0
    for y in range(room.height):
        for x in range(room.width):
            if room.get_tile(x, y) == tile_type:
                count += 1
    return count


def calculate_difficulty_tier(validation_results):
    """
    Assign difficulty tier based on validation results
    
    Tiers:
    - IMPOSSIBLE: No path exists, impossible gaps
    - EXPERT: Very challenging (5-tile jumps, high spike density)
    - HARD: Challenging but fair (4-tile jumps, moderate spikes)
    - NORMAL: Moderate challenge (3-tile jumps, some hazards)
    - EASY: Generous spacing, few hazards
    
    Returns:
        str: Tier name
    """
    # Already marked as impossible
    if not validation_results["valid"]:
        return "IMPOSSIBLE"
    
    if not validation_results["reachable"]:
        return "IMPOSSIBLE"
    
    # Score based on multiple factors
    score = 0
    
    # Factor 1: Max gap width
    max_gap = validation_results["max_gap_width"]
    if max_gap >= 5:
        score += 3
    elif max_gap >= 4:
        score += 2
    elif max_gap >= 3:
        score += 1
    
    # Factor 2: Spike density
    spike_count = validation_results["spike_count"]
    if spike_count >= 20:
        score += 3
    elif spike_count >= 10:
        score += 2
    elif spike_count >= 5:
        score += 1
    
    # Factor 3: Platform availability (inverse)
    platform_count = validation_results["platform_count"]
    if platform_count < 2:
        score += 2
    elif platform_count < 4:
        score += 1
    
    # Factor 4: Warnings
    warning_count = len(validation_results["warnings"])
    if warning_count >= 5:
        score += 2
    elif warning_count >= 3:
        score += 1
    
    # Map score to tier
    if score >= 8:
        return "EXPERT"
    elif score >= 5:
        return "HARD"
    elif score >= 2:
        return "NORMAL"
    else:
        return "EASY"
