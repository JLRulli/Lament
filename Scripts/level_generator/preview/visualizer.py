"""
2D Visualizer for room templates using Pillow
"""
from PIL import Image, ImageDraw, ImageFont
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.room_template import RoomTemplate
from utils.tile_constants import TILE_COLORS
import config


def render_room(room_template: RoomTemplate, output_path: str, 
                show_grid: bool = True, show_metadata: bool = True) -> None:
    """
    Render room template to PNG image
    
    Args:
        room_template: RoomTemplate to render
        output_path: Path to save PNG file
        show_grid: Whether to draw grid lines
        show_metadata: Whether to show metadata banner
    """
    tile_size = config.PREVIEW_TILE_SIZE
    
    # Calculate image dimensions
    img_width = room_template.width * tile_size
    img_height = room_template.height * tile_size
    
    # Add space for metadata banner if enabled
    if show_metadata:
        img_height += config.METADATA_BANNER_HEIGHT
    
    # Create image
    image = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Calculate Y offset for tilemap (0 if no metadata, banner height if metadata)
    y_offset = config.METADATA_BANNER_HEIGHT if show_metadata else 0
    
    # Draw tiles
    for y in range(room_template.height):
        for x in range(room_template.width):
            tile_id = room_template.get_tile(x, y)
            if tile_id is None:
                tile_id = 0  # Treat None as empty
            color = TILE_COLORS.get(tile_id, (255, 0, 255))  # Magenta for unknown tiles
            
            # Calculate pixel coordinates
            px = x * tile_size
            py = y * tile_size + y_offset
            
            # Draw tile rectangle
            draw.rectangle(
                [px, py, px + tile_size - 1, py + tile_size - 1],
                fill=color
            )
    
    # Draw grid lines
    if show_grid:
        grid_color = config.GRID_COLOR
        
        # Vertical lines
        for x in range(room_template.width + 1):
            px = x * tile_size
            draw.line(
                [(px, y_offset), (px, img_height)],
                fill=grid_color,
                width=config.GRID_LINE_WIDTH
            )
        
        # Horizontal lines
        for y in range(room_template.height + 1):
            py = y * tile_size + y_offset
            draw.line(
                [(0, py), (img_width, py)],
                fill=grid_color,
                width=config.GRID_LINE_WIDTH
            )
    
    # Draw door highlights
    for name, connection in room_template.connections.items():
        pos = connection["position"]
        x, y = pos["x"], pos["y"]
        
        # Determine color based on door type
        if name == "entrance":
            door_color = config.DOOR_ENTRY_COLOR
        elif name == "exit":
            door_color = config.DOOR_EXIT_COLOR
        else:
            door_color = (255, 255, 0)  # Yellow for other connections
        
        # Draw highlight rectangle
        px = x * tile_size
        py = y * tile_size + y_offset
        width = config.DOOR_HIGHLIGHT_WIDTH
        
        # Draw thick border around door tile
        draw.rectangle(
            [px, py, px + tile_size - 1, py + tile_size - 1],
            outline=door_color,
            width=width
        )
    
    # Draw metadata banner
    if show_metadata:
        # Background
        draw.rectangle(
            [0, 0, img_width, config.METADATA_BANNER_HEIGHT],
            fill=config.METADATA_BG_COLOR
        )
        
        # Text
        metadata_text = (
            f"ID: {room_template.id} | "
            f"Shape: {room_template.shape_type} | "
            f"Size: {room_template.width}x{room_template.height} | "
            f"Difficulty: {room_template.metadata['difficulty']}"
        )
        
        # Try to use a font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()
        
        # Draw text
        draw.text(
            (10, config.METADATA_BANNER_HEIGHT // 2 - 7),
            metadata_text,
            fill=config.METADATA_TEXT_COLOR,
            font=font
        )
    
    # Save image
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    image.save(output_path)
    print(f"✓ Rendered room to: {output_path}")


def render_room_simple(room_template: RoomTemplate, output_path: str) -> None:
    """
    Simple wrapper for quick rendering with default settings
    
    Args:
        room_template: RoomTemplate to render
        output_path: Path to save PNG file
    """
    render_room(room_template, output_path, show_grid=True, show_metadata=True)


def calculate_spatial_layout(levels):
    """
    Calculate 2D spatial positions for levels based on door directions
    
    Args:
        levels: List of level dicts from world generator
    
    Returns:
        Dict mapping level_id to position dict with x, y, width, height
    """
    positions = {}
    
    # Start at origin
    current_x = 0
    current_y = 0
    
    for i, level in enumerate(levels):
        level_id = level['level_id']
        room = level['room']
        
        # Store position
        positions[level_id] = {
            'x': current_x,
            'y': current_y,
            'width': room.width,
            'height': room.height,
            'level': level
        }
        
        # Calculate next position based on exit direction
        if i < len(levels) - 1:
            exit_conn = room.connections.get('exit')
            if exit_conn:
                exit_dir = exit_conn['direction']
                
                # Move to next position based on exit direction
                if exit_dir == 'right':
                    current_x += room.width
                elif exit_dir == 'left':
                    current_x -= room.width
                elif exit_dir == 'up':
                    current_y -= room.height
                elif exit_dir == 'down':
                    current_y += room.height
    
    return positions


def get_difficulty_color(difficulty):
    """
    Get color for difficulty heatmap (green=easy, yellow=medium, red=hard)
    
    Args:
        difficulty: Difficulty value (1-10)
    
    Returns:
        RGB tuple
    """
    # Normalize to 0-1
    norm = (difficulty - 1) / 9.0
    
    if norm < 0.5:
        # Green to Yellow (easy to medium)
        r = int(norm * 2 * 255)
        g = 255
        b = 0
    else:
        # Yellow to Red (medium to hard)
        r = 255
        g = int((1 - (norm - 0.5) * 2) * 255)
        b = 0
    
    return (r, g, b)


def render_world_spatial(levels, output_path, tile_size=16, show_grid=True):
    """
    Render entire world as a spatial 2D map
    
    Args:
        levels: List of level dicts from world generator
        output_path: Path to save PNG file
        tile_size: Pixels per tile (default 16 for world overview)
        show_grid: Whether to draw grid background
    """
    # Calculate spatial positions
    positions = calculate_spatial_layout(levels)
    
    # Find bounds
    min_x = min(pos['x'] for pos in positions.values())
    max_x = max(pos['x'] + pos['width'] for pos in positions.values())
    min_y = min(pos['y'] for pos in positions.values())
    max_y = max(pos['y'] + pos['height'] for pos in positions.values())
    
    # Calculate canvas size with padding
    padding = 100  # Extra space for labels and borders
    header_height = 80
    footer_height = 60
    
    total_width_tiles = max_x - min_x
    total_height_tiles = max_y - min_y
    
    canvas_width = total_width_tiles * tile_size + padding * 2
    canvas_height = total_height_tiles * tile_size + padding * 2 + header_height + footer_height
    
    # Create image
    image = Image.new('RGB', (canvas_width, canvas_height), color=(250, 250, 250))
    draw = ImageDraw.Draw(image)
    
    # Try to load font
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        label_font = ImageFont.truetype("arial.ttf", 12)
        small_font = ImageFont.truetype("arial.ttf", 10)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw header
    world_name = levels[0]['level_id'].rsplit('_L', 1)[0]
    total_enemies = sum(len(lvl['entities']['enemies']) for lvl in levels)
    total_obstacles = sum(len(lvl['entities']['obstacles']) for lvl in levels)
    
    header_text = f"{world_name} - {len(levels)} Levels | {total_enemies} Enemies | {total_obstacles} Obstacles"
    draw.rectangle([0, 0, canvas_width, header_height], fill=(60, 60, 80))
    draw.text((20, 25), header_text, fill=(255, 255, 255), font=title_font)
    
    # Draw grid background if enabled
    y_offset = header_height + padding
    x_offset = padding
    
    if show_grid:
        grid_spacing = tile_size * 5  # Grid every 5 tiles
        
        # Vertical grid lines
        for i in range(0, total_width_tiles * tile_size, grid_spacing):
            x = x_offset + i
            draw.line([(x, y_offset), (x, y_offset + total_height_tiles * tile_size)],
                     fill=(220, 220, 220), width=1)
        
        # Horizontal grid lines
        for i in range(0, total_height_tiles * tile_size, grid_spacing):
            y = y_offset + i
            draw.line([(x_offset, y), (x_offset + total_width_tiles * tile_size, y)],
                     fill=(220, 220, 220), width=1)
    
    # Render each level
    for level_id, pos in positions.items():
        level = pos['level']
        room = level['room']
        
        # Calculate pixel position
        pixel_x = x_offset + (pos['x'] - min_x) * tile_size
        pixel_y = y_offset + (pos['y'] - min_y) * tile_size
        
        # Get difficulty color for border
        difficulty = level['stats']['difficulty']
        border_color = get_difficulty_color(difficulty)
        
        # Draw level border (difficulty heatmap)
        border_width = 3
        draw.rectangle(
            [pixel_x - border_width, pixel_y - border_width,
             pixel_x + room.width * tile_size + border_width,
             pixel_y + room.height * tile_size + border_width],
            outline=border_color,
            width=border_width
        )
        
        # Draw tiles
        for y in range(room.height):
            for x in range(room.width):
                tile_id = room.get_tile(x, y)
                if tile_id is None:
                    tile_id = 0
                color = TILE_COLORS.get(tile_id, (255, 0, 255))
                
                px = pixel_x + x * tile_size
                py = pixel_y + y * tile_size
                
                draw.rectangle(
                    [px, py, px + tile_size - 1, py + tile_size - 1],
                    fill=color
                )
        
        # Draw entity markers
        entities = level['entities']
        
        # Enemies (red dots)
        for enemy in entities.get('enemies', []):
            ex = pixel_x + enemy['position']['x'] * tile_size + tile_size // 2
            ey = pixel_y + enemy['position']['y'] * tile_size + tile_size // 2
            dot_size = 2
            draw.ellipse([ex - dot_size, ey - dot_size, ex + dot_size, ey + dot_size],
                        fill=(255, 0, 0))
        
        # Obstacles (yellow markers)
        for obstacle in entities.get('obstacles', []):
            ox = pixel_x + obstacle['position']['x'] * tile_size + tile_size // 2
            oy = pixel_y + obstacle['position']['y'] * tile_size + tile_size // 2
            
            if obstacle['type'] == 'spike':
                # Triangle
                size = 3
                points = [(ox, oy - size), (ox - size, oy + size), (ox + size, oy + size)]
                draw.polygon(points, fill=(255, 200, 0))
            else:
                # Square for platforms
                size = 2
                draw.rectangle([ox - size, oy - size, ox + size, oy + size],
                             fill=(0, 200, 255))
        
        # Save point (green star)
        if entities.get('save_point'):
            sp = entities['save_point']
            sx = pixel_x + sp['position']['x'] * tile_size + tile_size // 2
            sy = pixel_y + sp['position']['y'] * tile_size + tile_size // 2
            star_size = 4
            draw.ellipse([sx - star_size, sy - star_size, sx + star_size, sy + star_size],
                        fill=(0, 255, 0))
        
        # Draw level label
        level_num = level_id.split('_L')[-1]
        label_x = pixel_x + 5
        label_y = pixel_y + 5
        
        # Label background
        label_bg_width = 50
        label_bg_height = 45
        draw.rectangle(
            [label_x - 2, label_y - 2,
             label_x + label_bg_width, label_y + label_bg_height],
            fill=(255, 255, 255, 200),
            outline=(0, 0, 0)
        )
        
        # Label text
        draw.text((label_x, label_y), f"L{level_num}", fill=(0, 0, 0), font=label_font)
        draw.text((label_x, label_y + 12), f"D:{difficulty}", fill=(100, 100, 100), font=small_font)
        draw.text((label_x, label_y + 24), f"{room.width}x{room.height}", fill=(100, 100, 100), font=small_font)
    
    # Draw connection arrows
    for i in range(len(levels) - 1):
        current_id = levels[i]['level_id']
        next_id = levels[i + 1]['level_id']
        
        current_pos = positions[current_id]
        next_pos = positions[next_id]
        current_room = current_pos['level']['room']
        
        # Get exit position
        exit_conn = current_room.connections.get('exit')
        if exit_conn:
            exit_x = x_offset + (current_pos['x'] - min_x) * tile_size + exit_conn['position']['x'] * tile_size
            exit_y = y_offset + (current_pos['y'] - min_y) * tile_size + exit_conn['position']['y'] * tile_size
            
            # Get entrance position of next level
            next_room = next_pos['level']['room']
            entrance_conn = next_room.connections.get('entrance')
            if entrance_conn:
                entrance_x = x_offset + (next_pos['x'] - min_x) * tile_size + entrance_conn['position']['x'] * tile_size
                entrance_y = y_offset + (next_pos['y'] - min_y) * tile_size + entrance_conn['position']['y'] * tile_size
                
                # Draw arrow
                draw.line([(exit_x, exit_y), (entrance_x, entrance_y)],
                         fill=(0, 150, 255), width=2)
                
                # Draw arrowhead
                arrow_size = 6
                dx = entrance_x - exit_x
                dy = entrance_y - exit_y
                length = (dx*dx + dy*dy) ** 0.5
                if length > 0:
                    dx /= length
                    dy /= length
                    
                    # Perpendicular vector
                    px = -dy
                    py = dx
                    
                    # Arrowhead points
                    tip_x = entrance_x
                    tip_y = entrance_y
                    left_x = tip_x - dx * arrow_size + px * arrow_size / 2
                    left_y = tip_y - dy * arrow_size + py * arrow_size / 2
                    right_x = tip_x - dx * arrow_size - px * arrow_size / 2
                    right_y = tip_y - dy * arrow_size - py * arrow_size / 2
                    
                    draw.polygon([(tip_x, tip_y), (left_x, left_y), (right_x, right_y)],
                               fill=(0, 150, 255))
    
    # Draw footer with legend
    footer_y = canvas_height - footer_height + 10
    draw.rectangle([0, canvas_height - footer_height, canvas_width, canvas_height],
                   fill=(240, 240, 240))
    
    # Legend
    legend_x = 20
    draw.text((legend_x, footer_y), "Legend:", fill=(0, 0, 0), font=label_font)
    
    # Enemy dot
    draw.ellipse([legend_x + 60, footer_y + 3, legend_x + 64, footer_y + 7], fill=(255, 0, 0))
    draw.text((legend_x + 70, footer_y), "Enemy", fill=(0, 0, 0), font=small_font)
    
    # Obstacle marker
    draw.polygon([(legend_x + 135, footer_y), (legend_x + 131, footer_y + 6), (legend_x + 139, footer_y + 6)],
                fill=(255, 200, 0))
    draw.text((legend_x + 145, footer_y), "Hazard", fill=(0, 0, 0), font=small_font)
    
    # Platform marker
    draw.rectangle([legend_x + 210, footer_y + 2, legend_x + 216, footer_y + 8], fill=(0, 200, 255))
    draw.text((legend_x + 222, footer_y), "Platform", fill=(0, 0, 0), font=small_font)
    
    # Save point
    draw.ellipse([legend_x + 300, footer_y + 1, legend_x + 308, footer_y + 9], fill=(0, 255, 0))
    draw.text((legend_x + 314, footer_y), "Save Point", fill=(0, 0, 0), font=small_font)
    
    # Difficulty colors
    draw.text((legend_x, footer_y + 20), "Difficulty:", fill=(0, 0, 0), font=small_font)
    for d in [1, 5, 10]:
        color = get_difficulty_color(d)
        color_x = legend_x + 60 + (d - 1) * 30
        draw.rectangle([color_x, footer_y + 20, color_x + 20, footer_y + 30], fill=color)
        draw.text((color_x + 2, footer_y + 18), str(d), fill=(255, 255, 255), font=small_font)
    
    # Save image
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    image.save(output_path)
    print(f"✓ Rendered world spatial map to: {output_path}")
