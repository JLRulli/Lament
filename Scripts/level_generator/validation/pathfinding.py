"""
A* Pathfinding for platformer level validation

Checks if entrance can reach exit considering platformer movement rules.
"""
import heapq
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tile_constants import EMPTY, GROUND, WALL, PLATFORM_ONEWAY, SPIKE, is_solid, is_platform
import config


class Node:
    """Node for A* pathfinding"""
    
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g  # Cost from start
        self.h = h  # Heuristic to goal
        self.f = g + h  # Total cost
        self.parent = parent
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))


def manhattan_distance(x1, y1, x2, y2):
    """Calculate Manhattan distance heuristic"""
    return abs(x1 - x2) + abs(y1 - y2)


def is_standing_on_solid(room, x, y):
    """Check if position (x, y) has solid ground below"""
    if y + 1 >= room.height:
        return False
    
    tile_below = room.get_tile(x, y + 1)
    return tile_below in [GROUND, WALL, PLATFORM_ONEWAY]


def can_stand_at(room, x, y):
    """
    Check if player can stand at position (x, y)
    
    Player collision model (Week 4):
    Coordinate system: Y=0 is TOP of room, Y=height-1 is BOTTOM
    - y: feet position
    - y-1, y-2: body (extends UPWARD from feet)
    - y+1: ground below feet (extends DOWNWARD)
    
    Total: 3 tiles of vertical clearance needed (y-2, y-1, y)
    
    Args:
        room: RoomTemplate
        x: X position (feet)
        y: Y position (feet)
    
    Returns:
        bool: True if player can stand at this position
    """
    # Check bounds for full player height (extends upward from y)
    if not (0 <= x < room.width):
        return False
    if y - config.PLAYER_HEIGHT < 0 or y >= room.height:  # Need headroom above
        return False
    
    # Check that 3 tiles of body space are passable (y, y-1, y-2)
    # This is feet + 2 body tiles extending UPWARD
    for dy in range(config.PLAYER_TOTAL_HEIGHT):
        check_y = y - dy  # Go UPWARD (toward y=0)
        if check_y < 0:
            return False
        
        tile = room.get_tile(x, check_y)
        
        # Solid tiles (GROUND, WALL) block player body
        if tile in [GROUND, WALL]:
            return False
        
        # PLATFORM_ONEWAY: Can pass through when jumping up from below
        # For now, treat as passable in body space
        # (player can jump through platforms from below)
    
    # Must have solid ground below feet (at y+1, going DOWNWARD)
    if y + 1 >= room.height:
        return False
    tile_below = room.get_tile(x, y + 1)
    return tile_below in [GROUND, WALL, PLATFORM_ONEWAY]


def check_jump_arc_clearance(room, start_x, start_y, end_x, end_y):
    """
    Check if jump arc has sufficient headroom (Week 4)
    
    Validates that player won't hit their head during jump.
    Samples points along parabolic arc and checks 3-tile clearance.
    
    Args:
        room: RoomTemplate
        start_x, start_y: Jump start position (feet)
        end_x, end_y: Jump end position (feet)
    
    Returns:
        bool: True if jump has clearance
    """
    # For platformer jumps, apex is roughly at horizontal midpoint
    mid_x = (start_x + end_x) // 2
    
    # Vertical jump height - apex is highest point
    if end_y < start_y:  # Jumping up
        apex_y = end_y
    else:  # Jumping down or level
        # Assume player jumps slightly up first
        apex_y = min(start_y, end_y) - 1
    
    # Check clearance at apex (most restrictive point)
    for check_y in range(apex_y, min(apex_y + config.PLAYER_TOTAL_HEIGHT, room.height)):
        if check_y < 0:
            continue
        if mid_x < 0 or mid_x >= room.width:
            continue
        
        tile = room.get_tile(mid_x, check_y)
        
        # Solid tiles block jump arc
        if tile in [GROUND, WALL]:
            return False
        
        # One-way platforms: Can jump through from below
        # So only block if we're descending onto them
        if tile == PLATFORM_ONEWAY:
            if apex_y >= start_y:  # Descending
                return False
    
    return True


