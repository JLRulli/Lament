# Lament - Documentation Hub

Welcome to the Lament project documentation. This Obsidian vault contains all game design documentation, technical specifications, and project planning materials.

---

## Quick Links

### Game Design
- [[Overview]] - Game concept, pillars, and vision
- [[Mechanics/README|Mechanics]] - Gameplay mechanics documentation
- [[Systems/README|Systems]] - Game systems (combat, inventory, progression, etc.)
- [[Narrative/README|Narrative]] - Story, lore, characters, world-building
- [[Technical/README|Technical]] - Technical design decisions and architecture

### Projects & Tools
- [[Projects/README|Active Projects]] - Mini-project planning and tracking

### Reference
- [[Reference/NamingConventions|Naming Conventions]] - Project-wide naming standards

---

## Documentation Structure

```
Documentation/
├── GameDesign/           # Core game design documentation
│   ├── Overview.md       # Start here for project overview
│   ├── Mechanics/        # Gameplay mechanics details
│   ├── Systems/          # Game systems design
│   ├── Narrative/        # Story and world-building
│   └── Technical/        # Technical design docs
├── Projects/             # Planning docs for scripts/tools
├── Reference/            # Standards and conventions
└── index.md             # This file
```

---

## Getting Started

### For New Team Members
1. Read [[Overview]] to understand the game concept and vision
2. Review [[Reference/NamingConventions|Naming Conventions]] for code/doc standards
3. Explore relevant sections based on your role:
   - **Programmers**: Technical/, Systems/, Mechanics/
   - **Designers**: Mechanics/, Systems/, Narrative/
   - **Writers**: Narrative/
   - **Tool Developers**: Projects/

### For OpenCode Agent
- Check [[Overview]] for game context
- Search relevant sections based on task type
- Update docs after implementing features
- Create new docs for new systems/features

---

## Documentation Guidelines

### Creating New Documentation
- Use PascalCase for file names (e.g., `CombatSystem.md`)
- Place in appropriate subfolder
- Link to related documents using Obsidian wiki-links
- Update this index if adding major new sections

### Maintaining Documentation
- Keep docs synchronized with code/implementation
- Document "why" decisions were made, not just "what"
- Update design docs if implementation differs from original plan
- Include examples and usage instructions

### Linking
- Use `[[WikiLinks]]` for internal documentation references
- Use relative paths for external files (e.g., code files)
- Create bidirectional links between related concepts

---

## Recent Changes

_This section tracks major documentation updates. Update when making significant changes._

- **2025-12-16**: Initial documentation structure created

---

## Project Status

**Phase**: Pre-production / Setup  
**Unreal Engine**: 5.5  
**Primary Language**: C++

---

## Notes

- This vault is part of the Lament project repository
- Use Obsidian for the best experience (linking, graph view, etc.)
- Documentation should be updated alongside code changes
- When in doubt, document it
