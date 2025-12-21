# Art Direction & Asset Pipelines

This section contains all documentation for Lament's visual art direction, asset creation workflows, and technical art systems.

---

## Overview

Lament's art style combines lower-poly 3D assets and 2D sprite animations with a moody, film-inspired aesthetic. The approach prioritizes automation and procedural techniques while maintaining creative control through strategic manual checkpoints.

**Core Principles:**
- **Automation-First**: Minimize manual art creation through AI, procedural generation, and asset modification
- **Checkpoint-Based Approval**: Review and approve work at key stages to avoid wasted effort
- **In-Engine Flexibility**: Use UE5.7 materials, lighting, and post-processing for visual polish rather than baked assets
- **Performance-Conscious**: Lower poly counts and optimized workflows for smooth gameplay

---

## Quick Navigation

### Getting Started
- **[[ArtOverview]]** - Start here for vision, inspirations, and art direction goals

### Asset Creation Workflows
- **[[Pipeline3D]]** - 3D asset workflow (sourcing, texturing, materials, lighting)
- **[[Pipeline2D]]** - 2D sprite/animation workflow (AI generation, rigging, conversion)

### Technical Systems
- **[[Materials3D]]** - 3D master materials, color palettes, edge effects
- **[[Materials2D]]** - 2D sprite materials, normal maps, dynamic lighting
- **[[Lighting]]** - Lighting approaches (naturalistic, cel-shaded, hybrid)
- **[[PostProcessing]]** - Film effects, grain, vignette, halation

### Reference & Tools
- **[[ColorPalettes]]** - Color theory, palette references, mood guidelines
- **[[Tools]]** - Complete software and tools reference

---

## Current Status

### Decisions Made
- Target Platform: UE5.7
- Art Approach: Automation with manual checkpoints
- 3D Style: Lower poly with solid color albedo
- 2D Style: AI-assisted sprite animation with normal maps

### In Testing
- [ ] Lighting approach (naturalistic vs. cel-shaded vs. hybrid)
- [ ] Normal map generation method for 2D sprites
- [ ] Edge mutation/clay-style materials for 3D
- [ ] Re-timing automation tools

### To Be Determined
- [ ] Specific polycount targets for 3D assets
- [ ] 3D asset sources/marketplaces
- [ ] Final post-processing settings
- [ ] Complete tool selection (see [[Tools]])

---

## Key Inspirations

**Visual Style:**
- Taiki Konno's animation work (Fire Force ED1, Magical Destroyers OP1/ED1)
- 90s anime aesthetic (lighting, "human error" in visuals)
- Moody film photography/video
- The Red Turtle (character design)

**Color & Mood:**
- Skyrim (desaturated Nordic palettes)
- Elden Ring (golden highlights on muted backgrounds)
- Mushishi (soft, melancholic naturalism)

See [[ArtOverview]] for detailed analysis and [[ColorPalettes]] for specific palette breakdowns.

---

## Workflow Overview

### 3D Assets
1. Source premade 3D assets
2. Simplify textures to solid colors
3. Apply master materials with color palette system
4. Test lighting approaches
5. Apply post-processing
6. (Optional) Add edge mutation effects

**Full workflow:** [[Pipeline3D]]

### 2D Sprite Animations
1. Generate character with Stable Diffusion + LoRA
2. Create multi-angle character sheet with OpenPose
3. Convert 2D to 3D model
4. Auto-rig character (humanoid)
5. Apply animations in Blender
6. Export side views
7. Convert 3D renders back to 2D style with AI
8. (Conditional) Deflicker
9. Generate normal maps
10. Add "human error" variations
11. Re-time animation
12. Convert to sprite sheet for UE5.7

**Full workflow:** [[Pipeline2D]]

---

## Documentation Structure

```
Art/
├── README.md              # This file - navigation hub
├── ArtOverview.md         # Vision, inspirations, principles
├── Tools.md               # Software and tools reference
├── Pipeline3D.md          # 3D asset workflow
├── Pipeline2D.md          # 2D sprite/animation workflow
├── Materials3D.md         # 3D materials system
├── Materials2D.md         # 2D materials system
├── Lighting.md            # Lighting approaches
├── PostProcessing.md      # Film effects
└── ColorPalettes.md       # Color theory and references
```

---

## Notes

- All art documentation uses Obsidian wiki-link format for internal references
- Progress tracking checkboxes throughout documentation - update as decisions are made
- See [[Tools]] before starting any pipeline to ensure all software is ready
- Mood board and visual references to be added separately (not in these docs)