def get_neighbors(room, node, max_jump_horizontal=5, max_jump_vertical=4):
    """
    Get all reachable neighbors from current node
    
    Improved movement rules for platformer:
    - Walk left/right (if on ground)
    - Jump in arc patterns (more realistic)
    - Fall down with gravity
    - Traverse slopes
    """
    neighbors = []
    x, y = node.x, node.y
    
    # Check if we're at a valid standing position
    on_ground = is_standing_on_solid(room, x, y)
    
    if not on_ground:
        # If in mid-air, can only fall
        fall_y = y
        while fall_y < room.height - 1:
            fall_y += 1
            tile_below = room.get_tile(x, fall_y + 1) if fall_y + 1 < room.height else None
            if tile_below in [GROUND, WALL, PLATFORM_ONEWAY]:
                if can_stand_at(room, x, fall_y):
                    neighbors.append((x, fall_y, 1))
                break
        return neighbors
    
    # 1. Walk left/right (cost 1)
    for dx in [-1, 1]:
        nx = x + dx
        if can_stand_at(room, nx, y):
            neighbors.append((nx, y, 1))
        
        # Also try walking down slopes (one tile diagonal)
        if can_stand_at(room, nx, y + 1):
            neighbors.append((nx, y + 1, 1))
    
    # 2. Jump mechanics - more lenient rules
    # Players can jump up to max_jump_horizontal horizontally and max_jump_vertical vertically
    # Use realistic arc patterns instead of all combinations
    
    for dx in range(-max_jump_horizontal, max_jump_horizontal + 1):
        if dx == 0:
            continue
        
        # For each horizontal distance, calculate reasonable vertical distances
        # Shorter horizontal jumps can go higher
        # Longer horizontal jumps tend to be flatter
        
        abs_dx = abs(dx)
        
        # Can jump up when moving shorter distances
        if abs_dx <= 2:
            vertical_range = range(-max_jump_vertical, 2)  # Can jump high on short hops
        elif abs_dx <= 4:
            vertical_range = range(-2, 2)  # Medium jumps are flatter
        else:
            vertical_range = range(-1, 3)  # Long jumps can only go slightly up or fall
        
        for dy in vertical_range:
            nx = x + dx
            ny = y + dy
            
            # Check landing position
            if 0 <= nx < room.width and 0 <= ny < room.height:
                # Check if we can land here
                tile_at = room.get_tile(nx, ny)
                if tile_at in [GROUND, WALL]:
                    continue  # Can't land inside solid tile
                
                # Check if there's ground below to land on
                if ny + 1 < room.height:
                    tile_below = room.get_tile(nx, ny + 1)
                    if tile_below in [GROUND, WALL, PLATFORM_ONEWAY]:
                        # Check if player can stand at landing position (3-tile clearance)
                        if can_stand_at(room, nx, ny):
                            # Check jump arc clearance (Week 4)
                            if check_jump_arc_clearance(room, x, y, nx, ny):
                                # Valid landing spot with clearance
                                cost = max(abs(dx), abs(dy))  # Chebyshev distance
                                neighbors.append((nx, ny, cost))
    
    # 3. Fall straight down
    fall_y = y
    while fall_y < room.height - 1:
        fall_y += 1
        if is_standing_on_solid(room, x, fall_y):
            if can_stand_at(room, x, fall_y):
                neighbors.append((x, fall_y, 1))
            break
    
    # 4. Climb up slopes (if current tile or adjacent is a slope)
    from utils.tile_constants import is_slope
    current_tile = room.get_tile(x, y)
    if is_slope(current_tile) or is_slope(room.get_tile(x, y + 1) if y + 1 < room.height else EMPTY):
        # Can move diagonally when on/near slopes
        for dx in [-1, 1]:
            for dy in [-1, 0]:  # Can climb up or stay level
                nx, ny = x + dx, y + dy
                if 0 <= nx < room.width and 0 <= ny < room.height:
                    if can_stand_at(room, nx, ny):
                        neighbors.append((nx, ny, 1))
    
    return neighbors


