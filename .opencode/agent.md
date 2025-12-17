# Lament - OpenCode Agent Configuration

## Project Overview

**Project Type**: Game Development (Unreal Engine 5.5)  
**Primary Language**: C++ (gameplay code)  
**Scripting**: Python (automation tools), Shell scripts  
**Documentation**: Obsidian vault in `Documentation/`

This is a game development project built with Unreal Engine 5.5. The agent should assist with C++ gameplay programming, Python automation scripts, and maintaining comprehensive documentation.

---

## Core Documentation

Always check these key documents for project context:

- **Game Overview**: `Documentation/GameDesign/Overview.md` - Main game concept, pillars, and design philosophy
- **Naming Conventions**: `Documentation/Reference/NamingConventions.md` - Project-wide naming standards
- **Active Projects**: `Documentation/Projects/` - Mini-project planning docs (scripts, tools, etc.)

---

## Documentation Search Strategy

When working on tasks, intelligently search relevant documentation sections:

### Gameplay Features
- Search `Documentation/GameDesign/Mechanics/` for gameplay mechanics
- Check `Documentation/GameDesign/Systems/` for game systems (inventory, combat, etc.)
- Review `Documentation/GameDesign/Technical/` for technical design decisions

### Narrative & Lore
- Reference `Documentation/GameDesign/Narrative/` for story, characters, world-building

### Script Projects
- **Always check** `Documentation/Projects/` for planning docs before starting script work
- Create planning docs for new automation tools/scripts

### Unfamiliar Topics
- Use the Task tool with the "explore" subagent to thoroughly search documentation
- Search multiple locations and related terms for comprehensive understanding

---

## Agent Responsibilities

### Documentation Management

**CRITICAL**: The agent must actively maintain documentation alongside code changes.

#### When Implementing Features:
1. **Before coding**: Read relevant design docs in `Documentation/GameDesign/`
2. **During implementation**: Note any design decisions or deviations
3. **After completion**: Update documentation with:
   - Implementation notes
   - Technical details
   - Usage instructions
   - Any changes from original design

#### When Creating New Systems:
1. Create documentation in appropriate `Documentation/GameDesign/` subfolder
2. Include: purpose, architecture, key classes/functions, usage examples
3. Link to related documentation

#### When Building Scripts/Tools:
1. Check for existing planning doc in `Documentation/Projects/`
2. If none exists, create one with: purpose, requirements, approach, usage
3. Update planning doc after implementation with usage instructions and status

#### Documentation Updates:
- Keep technical docs synchronized with code changes
- Update design docs if implementation differs from original design
- Document "why" decisions were made, not just "what" was implemented
- Cross-reference between code and documentation in commit messages

---

## Code Conventions

### Unreal Engine C++ Standards

Follow Unreal Engine coding standards strictly. See `Documentation/Reference/NamingConventions.md` for complete details.

#### Quick Reference:
- **Classes**: PascalCase with Unreal prefixes (`A` for Actors, `U` for UObjects, `F` for structs, `E` for enums)
  - Example: `APlayerCharacter`, `UInventoryComponent`, `FItemData`, `EWeaponType`
- **Functions**: PascalCase
  - Example: `GetHealth()`, `TakeDamage()`, `OnInventoryChanged()`
- **Variables**: PascalCase with prefixes
  - `b` for booleans: `bIsAlive`, `bCanJump`
  - No prefix for most others: `CurrentHealth`, `PlayerName`, `MaxSpeed`
- **Files**: Match class names exactly
  - `PlayerCharacter.h`, `PlayerCharacter.cpp`

#### Code Quality:
- **Comment complex logic** thoroughly
- Use descriptive variable/function names
- Prefer C++ for gameplay logic (minimize Blueprint dependency)
- Follow SOLID principles where applicable
- Write modular, reusable code

---

## Script Development

### Python Scripts
- **Naming**: `snake_case` for files, functions, variables
  - Example: `color_palette_extractor.py`, `extract_colors()`, `image_path`
- **Structure**: Place scripts in `Scripts/` with appropriate subfolders
  - Example: `Scripts/tools/color_palette_extractor/`
- **Dependencies**: Always include `requirements.txt`
- **Documentation**: Add README.md in script folder with usage instructions

### Shell Scripts
- Use for build automation and simple tooling
- Place in `Scripts/build/` or `Scripts/tools/`
- Include usage comments at the top of each script

---

## Task Guidelines

### Implementing Gameplay Features

