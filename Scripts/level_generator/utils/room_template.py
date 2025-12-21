"""
RoomTemplate class - Core data structure for room generation
"""
import copy
import uuid
from typing import List, Dict, Any, Tuple, Optional


class RoomTemplate:
    """
    Represents a single room template with tilemap and metadata
    """
    
    def __init__(self, width: int, height: int, shape_type: str = "horizontal_right"):
        """
        Initialize a new RoomTemplate
        
        Args:
            width: Room width in tiles
            height: Room height in tiles
            shape_type: Type of room shape (horizontal_right, vertical_up, box, etc.)
        """
        self.id = self._generate_id()
        self.width = width
        self.height = height
        self.shape_type = shape_type
        
        # Initialize empty tilemap (2D array)
        self.tiles = [[0] * width for _ in range(height)]
        
        # Metadata
        self.metadata = {
            "difficulty": 1,
            "length": "medium",
            "tags": [],
            "author": "procedural_gen",
            "version": "1.0"
        }
        
        # Entry/exit connections
        self.connections = {}
        
        # Spawn zones for entities
        self.spawn_zones = {
            "enemies": [],
            "obstacles": []
        }
        
        # Validation results (populated later in Week 2)
        self.validation = {
            "valid": False,
            "errors": [],
            "warnings": []
        }
    
    def _generate_id(self) -> str:
        """Generate unique ID for this template"""
        return str(uuid.uuid4())[:8]
    
    def set_tile(self, x: int, y: int, tile_id: int) -> None:
        """
        Set tile at position (x, y)
        
        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
            tile_id: Tile type ID
        
        Raises:
            ValueError: If position is out of bounds
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile_id
        else:
            raise ValueError(f"Position ({x}, {y}) out of bounds for room size {self.width}x{self.height}")
    
    def get_tile(self, x: int, y: int) -> Optional[int]:
        """
        Get tile at position (x, y)
        
        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
        
        Returns:
            Tile ID at position, or None if out of bounds
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None
    
    def add_connection(self, name: str, x: int, y: int, direction: str) -> None:
        """
        Add entry/exit door connection
        
        Args:
            name: Connection name (e.g., "entrance", "exit")
            x: X coordinate
            y: Y coordinate
            direction: Direction door faces ("left", "right", "up", "down")
        """
        self.connections[name] = {
            "position": {"x": x, "y": y},
            "direction": direction,
            "type": "door"
        }
    
    def add_enemy_zone(self, x: int, y: int, zone_type: str = "ground", 
                       allowed_enemies: Optional[List[str]] = None) -> None:
        """
        Add enemy spawn zone
        
        Args:
            x: X coordinate
            y: Y coordinate
            zone_type: Type of spawn zone ("ground", "aerial", "wall")
            allowed_enemies: List of enemy types allowed in this zone
        """
        if allowed_enemies is None:
            allowed_enemies = ["light_flyer", "medium_walker"]
        
        self.spawn_zones["enemies"].append({
            "id": f"zone_{len(self.spawn_zones['enemies'])}",
            "position": {"x": x, "y": y},
            "type": zone_type,
            "allowed_enemies": allowed_enemies
        })
    
    def add_obstacle_slot(self, x: int, y: int, allowed_types: Optional[List[str]] = None) -> None:
        """
        Add obstacle placement slot
        
        Args:
            x: X coordinate
            y: Y coordinate
            allowed_types: List of obstacle types allowed in this slot
        """
        if allowed_types is None:
            allowed_types = ["spike", "moving_platform", "drill"]
        
        self.spawn_zones["obstacles"].append({
            "id": f"slot_{len(self.spawn_zones['obstacles'])}",
            "position": {"x": x, "y": y},
            "allowed_types": allowed_types
        })
    
    def to_json(self) -> Dict[str, Any]:
        """
        Export room template to JSON format
        
        Returns:
            Dictionary representing room data
        """
        return {
            "id": self.id,
            "metadata": self.metadata,
            "tilemap": {
                "width": self.width,
                "height": self.height,
                "tiles": self.tiles
            },
            "connections": self.connections,
            "spawn_zones": self.spawn_zones,
            "validation": self.validation
        }
    
    def copy(self) -> 'RoomTemplate':
        """
        Create a deep copy of this template
        
        Returns:
            New RoomTemplate instance with copied data
        """
        return copy.deepcopy(self)
    
    def get_summary(self) -> str:
        """
        Get human-readable summary of this template
        
        Returns:
            String summary with key information
        """
        return (f"RoomTemplate({self.id}): {self.shape_type} "
                f"{self.width}x{self.height} "
                f"difficulty={self.metadata['difficulty']} "
                f"connections={len(self.connections)}")
    
    def __repr__(self) -> str:
        return self.get_summary()