def astar(room, start, goal, max_jump_horizontal=None, max_jump_vertical=None):
    """
    A* pathfinding for platformer movement
    
    Args:
        room: RoomTemplate
        start: (x, y) tuple for start position
        goal: (x, y) tuple for goal position
        max_jump_horizontal: Max horizontal jump distance (default from config)
        max_jump_vertical: Max vertical jump height (default from config)
    
    Returns:
        List of (x, y) positions if path exists, None otherwise
    """
    if max_jump_horizontal is None:
        max_jump_horizontal = config.MAX_JUMP_DISTANCE
    if max_jump_vertical is None:
        max_jump_vertical = config.MAX_JUMP_HEIGHT
    
    start_x, start_y = start
    goal_x, goal_y = goal
    
    # Improved door position handling - find nearest valid standing position
    def find_nearest_standing_position(px, py, max_search=10):
        """
        Find nearest valid standing position from a point
        
        Platformer-aware search prioritizes vertical then horizontal
        """
        # First check if current position is valid
        if can_stand_at(room, px, py):
            return (px, py)
        
        # Strategy 1: Search vertically - player might be IN ground, try above/below
        for dy in range(-5, 6):
            test_y = py + dy
            if 0 <= test_y < room.height and can_stand_at(room, px, test_y):
                return (px, test_y)
        
        # Strategy 2: Search horizontally at similar Y levels
        for dx in range(1, max_search):
            for direction in [1, -1]:
                test_x = px + (dx * direction)
                if 0 <= test_x < room.width:
                    # Try this X at various Y levels
                    for dy in range(-4, 5):
                        test_y = py + dy
                        if 0 <= test_y < room.height and can_stand_at(room, test_x, test_y):
                            return (test_x, test_y)
        
        # Last resort: find ANY valid position in the room
        for y in range(room.height):
            for x in range(room.width):
                if can_stand_at(room, x, y):
                    return (x, y)
        
        return None
    
    # Find valid positions near doors
    start_pos = find_nearest_standing_position(start_x, start_y)
    goal_pos = find_nearest_standing_position(goal_x, goal_y)
    
    # DEBUG: Uncomment to see door position finding
    #import sys
    #print(f'DEBUG: Doors at ({start}, {goal}) -> positions ({start_pos}, {goal_pos})', file=sys.stderr)
    
    if not start_pos:
        return None  # No valid standing position near entrance
    if not goal_pos:
        return None  # No valid standing position near exit
    
    start_x, start_y = start_pos
    goal_x, goal_y = goal_pos
    
    # Initialize open and closed sets
    open_set = []
    closed_set = set()
    
    # Create start node
    h = manhattan_distance(start_x, start_y, goal_x, goal_y)
    start_node = Node(start_x, start_y, 0, h)
    
    heapq.heappush(open_set, start_node)
    
    # Track best g-score for each position
    g_scores = {(start_x, start_y): 0}
    
    # A* main loop
    iterations = 0
    max_iterations = room.width * room.height * 2  # Prevent infinite loops
    
    while open_set and iterations < max_iterations:
        iterations += 1
        
        # Get node with lowest f-score
        current = heapq.heappop(open_set)
        
        # Check if we reached goal
        if current.x == goal_x and current.y == goal_y:
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append((node.x, node.y))
                node = node.parent
            return list(reversed(path))
        
        # Mark as visited
        closed_set.add((current.x, current.y))
        
        # Explore neighbors
        for nx, ny, move_cost in get_neighbors(room, current, max_jump_horizontal, max_jump_vertical):
            if (nx, ny) in closed_set:
                continue
            
            # Calculate new g-score
            tentative_g = current.g + move_cost
            
            # Check if this is a better path
            if (nx, ny) not in g_scores or tentative_g < g_scores[(nx, ny)]:
                g_scores[(nx, ny)] = tentative_g
                h = manhattan_distance(nx, ny, goal_x, goal_y)
                neighbor_node = Node(nx, ny, tentative_g, h, current)
                heapq.heappush(open_set, neighbor_node)
    
    # No path found
    return None


def has_path(room, start, goal):
    """
    Simple boolean check if path exists
    
    Returns:
        bool: True if path exists, False otherwise
    """
    return astar(room, start, goal) is not None
