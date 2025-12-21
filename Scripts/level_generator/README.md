# Level Generation Tool

Procedural 2D level generator for Lament platformer game.

## About

This tool generates room templates for linear 2D platformer levels with:
- Multiple shape types (Horizontal, Vertical, Box arenas, etc.)
- Difficulty-based procedural generation
- Obstacles: platforms, gaps, spikes, slopes
- Visual preview system
- JSON export for Unreal Engine 5 import

**Current Status**: Week 1 - Foundation + Procedural Generator

## Setup

### Prerequisites
- Python 3.8 or higher

### Installation

1. **Create virtual environment:**
   ```bash
   cd Scripts/level_generator
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Generate Single Room

```bash
python main.py --shape horizontal_right --difficulty 5 --length medium
```

**Available options:**
- `--shape`: `horizontal_right`, `vertical_up`, `box`
- `--difficulty`: 1-10 (1=easy, 10=hard)
- `--length` or `--size`: `short`, `medium`, `long` (or `small`, `large` for box)
- `--features`: Comma-separated list (default: `spikes,slopes,platforms`)
- `--output`: Output filename (optional, auto-generates if not provided)

**Examples:**
```bash
# Easy horizontal room
python main.py --shape horizontal_right --difficulty 2 --length short

# Hard vertical climbing challenge
python main.py --shape vertical_up --difficulty 8 --length long

# Medium combat arena
python main.py --shape box --difficulty 5 --size medium
```

### Batch Generation

Generate multiple templates for testing:

```bash
python batch_generate.py
```

This generates 50-150 templates across different shape types, difficulties, and sizes.

**Output location**: `output/batch_TIMESTAMP/`

## Project Structure

```
level_generator/
├── main.py                    # CLI entry point
├── batch_generate.py          # Batch generation script
├── config.py                  # Global configuration
├── generators/
│   ├── room_generator.py      # Main generation dispatcher
│   └── shape_generators/      # Shape-specific generators
│       ├── horizontal_right.py
│       ├── vertical_up.py
│       └── box.py
├── utils/
│   ├── room_template.py       # RoomTemplate data class
│   └── tile_constants.py      # Tile type definitions
├── preview/
│   └── visualizer.py          # 2D preview renderer
├── output/                    # Generated previews
└── tests/                     # Unit tests
```

## Tile Types

| ID | Type | Description |
|----|------|-------------|
| 0 | Empty | Air/void |
| 1 | Ground | Solid ground tile |
| 2 | Wall | Solid wall tile |
| 3 | Platform (One-Way) | Fall-through platform |
| 4 | Spike | Damage hazard |
| 10 | Slope Up-Right | 45° ramp / |
| 11 | Slope Up-Left | 45° ramp \ |
| 12 | Slope Down-Right | 45° ramp \ |
| 13 | Slope Down-Left | 45° ramp / |

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Week 1 Features

- ✅ 3 shape generators (Horizontal Right, Vertical Up, Box)
- ✅ Procedural generation with difficulty scaling
- ✅ Spikes and 45-degree slopes
- ✅ 2D visualizer with grid lines
- ✅ Batch generation script
- ✅ CLI interface

### Coming in Week 2

- Validation system (pathfinding, jump checks)
- Template variation system
- More shape types
- JSON export

## Documentation

Full design documentation: `Documentation/Projects/LevelGenerationTool.md`

## License

Part of the Lament game project.
