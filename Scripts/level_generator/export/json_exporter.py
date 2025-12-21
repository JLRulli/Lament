"""
JSON export system for room templates

Exports room templates to JSON format for use in Unreal Engine 5.
"""
import json
import os
from typing import Dict, Any, Optional, List
from utils.tile_constants import TILE_LEGEND


def export_room_to_json(
    room,
    validation: Dict,
    quality: Dict,
    filepath: str,
    include_metadata: bool = True
):
    """
    Export a room template to JSON format
    
    Creates a JSON file compatible with UE5 integration.
    
    Args:
        room: RoomTemplate object
        validation: Validation results dict
        quality: Quality scoring results dict
        filepath: Output JSON file path
        include_metadata: Whether to include full metadata (default: True)
    """
    data = build_room_json(room, validation, quality, include_metadata)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def build_room_json(
    room,
    validation: Dict,
    quality: Dict,
    include_metadata: bool = True
) -> Dict[str, Any]:
    """
    Build JSON data structure for a room template
    
    Args:
        room: RoomTemplate object
        validation: Validation results dict
        quality: Quality scoring results dict
        include_metadata: Whether to include full metadata
    
    Returns:
        Dict ready for JSON serialization
    """
    data = {
        "version": "1.0",
        "generated_by": "level_generator_week4"
    }
    
    # Core metadata
    if include_metadata:
        data["metadata"] = {
            "id": room.id,
            "shape_type": room.shape_type,
            "width": room.width,
            "height": room.height,
            "difficulty": room.metadata.get('difficulty', 1),
            "size_category": room.metadata.get('size', 'medium'),
            "features": room.metadata.get('features', [])
        }
    
    # Tilemap data (essential for UE5)
    data["tilemap"] = {
        "width": room.width,
        "height": room.height,
        "tiles": room.tiles,  # 2D array of tile IDs
        "tile_legend": TILE_LEGEND,
        "coordinate_system": "Y=0 is TOP, Y=height-1 is BOTTOM"
    }
    
    # Validation info
    if include_metadata:
        data["validation"] = {
            "valid": validation.get('valid', False),
            "tier": validation.get('tier', 'UNKNOWN'),
            "path_length": validation.get('path_length', 0),
            "spike_count": validation.get('spike_count', 0),
            "platform_count": validation.get('platform_count', 0),
            "floor_coverage": round(validation.get('floor_coverage', 0), 3)
        }
    
    # Quality scores
    if include_metadata:
        data["quality"] = {
            "overall": round(quality.get('overall', 0), 2),
            "playability": round(quality.get('playability', 0), 2),
            "challenge": round(quality.get('challenge', 0), 2),
            "variety": round(quality.get('variety', 0), 2)
        }
    
    # Spawn zones (essential for enemy placement)
    data["spawn_zones"] = room.spawn_zones
    
    # Connections (entrance/exit positions)
    data["connections"] = room.connections
    
    return data


def import_room_from_json(filepath: str) -> Dict[str, Any]:
    """
    Import a room template from JSON
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Dict with room data
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return data


def export_library_to_json_batch(
    library,
    output_dir: str,
    prefix: str = "room",
    include_metadata: bool = True
):
    """
    Export all templates in a library to individual JSON files
    
    Args:
        library: TemplateLibrary object
        output_dir: Output directory path
        prefix: Filename prefix (default: "room")
        include_metadata: Whether to include full metadata
    
    Returns:
        List of exported file paths
    """
    import os
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    exported_files = []
    
    for i, template in enumerate(library.templates):
        room = template['room']
        validation = template['validation']
        quality = template['quality']
        
        # Generate filename
        filename = f"{prefix}_{room.shape_type}_{room.id}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Export
        export_room_to_json(room, validation, quality, filepath, include_metadata)
        exported_files.append(filepath)
    
    return exported_files


def validate_json_export(filepath: str) -> bool:
    """
    Validate that a JSON export file is well-formed
    
    Args:
        filepath: Path to JSON file to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        data = import_room_from_json(filepath)
        
        # Check required fields
        required_fields = ['tilemap', 'spawn_zones', 'connections']
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return False
        
        # Check tilemap structure
        tilemap = data['tilemap']
        if 'width' not in tilemap or 'height' not in tilemap or 'tiles' not in tilemap:
            print("Tilemap missing required fields")
            return False
        
        # Check tilemap dimensions match
        height = len(tilemap['tiles'])
        if height != tilemap['height']:
            print(f"Tilemap height mismatch: {height} != {tilemap['height']}")
            return False
        
        if height > 0:
            width = len(tilemap['tiles'][0])
            if width != tilemap['width']:
                print(f"Tilemap width mismatch: {width} != {tilemap['width']}")
                return False
        
        return True
    
    except Exception as e:
        print(f"Validation error: {e}")
        return False


def export_level_with_entities(
    level_data: Dict[str, Any],
    filepath: str
):
    """
    Export a level with entities (enemies, obstacles, save points) to JSON
    
    Args:
        level_data: Level data dict from world generator
        filepath: Output JSON file path
    """
    room = level_data['room']
    validation = level_data['validation']
    quality = level_data['quality']
    entities = level_data['entities']
    
    # Build base room JSON
    data = build_room_json(room, validation, quality, include_metadata=True)
    
    # Add entities
    data["entities"] = {
        "enemies": entities.get('enemies', []),
        "obstacles": entities.get('obstacles', []),
        "save_point": entities.get('save_point')
    }
    
    # Add level-specific metadata
    data["level_info"] = {
        "level_id": level_data['level_id'],
        "stats": level_data['stats']
    }
    
    # Write to file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def export_world(levels: List[Dict[str, Any]], output_dir: str, world_name: str = "World"):
    """
    Export all levels in a world to separate JSON files
    
    Args:
        levels: List of level data dicts
        output_dir: Output directory path
        world_name: World name for file naming
    
    Returns:
        List of exported file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    
    exported_files = []
    
    for i, level_data in enumerate(levels):
        filename = f"{world_name}_L{i+1:02d}.json"
        filepath = os.path.join(output_dir, filename)
        
        export_level_with_entities(level_data, filepath)
        exported_files.append(filepath)
    
    # Also export world summary
    summary_path = os.path.join(output_dir, f"{world_name}_summary.json")
    
    summary = {
        "world_name": world_name,
        "level_count": len(levels),
        "levels": [
            {
                "level_id": lvl['level_id'],
                "difficulty": lvl['stats']['difficulty'],
                "shape": lvl['stats']['shape'],
                "quality": lvl['stats']['quality_score'],
                "enemy_count": lvl['stats']['enemy_count'],
                "obstacle_count": lvl['stats']['obstacle_count']
            }
            for lvl in levels
        ]
    }
    
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    exported_files.append(summary_path)
    
    return exported_files
