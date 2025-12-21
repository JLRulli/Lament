"""
Simplified validator for Week 2/3

Shape-aware validation with basic checks + optional A* pathfinding.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tile_constants import EMPTY, GROUND, WALL, PLATFORM_ONEWAY, SPIKE, is_slope
import config


def validate_room_simple(room, use_pathfinding=False):
    """
    Validation with optional A* pathfinding
    
    Args:
        room: RoomTemplate to validate
        use_pathfinding: If True, use A* pathfinding for reachability (Week 3)
                        If False, use heuristic checks (Week 2)
    
    Returns:
        dict: Validation results with tier
    """
    results = {
        "valid": True,
        "tier": "NORMAL",
        "errors": [],
        "warnings": [],
        "max_gap_width": 0,
        "spike_count": 0,
        "platform_count": 0,
        "floor_coverage": 0.0,
        "path_found": None,
        "path_length": 0
    }
    
    # Count tiles
    results["spike_count"] = count_tiles(room, SPIKE)
    results["platform_count"] = count_tiles(room, PLATFORM_ONEWAY)
    
    # Check platform spacing (Week 4)
    spacing_valid, spacing_errors = check_platform_spacing(room)
    if not spacing_valid:
        results["valid"] = False
        results["tier"] = "IMPOSSIBLE"
        results["errors"].extend(spacing_errors)
        return results
    
    # Optional: A* pathfinding validation (Week 3)
    if use_pathfinding:
        path_valid = check_pathfinding(room, results)
        if not path_valid:
            results["valid"] = False
            results["tier"] = "IMPOSSIBLE"
            return results
    
    # Shape-specific validation
    if room.shape_type in ["horizontal_right", "horizontal_left"]:
        return validate_horizontal(room, results)
    elif room.shape_type in ["vertical_up", "vertical_down"]:
        return validate_vertical(room, results)
    elif room.shape_type == "box":
        return validate_box(room, results)
    else:
        # Unknown shape, use generic
        return validate_horizontal(room, results)


def check_platform_spacing(room):
    """
    Verify platforms don't violate MIN_PLATFORM_VERTICAL_SPACING
    
    Checks that platforms have sufficient vertical spacing (4 tiles minimum)
    to allow player (2 tiles tall + 1 tile headroom) to fit.
    
    Args:
        room: RoomTemplate to validate
    
    Returns:
        tuple: (is_valid: bool, errors: list)
    """
    errors = []
    
    # Find all platforms and ground tiles
    solid_positions = set()
    for y in range(room.height):
        for x in range(room.width):
            tile = room.get_tile(x, y)
            if tile in [GROUND, WALL, PLATFORM_ONEWAY]:
                solid_positions.add((x, y))
    
    # Check each solid tile for spacing violations
    # Y=0 is TOP, Y=height-1 is BOTTOM
    # Floor level is typically at Y=height-2 (with wall boundary at height-1)
    floor_level = room.height - 2
    
    for x, y in solid_positions:
        tile = room.get_tile(x, y)
        
        # Only check spacing for platforms and ground (not walls)
        if tile not in [GROUND, PLATFORM_ONEWAY]:
            continue
        
        # Skip boundary tiles (floor and walls) - only check interior platforms
        # Left wall: X=0, Right wall: X=width-1, Floor: Y>=floor_level
        if x == 0 or x == room.width - 1 or y >= floor_level:
            continue
        
        # Check if there's a solid tile within PLAYER_TOTAL_HEIGHT above this tile
        # Player needs PLAYER_TOTAL_HEIGHT (3 tiles) of clearance ABOVE the platform
        for dy in range(1, config.PLAYER_TOTAL_HEIGHT + 1):
            check_y = y - dy  # Going UPWARD (toward Y=0)
            
            if check_y < 0:
                break  # Hit top of room, no violation
            
            check_tile = room.get_tile(x, check_y)
            if check_tile in [GROUND, WALL, PLATFORM_ONEWAY]:
                # Found a solid tile too close above
                if dy < config.PLAYER_TOTAL_HEIGHT:
                    errors.append(
                        f"Insufficient vertical spacing at ({x},{y}): "
                        f"only {dy} tiles clearance (need {config.PLAYER_TOTAL_HEIGHT})"
                    )
                break
    
    return len(errors) == 0, errors


def check_pathfinding(room, results):
    """
    Use A* pathfinding to check if entrance can reach exit
    
    Args:
        room: RoomTemplate
        results: Results dict to populate
    
    Returns:
        bool: True if path exists
    """
    try:
        from validation.pathfinding import astar
        
        entrance = room.connections.get("entrance")
        exit_door = room.connections.get("exit")
        
        if not entrance or not exit_door:
            results["errors"].append("Missing entrance or exit")
            return False
        
        start = (entrance["position"]["x"], entrance["position"]["y"])
        goal = (exit_door["position"]["x"], exit_door["position"]["y"])
        
        path = astar(room, start, goal)
        
        if path is None:
            results["errors"].append("No path from entrance to exit")
            results["path_found"] = False
            return False
        
        results["path_found"] = True
        results["path_length"] = len(path)
        
        # Longer paths might indicate more challenging rooms
        if len(path) > room.width * 2:
            results["warnings"].append(f"Very long path: {len(path)} steps")
        
        return True
    
    except Exception as e:
        # If pathfinding fails for any reason, fall back to heuristic
        results["warnings"].append(f"Pathfinding error: {e}")
        return True  # Don't fail room just because pathfinding errored


def validate_horizontal(room, results):
    """Validate horizontal progression rooms"""
    floor_y = room.height - 2
    ground_count = 0
    for x in range(room.width):
        tile = room.get_tile(x, floor_y)
        if tile in [GROUND, PLATFORM_ONEWAY]:
            ground_count += 1
    
    results["floor_coverage"] = ground_count / room.width if room.width > 0 else 0
    
    # Check floor coverage
    if results["floor_coverage"] < 0.25:
        results["valid"] = False
        results["tier"] = "IMPOSSIBLE"
        results["errors"].append(f"Insufficient floor: {results['floor_coverage']:.1%}")
        return results
    
    # Check gaps
    max_gap = check_gaps_at_level(room, floor_y, results)
    results["max_gap_width"] = max_gap
    
    if not results["valid"]:
        return results
    
    # Calculate tier
    results["tier"] = calculate_tier_simple(results)
    return results


def validate_vertical(room, results):
    """Validate vertical climbing rooms"""
    # For vertical rooms, check that there are enough platforms/walls to climb
    wall_coverage = 0
    platform_count = 0
    
    for y in range(room.height):
        for x in range(room.width):
            tile = room.get_tile(x, y)
            if tile == WALL:
                wall_coverage += 1
            elif tile == PLATFORM_ONEWAY:
                platform_count += 1
    
    total_tiles = room.width * room.height
    wall_pct = wall_coverage / total_tiles if total_tiles > 0 else 0
    
    # Vertical rooms need walls to climb and platforms to rest
    if wall_pct < 0.1:
        results["valid"] = False
        results["tier"] = "IMPOSSIBLE"
        results["errors"].append(f"Insufficient walls for climbing: {wall_pct:.1%}")
        return results
    
    if platform_count < 2:
        results["warnings"].append("Very few rest platforms")
    
    results["platform_count"] = platform_count
    results["floor_coverage"] = wall_pct  # Reuse field for wall coverage
    
    # Calculate tier
    results["tier"] = calculate_tier_simple(results)
    return results


def validate_box(room, results):
    """Validate box arena rooms"""
    # For arenas, just check that there are some platforms and it's not too deadly
    platform_count = count_tiles(room, PLATFORM_ONEWAY)
    ground_count = count_tiles(room, GROUND)
    
    total_solid = platform_count + ground_count
    total_tiles = room.width * room.height
    
    coverage = total_solid / total_tiles if total_tiles > 0 else 0
    
    if coverage < 0.05:
        results["valid"] = False
        results["tier"] = "IMPOSSIBLE"
        results["errors"].append("Insufficient platforms in arena")
        return results
    
    results["platform_count"] = platform_count
    results["floor_coverage"] = coverage
    
    # Calculate tier
    results["tier"] = calculate_tier_simple(results)
    return results


def check_gaps_at_level(room, y, results):
    """Check gaps at specific Y level"""
    max_gap = 0
    gap_start = None
    
    for x in range(room.width + 1):
        if x < room.width:
            tile = room.get_tile(x, y)
            is_gap = tile == EMPTY
        else:
            is_gap = False
        
        if is_gap:
            if gap_start is None:
                gap_start = x
        else:
            if gap_start is not None:
                gap_width = x - gap_start
                max_gap = max(max_gap, gap_width)
                
                if gap_width > config.MAX_JUMP_DISTANCE:
                    results["valid"] = False
                    results["tier"] = "IMPOSSIBLE"
                    results["errors"].append(f"Impossible gap: {gap_width} tiles")
                    return max_gap
                elif gap_width >= config.MAX_JUMP_DISTANCE - 1:
                    results["warnings"].append(f"Challenging gap: {gap_width} tiles")
                
                gap_start = None
    
    return max_gap


def count_tiles(room, tile_type):
    """Count tiles of given type"""
    count = 0
    for y in range(room.height):
        for x in range(room.width):
            if room.get_tile(x, y) == tile_type:
                count += 1
    return count


def calculate_tier_simple(results):
    """Calculate difficulty tier from validation results"""
    if not results["valid"]:
        return "IMPOSSIBLE"
    
    score = 0
    
    # Factor: Gap width
    if results["max_gap_width"] >= 5:
        score += 3
    elif results["max_gap_width"] >= 4:
        score += 2
    elif results["max_gap_width"] >= 3:
        score += 1
    
    # Factor: Spike count
    if results["spike_count"] >= 15:
        score += 3
    elif results["spike_count"] >= 8:
        score += 2
    elif results["spike_count"] >= 4:
        score += 1
    
    # Factor: Platform availability (inverse)
    if results["platform_count"] < 2:
        score += 2
    elif results["platform_count"] < 4:
        score += 1
    
    # Factor: Floor/wall coverage (inverse)
    if results["floor_coverage"] < 0.4:
        score += 2
    elif results["floor_coverage"] < 0.6:
        score += 1
    
    # Map to tier
    if score >= 7:
        return "EXPERT"
    elif score >= 4:
        return "HARD"
    elif score >= 2:
        return "NORMAL"
    else:
        return "EASY"
