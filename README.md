# Lament

A game development project built with Unreal Engine 5.5.

---

## Project Overview

This repository contains all materials for the Lament game project, including:
- Game design documentation (Obsidian vault)
- Unreal Engine project files
- Automation scripts and development tools
- Source assets

---

## Project Structure

```
Lament/
├── .opencode/            # OpenCode agent configuration
│   └── agent.md          # Agent instructions and documentation strategy
├── Documentation/        # Obsidian vault - game design & planning docs
│   ├── GameDesign/       # Core game design documentation
│   │   ├── Overview.md   # Main game concept and vision
│   │   ├── Mechanics/    # Gameplay mechanics details
│   │   ├── Systems/      # Game systems (inventory, combat, etc.)
│   │   ├── Narrative/    # Story, lore, characters
│   │   └── Technical/    # Technical design decisions
│   ├── Projects/         # Mini-project planning docs (scripts, tools)
│   ├── Reference/        # Standards and conventions
│   │   └── NamingConventions.md
│   └── index.md          # Documentation hub
├── UnrealProjects/       # Unreal Engine 5.5 project files
│   └── [YourProject]/    # Created via UE5 editor
├── Scripts/              # Automation scripts and tools
│   ├── tools/            # Utility scripts (Python)
│   └── build/            # Build automation
├── Assets/               # Source assets (pre-import to UE)
│   ├── Textures/
│   ├── Models/
│   └── Audio/
├── .gitignore
└── README.md             # This file
```

---

## Getting Started

### Prerequisites

- **Unreal Engine 5.5** - [Download](https://www.unrealengine.com/download)
- **Python 3.x** - For automation scripts
- **Obsidian** - [Download](https://obsidian.md) for documentation
- **Git** - Version control

### Initial Setup

1. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd Lament
   ```

2. **Open Documentation in Obsidian**:
   - Launch Obsidian
   - Open folder as vault: `Documentation/`
   - Start with `index.md` for navigation

3. **Create Unreal Project** (when ready):
   - Open Unreal Engine 5.5
   - Create new C++ project
   - Save in `UnrealProjects/` directory
   - Choose appropriate template and settings

4. **Set up Python environment** (for scripts):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   # Install dependencies as needed
   ```

---

## Development Workflow

### Working with Documentation

All design documents, technical specs, and project plans live in `Documentation/`.

**Key Documents**:
- `Documentation/index.md` - Documentation hub with links to all sections
- `Documentation/GameDesign/Overview.md` - Game concept and vision
- `Documentation/Reference/NamingConventions.md` - Code/doc naming standards

**Guidelines**:
- Use Obsidian for the best experience (wiki links, graph view, search)
- Update documentation alongside code changes
- Link related documents using `[[WikiLinks]]`
- Keep docs synchronized with implementation

### Working with OpenCode

This project is configured for use with OpenCode AI assistant.

**Agent Configuration**: `.opencode/agent.md`

**The agent is configured to**:
- Reference documentation in `Documentation/` for project context
- Update docs automatically when implementing features
- Follow naming conventions from `Documentation/Reference/NamingConventions.md`
- Search relevant docs based on task type (gameplay, scripts, etc.)

**Best Practices**:
- The agent will check `Documentation/GameDesign/Overview.md` for game context
- For script projects, it will look for planning docs in `Documentation/Projects/`
- After implementing features, the agent updates relevant documentation

### Coding Standards

See `Documentation/Reference/NamingConventions.md` for complete guidelines.

**Quick Reference**:
- **Unreal C++ code**: PascalCase with Unreal prefixes (`APlayerCharacter`, `UHealthComponent`)
- **Functions**: PascalCase (`GetHealth()`, `TakeDamage()`)
- **Variables**: PascalCase, `b` prefix for booleans (`bIsAlive`, `CurrentHealth`)
- **Documentation files**: PascalCase (`Overview.md`, `CombatSystem.md`)
- **Python scripts**: snake_case (`color_palette_extractor.py`)
- **Folders**: PascalCase (docs) or snake_case (scripts)

### Working with Scripts

Automation scripts are located in `Scripts/`.

**Creating New Scripts**:
1. Create planning doc in `Documentation/Projects/[ScriptName].md`
2. Implement script in appropriate `Scripts/` subfolder
3. Include `README.md` in script folder
4. Add `requirements.txt` for Python dependencies
5. Update planning doc with usage instructions

**Example Structure**:
```
Scripts/tools/color_palette_extractor/
├── color_palette_extractor.py
├── requirements.txt
└── README.md
```

### Working with Assets

**Source Assets** (pre-import):
- Place in `Assets/` organized by type
- Use descriptive names: `character_diffuse_1024.png`

**Unreal Assets** (post-import):
- Import through UE5 to `UnrealProjects/[Project]/Content/`
- Follow Unreal naming conventions with prefixes: `T_Character_Diffuse`

---

## Version Control

### Git Workflow

```bash
# Check status
git status

# Stage changes
git add <files>

# Commit with meaningful message
git commit -m "Add player health system

Implements health/damage mechanics from Documentation/GameDesign/Systems/HealthSystem.md"

# Push changes
git push
```

### What's Ignored

The `.gitignore` is configured to exclude:
- Unreal Engine intermediate/generated files (`Binaries/`, `Intermediate/`, `Saved/`)
- Python cache and virtual environments
- Obsidian workspace files (user-specific)
- OS-specific files (`.DS_Store`, `Thumbs.db`)
- IDE configurations

See `.gitignore` for complete list.

---

## Technology Stack

- **Game Engine**: Unreal Engine 5.5
- **Primary Language**: C++ (gameplay code)
- **Scripting**: Python (automation), Shell scripts
- **Documentation**: Obsidian (Markdown-based)
- **Version Control**: Git
- **AI Assistant**: OpenCode

---

## Project Status

**Phase**: Pre-production / Setup  
**Last Updated**: 2025-12-16

See `Documentation/GameDesign/Overview.md` for development roadmap.

---

## Documentation

For detailed game design, technical specifications, and project planning:

📖 **Start here**: `Documentation/index.md`

Key sections:
- **Game Design**: Concept, mechanics, systems, narrative
- **Projects**: Planning docs for scripts and tools
- **Reference**: Naming conventions and standards

---

## Contributing

_[Add contribution guidelines if working with a team]_

---

## License

_[To be determined]_

---

## Contact

_[Add contact information]_

---

## Notes

- Create your Unreal project through UE5 editor and save it in `UnrealProjects/`
- The entire `Documentation/` folder is an Obsidian vault
- Use OpenCode for development assistance - it's configured to reference your docs
- Keep documentation updated alongside code changes
