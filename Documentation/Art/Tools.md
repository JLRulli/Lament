# Tools & Software Reference

This document catalogs all software, tools, and services used in Lament's art production pipelines. Each tool is referenced throughout the pipeline documentation.

**Status Legend:**
- ✅ **Confirmed** - Tool selected and ready to use
- 🔍 **Under Evaluation** - Currently researching/testing options
- ❓ **TBD** - Not yet researched, decision needed

---

## Core Development Tools

### Unreal Engine 5.7
**Status:** ✅ Confirmed  
**Purpose:** Game engine, material editor, lighting, post-processing  
**Used In:** [[Pipeline3D]], [[Pipeline2D]], [[Materials3D]], [[Materials2D]], [[Lighting]], [[PostProcessing]]

**Key Capabilities:**
- Master material system for runtime color palettes
- Paper2D for sprite rendering
- Post-process volumes for film effects
- Dynamic lighting with normal maps

**Documentation:** [Unreal Engine Documentation](https://docs.unrealengine.com/)

---

## 3D Asset Tools

### Asset Sources
**Status:** ❓ TBD  
**Purpose:** Premade 3D assets for modification  
**Used In:** [[Pipeline3D]]

**Options to Evaluate:**
- Quixel Megascans (included with UE5)
- Sketchfab
- TurboSquid
- CGTrader
- Unity Asset Store (convert to UE5)
- Polyhaven
- Free3D

**Selection Criteria:**
- Lower poly assets available
- Commercial license for game use
- Clean topology
- Price/budget considerations

### Blender
**Status:** ✅ Confirmed  
**Purpose:** 3D model viewing, animation application, rendering for 2D pipeline  
**Used In:** [[Pipeline2D]]

**Key Uses:**
- Apply animations to rigged 3D characters
- Render side-view animations for 2D conversion
- Batch export automation via Python scripting

**Documentation:** [Blender Manual](https://docs.blender.org/)

### Texture/Image Editing
**Status:** ❓ TBD  
**Purpose:** Simplify textures to solid colors for 3D assets  
**Used In:** [[Pipeline3D]]

**Options to Evaluate:**
- Substance Painter (texture authoring)
- Photoshop
- GIMP (free alternative)
- Krita (free alternative)
- Direct in-engine (UE5 Material Editor)

**Requirements:**
- Batch processing capability preferred
- Can output solid color textures
- Integrates with UE5 workflow

---

## 2D Animation Pipeline Tools

### Stable Diffusion
**Status:** 🔍 Under Evaluation  
**Purpose:** AI image generation for character design and style conversion  
**Used In:** [[Pipeline2D]]

**Key Uses:**
- Initial character image generation
- 3D render to 2D style conversion (final animation look)
- Custom LoRA training for consistent art style

**Implementation Options:**
- Local installation (Automatic1111, ComfyUI)
- Cloud services (RunPod, Vast.ai)
- API services (Stability AI)

**Requirements:**
- LoRA training capability
- Img2img for style conversion
- Batch processing
- Consistent output quality

**Documentation:** TBD based on implementation choice

### LoRA Training
**Status:** ❓ TBD  
**Purpose:** Train custom AI model on personal art style  
**Used In:** [[Pipeline2D]]

**Options to Evaluate:**
- Kohya_ss (local training)
- Cloud training services
- Custom training scripts

**Requirements:**
- Training dataset preparation
- Sufficient compute resources (GPU)
- Testing/validation workflow

### OpenPose / Pose Estimation
**Status:** ❓ TBD  
**Purpose:** Generate character sheets with multiple angles/poses  
**Used In:** [[Pipeline2D]]

**Options to Evaluate:**
- OpenPose (original implementation)
- ControlNet with OpenPose preprocessor (Stable Diffusion integration)
- DWPose
- Custom skeleton generation

**Requirements:**
- Multiple angle output
- Compatible with Stable Diffusion workflow
- Consistent character proportions

### 2D to 3D Conversion (CLI)
**Status:** ❓ TBD  
**Purpose:** Convert 2D character images to 3D models  
**Used In:** [[Pipeline2D]]

**Options to Evaluate:**
- TripoSR
- Shap-E
- Point-E
- Commercial services (CSM, Luma AI)
- Custom ML models

**Requirements:**
- CLI/scriptable (for automation)
- Humanoid character support
- Clean topology for rigging
- Reasonable processing time

### Auto-Rigging (Humanoid)
**Status:** ❓ TBD  
**Purpose:** Automatically rig 3D humanoid characters for animation  
**Used In:** [[Pipeline2D]]

**Options to Evaluate:**
- Mixamo Auto-Rigger (web-based, free)
- Rigify (Blender addon)
- AccuRIG
- Custom rigging scripts

**Requirements:**
- Humanoid skeleton only (non-humanoid workflow TBD)
- Compatible with standard animation formats (FBX, BVH)
- Batch processing capability preferred

**Notes:** Non-humanoid rigging workflow to be determined separately

### Animation Asset Sources
**Status:** ❓ TBD  
**Purpose:** Premade animations to apply to rigged characters  
**Used In:** [[Pipeline2D]]

**Options to Evaluate:**
- Mixamo (free, large library)
- Motion capture libraries
- Procedural animation tools
- Hand-animated asset packs

**Requirements:**
- Humanoid compatible
- Variety of actions (idle, walk, run, attack, etc.)
- Side-scrolling appropriate (not all angles needed)

### Blender Automation Scripts
**Status:** ❓ TBD  
**Purpose:** Automate animation application and side-view rendering  
**Used In:** [[Pipeline2D]]

**Development Needed:**
- Script to batch-apply animations from directory
- Script to render side views at consistent camera angle/settings
- Batch export to image sequences

**Language:** Python (Blender API)

**Documentation:** [Blender Python API](https://docs.blender.org/api/current/)

### Deflickering Tool
**Status:** ❓ TBD (may not be needed)  
**Purpose:** Remove frame-to-frame inconsistencies in AI-generated animations  
**Used In:** [[Pipeline2D]] (conditional step)

**Options to Evaluate:**
- Deflicker plugins (After Effects, DaVinci Resolve)
- Video processing tools (FFmpeg filters)
- Custom scripts (frame averaging, optical flow)
- AI-based solutions (temporal consistency models)

**Decision Point:** Test AI style conversion first - may not flicker significantly

### Normal Map Generation
**Status:** ❓ TBD  
**Purpose:** Generate normal maps for 2D sprites to enable dynamic lighting  
**Used In:** [[Pipeline2D]], [[Materials2D]]

**Option A: From 3D Model (During Blender Phase)**
- Render normal pass alongside color render
- Pros: Accurate, consistent with geometry
- Cons: May not match final 2D stylized look

**Option B: AI Generation (Post-Style Conversion)**
- Use AI model to generate normals from 2D images
- Options: Stable Diffusion ControlNet, specialized normal map generators
- Pros: Matches final art style, potentially more stylized
- Cons: Less geometrically accurate, additional processing step

**To Test:** Both options and compare results

**Tools to Evaluate:**
- Blender normal pass rendering (Option A)
- ControlNet Normal preprocessor (Option B)
- Substance Designer normal generation (Option B)
- GIMP normal map plugin (Option B)

### "Human Error" Variation Script
**Status:** ❓ TBD  
**Purpose:** Add frame jitter and imperfections to avoid rotoscoped look  
**Used In:** [[Pipeline2D]]

**Development Needed:**
- Custom script (Python likely)
- Randomize frame positions slightly
- Add line wobble/variation
- Timing variation (frame holds)

**Parameters to Control:**
- Jitter amount (pixel offset)
- Line edge variation
- Frame hold probability
- Noise seed for consistency

**Inspiration:** 90s anime limited animation techniques

### Re-timing Tool
**Status:** ❓ TBD  
**Purpose:** Adjust animation timing (frame holds, speed changes)  
**Used In:** [[Pipeline2D]]

**Option A: Automated (Preferred if Available)**
- AI-based re-timing (investigate availability)
- Preset timing patterns (anime-style holds)
- Batch processing

**Option B: Manual (DaVinci Resolve)**
- Import animation frames
- Manually adjust timing on timeline
- Export re-timed sequence

**DaVinci Resolve:** ✅ Confirmed as fallback  
**Documentation:** [DaVinci Resolve Manual](https://www.blackmagicdesign.com/products/davinciresolve)

**Decision Point:** Research automated options first; fall back to manual if needed

### Sprite Sheet Conversion
**Status:** ❓ TBD  
**Purpose:** Convert image sequence to sprite sheet for UE5  
**Used In:** [[Pipeline2D]]

**Options to Evaluate:**
- TexturePacker
- Shoebox
- Free Texture Packer
- Custom script (ImageMagick, Python PIL)
- UE5 built-in tools

**Requirements:**
- Consistent frame sizing
- Optimized packing
- Metadata export (frame positions)
- Compatible with UE5 Paper2D

---

## Materials & Rendering

### UE5 Material Editor
**Status:** ✅ Confirmed  
**Purpose:** Create master materials, color palette system, edge effects  
**Used In:** [[Materials3D]], [[Materials2D]]

**Key Features:**
- Material instances for variations
- Material parameter collections for global control
- Custom shader code (HLSL)

**Research Areas:**
- Edge mutation/clay-style materials
- Runtime color palette swapping
- Normal map integration for 2D sprites

### Clay-Style Material Resources
**Status:** ❓ TBD  
**Purpose:** Research for edge mutation/"human error" 3D materials  
**Used In:** [[Materials3D]]

**Options to Evaluate:**
- UE Marketplace assets (clay/toon shaders)
- Community tutorials (YouTube, forums)
- Custom shader development
- Vertex displacement techniques

**Goal:** Add subtle edge wobble/variation to 3D meshes mimicking hand-drawn look

---

## Post-Processing & Color

### Film LUT Sources
**Status:** ❓ TBD  
**Purpose:** Color grading lookup tables for film aesthetic  
**Used In:** [[PostProcessing]]

**Options to Evaluate:**
- Commercial LUT packs (film emulation)
- Free LUT libraries
- Custom LUT creation (DaVinci Resolve, Photoshop)
- Game-specific LUTs (Skyrim, Elden Ring inspired)

**Requirements:**
- Compatible with UE5 (3D LUT, .cube format)
- Moody/desaturated aesthetic
- Subtle grain/halation simulation

### Film Grain Resources
**Status:** ❓ TBD  
**Purpose:** Grain textures for post-processing  
**Used In:** [[PostProcessing]]

**Options to Evaluate:**
- UE5 built-in film grain
- Custom grain textures (scanned film, noise generation)
- Temporal vs. static grain

**Requirements:**
- High resolution
- Seamless tiling
- Adjustable intensity

---

## Development & Scripting

### Python
**Status:** ✅ Confirmed  
**Purpose:** Scripting and automation  
**Used In:** [[Pipeline2D]] (Blender automation, custom tools)

**Key Uses:**
- Blender API scripting
- Image processing (PIL/Pillow)
- Batch operations
- "Human error" variation script
- Pipeline automation

**Documentation:** [Python Documentation](https://docs.python.org/)

### Version Control (Git)
**Status:** ✅ Confirmed  
**Purpose:** Asset versioning and pipeline scripts  
**Used In:** All pipelines

**Notes:** 
- Track pipeline scripts
- Version control for critical assets
- Large file handling (Git LFS) if needed

---

## Decision Checklist

Use this checklist to track tool selection progress:

### 3D Pipeline
- [ ] Asset marketplace/source selected
- [ ] Texture editing tool selected
- [ ] Clay-style material approach determined

### 2D Pipeline
- [ ] Stable Diffusion implementation chosen
- [ ] LoRA training workflow established
- [ ] OpenPose/pose tool selected
- [ ] 2D→3D conversion tool selected
- [ ] Auto-rigging tool selected
- [ ] Animation source library selected
- [ ] Blender automation scripts developed
- [ ] Normal map generation approach decided (A or B)
- [ ] Deflickering tool selected (if needed)
- [ ] "Human error" script developed
- [ ] Re-timing approach decided (automated or manual)
- [ ] Sprite sheet tool selected

### Materials & Post
- [ ] Film LUT library selected/created
- [ ] Film grain resources acquired
- [ ] Edge mutation material researched

---

## Tool Acquisition Notes

**Budget Considerations:**
- Many tools have free alternatives (Blender, GIMP, free LUTs)
- Some require subscription (Substance Painter, commercial AI services)
- UE5 Marketplace assets vary widely in cost

**Learning Resources:**
- Official documentation linked above
- YouTube tutorials for specific workflows
- Community forums (Unreal forums, Blender Artists, Reddit)

**Integration Testing:**
- Test each tool with sample assets before committing to pipeline
- Validate automation capabilities early
- Benchmark performance (especially AI tools)

---

## Related Documentation

- **[[Pipeline3D]]** - See where each 3D tool is used
- **[[Pipeline2D]]** - See where each 2D tool is used
- **[[Materials3D]]** - Material system tool requirements
- **[[Materials2D]]** - Sprite material tool requirements
- **[[PostProcessing]]** - Post-processing tool requirements