**Workflow:**
1. **Research**: Read relevant docs in `Documentation/GameDesign/`
2. **Plan**: Understand requirements, dependencies, and architecture
3. **Implement**: Write C++ code in `UnrealProjects/[ProjectName]/Source/`
4. **Document**: Update design docs with implementation details
5. **Commit**: Include reference to related design docs in commit message

**Example Commit Message:**
```
Add player health system

Implements health/damage mechanics from Documentation/GameDesign/Systems/HealthSystem.md
- Created AHealthComponent for reusable health logic  
- Added damage types and resistance calculations
- Integrated with UI system for health bar updates
```

### Creating Automation Scripts

**Workflow:**
1. **Check Planning Doc**: Look for existing doc in `Documentation/Projects/`
2. **Create Structure**: Set up script folder in `Scripts/` with appropriate nesting
3. **Implement**: Write Python/shell script following naming conventions
4. **Dependencies**: Add `requirements.txt` (Python) or document dependencies
5. **Document**: 
   - Add README.md in script folder
   - Update planning doc in `Documentation/Projects/` with usage and status
6. **Test**: Verify script works as expected

### Working with Assets

**Workflow:**
1. **Check Design Docs**: Verify asset specifications in relevant design docs
2. **Source Assets**: Place pre-import assets in `Assets/` (organized by type)
   - `Assets/Textures/`
   - `Assets/Models/`
   - `Assets/Audio/`
3. **Import to UE**: Import through Unreal Engine to `UnrealProjects/[ProjectName]/Content/`
4. **Document Pipeline**: Note any asset pipeline details in design docs

---

## File Organization

### Documentation Structure
```
Documentation/
├── GameDesign/           # Game design documentation
│   ├── Overview.md       # Main game concept (ALWAYS CHECK FIRST)
│   ├── Mechanics/        # Gameplay mechanics
│   ├── Systems/          # Game systems
│   ├── Narrative/        # Story, lore, characters
│   └── Technical/        # Technical design
├── Projects/             # Mini-project planning docs
├── Reference/            # Reference materials
│   └── NamingConventions.md
└── index.md              # Documentation hub
```

### Project Structure
```
Lament/
├── .opencode/            # This file
├── Documentation/        # Obsidian vault (see above)
├── UnrealProjects/       # UE 5.5 projects
├── Scripts/              # Automation scripts
│   ├── tools/           # Utility scripts
│   └── build/           # Build automation
├── Assets/              # Source assets (pre-import)
└── README.md
```

---

## Development Workflow

### Standard Task Flow
1. **Understand Requirements**: Read user request carefully
2. **Gather Context**: Search relevant documentation using strategies above
3. **Plan**: Break down task into steps (use TodoWrite for complex tasks)
4. **Implement**: Write code following conventions
5. **Document**: Update or create documentation
6. **Verify**: Test implementation
7. **Commit**: Create meaningful commit with documentation references

### Multi-Step Tasks
- Use TodoWrite tool to track progress for complex tasks (3+ steps)
- Mark todos as in_progress, completed as you work
- Only one todo in_progress at a time

### Communication
- Be concise and technical
- Reference specific files with line numbers when relevant
- Explain "why" behind decisions, not just "what"
- Ask clarifying questions if requirements are unclear

---

## Special Considerations

### Unreal Engine Specifics
- Understand UE project structure (Source/, Content/, Config/)
- Be aware of UE build process and generated files
- Know when to use Actors vs Components vs UObjects
- Understand Blueprint vs C++ trade-offs (prefer C++)

### Documentation-First Approach
- Design docs should drive implementation
- Implementation insights should update design docs
- Keep documentation and code in sync
- Documentation is not optional

### Version Control
- Never commit Unreal intermediate/generated files (see .gitignore)
- Commit source code, assets, and documentation together
- Write meaningful commit messages that reference docs
- Keep commits focused and atomic

---

## Quick Command Reference

### Common Tasks
- **Search game design**: Use Task tool with "explore" subagent on `Documentation/GameDesign/`
- **Check naming conventions**: Read `Documentation/Reference/NamingConventions.md`
- **Find script plans**: Look in `Documentation/Projects/`
- **Implement feature**: Check design docs → Write code → Update docs → Commit

### Documentation Paths
- Game overview: `Documentation/GameDesign/Overview.md`
- Naming guide: `Documentation/Reference/NamingConventions.md`
- Doc hub: `Documentation/index.md`
- Script plans: `Documentation/Projects/`

---

## Notes

- This project uses C++ predominantly for gameplay code
- Python is the primary scripting language for automation
- Documentation lives in an Obsidian vault for rich linking and graph view
- The agent should be proactive about documentation maintenance
- When in doubt, search documentation before making assumptions
