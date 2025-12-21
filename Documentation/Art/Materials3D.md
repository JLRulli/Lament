# 3D Materials System

This document details the master material architecture and material systems for 3D assets (environment, props, and effects) in Lament, including the runtime color palette system and optional edge mutation effects.

**Related Documentation:**
- [[Pipeline3D]] - Where materials are applied in the workflow
- [[Materials2D]] - Comparison with 2D sprite material system
- [[Lighting]] - How materials interact with different lighting approaches
- [[ColorPalettes]] - Color palette definitions and mood guidelines
- [[Tools]] - Clay-style material resources

---

## Overview

The 3D material system prioritizes flexibility and simplicity through UE5's master material architecture. Materials use solid color or textured albedo with runtime color palette swapping, avoiding baked textures that limit iteration.

**Core Goals:**
- **Flexibility:** Change colors in-engine without re-authoring assets
- **Simplicity:** Solid color approach reduces texture memory and complexity
- **Consistency:** Master material ensures uniform look across all assets
- **Experimentation:** Easy to test edge mutation and lighting approaches

**Philosophy:** Materials elevate simple geometry through shader complexity, with optional texture detail for specific assets

---

## Master Material Architecture

### Master Material Structure

**Base Master Material:** `M_Master_3D` (name TBD)

**Material Instances Hierarchy:**
```
M_Master_3D (Master Material)
├── MI_Environment (Material Instance - Environment preset)
│   ├── MI_Environment_Props
│   ├── MI_Environment_Architecture
│   └── MI_Environment_Vegetation
└── MI_Effects (Material Instance - Special effects preset)
```

**Benefits of Hierarchy:**
- Shared base features from master
- Category-level presets (Environment, Effects, etc.)
- Specific overrides per asset or asset type
- Easy to propagate changes from top-level

**Note:** Characters are 2D sprites and use the [[Materials2D]] system

---

### Master Material Parameters

**Exposed Parameters (Material Instances can override):**

**Color & Palette:**
- `BaseColor` (Vector3/Color): Primary solid color
- `PaletteID` (Scalar/Integer): Which color palette set to use
- `UsePaletteSystem` (Bool): Enable/disable runtime palette swapping
- `ColorVariation` (Scalar): Slight color variation per instance (optional)

**Albedo Source:**
- `UseAlbedoTexture` (Bool): Use texture instead of solid color
- `AlbedoTexture` (Texture2D): Albedo texture map (when UseAlbedoTexture = true)
- `TexturePaletteTint` (Bool): Apply palette color as tint to texture
- `TextureTintStrength` (Scalar): How much palette affects texture (0 = no tint, 1 = full tint)

**Lighting Response:**
- `Roughness` (Scalar): Surface roughness (0 = smooth, 1 = rough)
- `Metallic` (Scalar): Metallic property (typically 0 for matte look)
- `SpecularIntensity` (Scalar): Specular highlight strength
- `TwoSided` (Bool): Render both sides of faces

**Edge Mutation (Optional/Experimental):**
- `EnableEdgeMutation` (Bool): Enable edge distortion effect (default: false)
- `EdgeMutationMode` (Integer/Enum): 0 = Persistent (static), 1 = Per-Frame (animated) (default: 0)
- `EdgeMutationIntensity` (Scalar): Amount of edge wobble
- `EdgeNoiseScale` (Scalar): Frequency of noise pattern
- `EdgeNoiseSeed` (Scalar): Variation seed (used in Persistent mode for per-instance variation)
- `EdgeMutationSpeed` (Scalar): Animation speed (used in Per-Frame mode only)

**Cel-Shading (If using cel-shaded lighting - see [[Lighting]]):**
- `EnableCelShading` (Bool): Enable toon shading
- `CelSteps` (Scalar/Integer): Number of shade bands (e.g., 3 for tri-tone)
- `CelThreshold` (Scalar): Shadow edge hardness

**Advanced:**
- `EmissiveColor` (Vector3/Color): Glow color (for special effects)
- `EmissiveIntensity` (Scalar): Glow strength
- `Opacity` (Scalar): Transparency (for special cases)

---

### Master Material Graph Overview

**High-Level Structure:**

1. **Base Color Calculation**
   - If `UseAlbedoTexture` = true: 
     - Sample `AlbedoTexture`
     - If `TexturePaletteTint` = true: Multiply/blend texture with palette color based on `TextureTintStrength`
     - Else: Use texture color directly
   - Else (solid color mode):
     - If `UsePaletteSystem` = true: Sample color from palette texture/lookup
     - Else: Use `BaseColor` parameter directly
   - Apply optional `ColorVariation` noise

2. **Lighting Model**
   - Standard PBR if naturalistic (see [[Lighting]])
   - Custom cel-shading if enabled (see [[Lighting]])
   - Hybrid approach if selected (see [[Lighting]])

3. **Edge Mutation (Optional)**
   - If `EnableEdgeMutation` = true:
     - Use World Position Offset or vertex displacement
     - Apply noise pattern to mesh edges/vertices
     - Controlled by intensity, scale, seed parameters

4. **Output**
   - Base Color → Material output
   - Roughness, Metallic, Specular → Material output
   - Emissive (if used)
   - Opacity (if used)

**Detailed graph implementation:** TBD during UE5 setup (document shader code here when built)

---

## Runtime Color Palette System

### Concept

Instead of baking colors into textures, materials reference a color palette that can be changed at runtime (per level, per mood, per gameplay state).

**Benefits:**
- Change entire level's color scheme without re-importing assets
- Swap palettes for different worlds/areas
- Dynamic mood shifts (e.g., "corruption" effect changes palette)
- Easy to test different color schemes during development

### Implementation Approach

**Option A: Material Parameter Collection (MPC)**

1. Create Material Parameter Collection: `MPC_ColorPalettes`
2. Define color parameters: `Palette_Color1`, `Palette_Color2`, ... `Palette_ColorN`
3. Master material samples from MPC based on `PaletteID`
4. Blueprints/code update MPC to swap palettes

**Pros:** Simple, centralized control, fast iteration  
**Cons:** Limited number of palettes, global (all instances see same palette)

**Option B: Texture-Based Palette Lookup**

1. Create palette texture: Each row = one palette, each pixel = one color
2. Master material samples texture using `PaletteID` and asset's color index
3. Swap palette by changing texture or updating which row to read

**Pros:** Many palettes possible, can be data-driven (external files)  
**Cons:** More complex setup, requires texture asset management

**Option C: Material Instances (Simplest)**

1. Create Material Instance per palette
2. Each instance has different `BaseColor` values
3. Assign appropriate instance to assets per level/area

**Pros:** No custom shader code, very simple  
**Cons:** Less flexible, harder to swap dynamically, more material instances to manage

**Recommended:** Start with **Option C** for simplicity, upgrade to **Option A** if dynamic swapping needed

### Palette Assignment Workflow

1. Define color palettes in [[ColorPalettes]]
2. Create Material Instance for each palette (e.g., `MI_Palette_Skyrim_Cold`, `MI_Palette_Elden_Golden`)
3. Assign palette-specific instances to assets based on level/area
4. (Optional) Implement dynamic swapping if needed (Blueprint/code)

**Example:**
- **World 1 (Cold, Nordic):** Uses `MI_Palette_Skyrim_Cold` (desaturated blues, grays)
- **World 2 (Warm, Decay):** Uses `MI_Palette_Elden_Golden` (amber, muted browns)
- Assets are the same, only material instance changes

---

## Albedo System (Solid Color & Texture)

### Why Solid Colors (Default Approach)

**Artistic Benefits:**
- Forces focus on shape, silhouette, and lighting (not texture detail)
- Unified, cohesive look across all assets
- Easier to maintain consistent art style
- Matches lower-poly aesthetic (detail comes from engine systems, not assets)

**Technical Benefits:**
- Minimal texture memory usage
- Fast iteration (change color in material, no texture re-export)
- Reduces asset creation complexity
- Performance-friendly (small textures or no textures)

**Inspiration:** Matches simplification seen in The Red Turtle character design (see [[ArtOverview]])

### Setting Up Solid Color Materials

**Method 1: No Texture (Pure Parameter)**
- Master material uses `BaseColor` parameter directly
- No texture sampling node needed
- Smallest memory footprint

**Method 2: Tiny Solid Color Texture**
- Create 1x1 or 4x4 texture per color
- Sample texture in material
- Allows traditional texture workflow if needed

**Recommended:** Method 1 (pure parameter) for flexibility and performance

**Material Graph:**
```
[Vector Parameter: BaseColor] → Base Color output
[Scalar Parameter: Roughness] → Roughness output
[Scalar Parameter: Metallic] → Metallic output
```

### Albedo Textures with Palette Integration

**When to Use Textures:**
- Assets requiring surface detail (terrain with subtle variation, architectural elements with patterns)
- Specific props where solid color feels too flat
- Special cases needing painted detail while maintaining palette cohesion

**Texture + Palette Workflow:**
1. Author albedo texture in Blender (grayscale or base color)
2. Export texture and import to UE5
3. Enable `UseAlbedoTexture` in Material Instance
4. Enable `TexturePaletteTint` to allow palette system to colorize/tint the texture
5. Adjust `TextureTintStrength`:
   - 0.0 = Texture color only (bypasses palette)
   - 0.5 = Balanced blend of texture and palette
   - 1.0 = Palette dominates (heavily tinted)

**Benefits:**
- Combines texture detail with runtime palette flexibility
- Can shift texture mood/color at runtime without re-authoring
- Maintains cohesive palette-driven aesthetic even with textures

**Performance Note:** Textures add memory overhead and sampling cost compared to solid colors. Use selectively.

**Default Approach:** Solid color remains primary for consistency, performance, and iteration speed.

### Handling Multi-Material Assets

For assets with multiple material slots (e.g., modular building with walls + roof + trim, or prop with base + details):

**Approach A: Separate Material Instances**
- Walls: `MI_Environment_Building_Walls` (primary color)
- Roof: `MI_Environment_Building_Roof` (secondary color)
- Trim: `MI_Environment_Building_Trim` (accent color)

**Approach B: Single Instance with Multiple Colors**
- Expose `BaseColor_Slot1`, `BaseColor_Slot2`, etc. in master material
- Use vertex colors or UV channels to determine which slot each face uses
- More complex shader, but single material instance

**Recommended:** Approach A (separate instances) for simplicity

---

## Edge Mutation Materials (Experimental)

### Concept

Add subtle edge wobble/distortion to 3D meshes to mimic hand-drawn "human error" and avoid sterile CG look.

**Inspiration:** Clay animation, hand-drawn cel animation line wobble, analog imperfection (see [[ArtOverview]])

**Status:** Experimental - test before wide adoption

### Edge Mutation Modes

**Mode 0: Persistent (Static Variation) - DEFAULT**
- Single frozen frame of noise applied to vertices
- Each object instance maintains consistent wobble across all frames
- Controlled by `EdgeNoiseSeed` to create variation between instances
- **Use Case:** Add subtle "handmade" imperfection without animation distraction
- **Performance:** Cheapest option (calculated once, can be baked)
- **Aesthetic:** Mimics slight variations in hand-sculpted clay or carved surfaces

**Mode 1: Per-Frame (Animated)**
- Continuously changing noise pattern driven by time
- Creates "breathing" or stop-motion clay-like wobble effect
- Controlled by `EdgeMutationSpeed` for animation rate (recommend: 0.1-0.5 for subtle)
- **Use Case:** Emphasize organic, living quality or dreamlike atmosphere
- **Performance:** More expensive (per-frame vertex calculation)
- **Aesthetic:** Mimics stop-motion animation frame-to-frame variation

**Recommendation:** 
- Default to Mode 0 (Persistent) for most assets
- Enable `EnableEdgeMutation` = false by default; enable selectively per asset
- Use Mode 1 sparingly for hero assets or special atmospheric areas

### Implementation Techniques

**Option 1: World Position Offset (Vertex Displacement)**

Offset vertices slightly using noise function.

**Material Graph - Persistent Mode (Mode 0):**
```
[World Position + (Object Position * 0.001) + EdgeNoiseSeed] 
  → [Noise Function: Simplex/Perlin] (scaled by EdgeNoiseScale)
  → [Multiply by EdgeMutationIntensity]
  → [Optional: Mask to affect edges/silhouette only]
  → World Position Offset output
```

**Material Graph - Per-Frame Mode (Mode 1):**
```
[World Position + (Time * EdgeMutationSpeed)] 
  → [Noise Function: Simplex/Perlin] (scaled by EdgeNoiseScale)
  → [Multiply by EdgeMutationIntensity]
  → [Optional: Mask to affect edges/silhouette only]
  → World Position Offset output
```

**Implementation:** Use `EdgeMutationMode` parameter with Branch/Switch node to select between static seed-based input and time-based input.

**Pros:** Affects mesh geometry, creates actual edge wobble visible in silhouette  
**Cons:** May cause mesh interpenetration if too strong, performance cost (especially Mode 1), can break tight collision if intensity too high

**Option 2: Pixel Manipulation**

Distort at pixel level without moving vertices:

**Material Graph (Simplified):**
```
[Screen Position or UVs]
  → [Noise Function]
  → [Offset base color sampling slightly]
  → Base Color output
```

**Pros:** No geometry changes, cheaper than vertex displacement  
**Cons:** Less dramatic effect, may not affect actual silhouette

### Testing Edge Mutation

**Test Setup:**
1. Create test level with sample 3D environment assets
2. Implement Option 1 (World Position Offset) with both modes
3. Expose parameters in Material Instance:
   - `EnableEdgeMutation` (default: false)
   - `EdgeMutationMode` (default: 0 - Persistent)
   - `EdgeMutationIntensity`, `EdgeNoiseScale`, `EdgeNoiseSeed`, `EdgeMutationSpeed`
4. Test with different asset types (organic rocks/trees vs. architecture)
5. Test Persistent mode with multiple instances (vary `EdgeNoiseSeed`)
6. Test Per-Frame mode at different speeds
7. Compare performance impact: Off vs. Persistent vs. Per-Frame

**Evaluation Criteria:**
- Persistent mode: Adds subtle uniqueness without distraction?
- Per-Frame mode: Enhances atmosphere or too distracting?
- Acceptable performance impact for each mode?
- Works for all asset types or only some (organic vs. hard-surface)?
- Intensity sweet spot identified (recommend: 0.5-2.0 units)?

**Decision Points:**
- [ ] Default: Enable or disable edge mutation for production assets?
- [ ] Persistent mode: Adopt for all/some/no environment assets?
- [ ] Per-Frame mode: Reserve for special cases only or allow broader use?
- [ ] Performance: Acceptable cost confirmed for target platform?

**Document findings in [[Pipeline3D]] progress tracking**

### Clay-Style Material Research

See [[Tools]] for resources on clay/toon shader development.

**Research Topics:**
- UE Marketplace clay/toon shaders (study techniques)
- Community tutorials (YouTube, forums)
- Custom HLSL/shader code for edge distortion
- Performance optimization techniques

**Reference Materials:**
- Aardman Animations (Wallace & Gromit) - clay aesthetic
- Stop-motion animation techniques
- Hand-drawn line wobble examples (90s anime)

---

## Lighting Integration

Materials must support the chosen lighting approach (see [[Lighting]] for full details):

### Naturalistic Lighting

**Material Requirements:**
- Standard PBR shading model (Lit material)
- Roughness/Metallic parameters functional

**No special shader code needed** - UE5 default lighting

### Cel-Shaded Lighting

**Material Requirements:**
- Custom shading model or modified light calculation
- `CelSteps` parameter controls number of shade bands
- `CelThreshold` parameter controls shadow edge hardness

**Material Graph (Simplified):**
```
[Light Vector dot Normal] 
  → [Quantize/Step function based on CelSteps]
  → [Hard threshold for shadow boundary]
  → Custom Lighting output
```

**Resources:** UE toon shading tutorials, cel-shader examples

### Hybrid Lighting

**Material Requirements:**
- Blend between PBR and cel-shaded
- Parameter to control blend amount
- May apply different approaches to different assets

**Implementation:** TBD based on testing (see [[Lighting]])

---

## Material Performance Considerations

### Optimization Tips

**Shader Complexity:**
- Keep master material as simple as possible (features can be toggled off)
- Use static switches for features (edge mutation, cel-shading) so unused code compiles out
- Avoid expensive operations (loops, complex math) if possible

**Instancing:**
- Use Material Instances extensively (not unique materials per asset)
- Batch assets with same material instance to reduce draw calls
- Share material instances across similar assets

**Texture Sampling:**
- Solid color approach minimizes texture reads
- If using palette texture, keep it small (e.g., 16x16 pixels)
- Avoid multiple texture lookups if possible

**Testing:**
- Use UE5 shader complexity view to identify expensive materials
- Profile with stat commands (`stat RHI`, `stat SceneRendering`)
- Test with typical scene asset counts (not just single asset)

### Performance Targets

**TBD:** Establish performance benchmarks during initial testing

**Metrics to Track:**
- Frame time impact of master material vs. simple unlit material
- Edge mutation performance cost (if used)
- Cel-shading performance cost (if used)
- Draw call count with material instancing

**Document findings:** Update this section with actual performance data after testing

### Performance Comparisons

**Albedo Approach:**
- **Solid Color (Parameter):** Fastest - no texture sampling, minimal memory
- **Solid Color (Palette System):** Fast - single palette texture lookup
- **Albedo Texture (No Tint):** Moderate - standard texture sampling cost
- **Albedo Texture (Palette Tint):** Moderate-High - texture sample + palette lookup + blend operation

**Recommendation:** Default to solid color; use textures only where detail justifies cost.

---

**Edge Mutation Modes:**
- **Disabled:** Baseline - no additional cost
- **Persistent Mode:** Low - noise calculated per-vertex but can be cached/baked
- **Per-Frame Mode:** Medium-High - per-vertex noise calculation every frame

**Recommendation:** 
- Enable edge mutation selectively, not globally
- Prefer Persistent mode for ambient detail
- Reserve Per-Frame mode for <10 hero assets per scene or special atmospheric zones

**Estimated Impact (TBD - validate during testing):**
- Persistent edge mutation: ~5-10% shader cost increase
- Per-Frame edge mutation: ~15-25% shader cost increase
- Texture albedo: +memory cost (varies by texture size/compression)

---

## Material Setup Workflow

### Initial Setup (One-Time)

1. **Create Master Material** in UE5 Content Browser
   - Name: `M_Master_3D`
   - Parent: Default Lit (or Custom if cel-shading)
   - Set up base parameters and graph (see Architecture section above)

2. **Create Material Parameter Collection** (if using palette system)
   - Name: `MPC_ColorPalettes`
   - Add color parameters for palettes

3. **Create Base Material Instances**
   - `MI_Environment` (preset for environment assets)
   - `MI_Effects` (preset for special effects)

4. **Test Material** with sample asset
   - Verify parameters work
   - Test lighting response
   - Test edge mutation (if implemented)

### Per-Asset Workflow

See [[Pipeline3D]] Step 4 for full context.

1. **Create Material Instance** from appropriate parent (e.g., `MI_Environment`)
2. **Name Instance** descriptively (e.g., `MI_Environment_Tree_01`)
3. **Set Parameters:**
   - `BaseColor` (solid color from palette - see [[ColorPalettes]])
   - `Roughness` (default: ~0.7 for matte)
   - `Metallic` (default: 0 for non-metallic)
   - (Optional) `EnableEdgeMutation`, `EdgeMutationIntensity`
4. **Assign to Asset** mesh in UE5
5. **Test in Level** with lighting and post-processing

---

## Comparison with 2D Materials

See [[Materials2D]] for 2D sprite material system.

**Key Differences:**

| Feature | 3D Materials (This Doc) | 2D Materials ([[Materials2D]]) |
|---------|------------------------|-------------------------------|
| **Asset Scope** | Environment, props, effects only | Characters, sprites, UI elements |
| **Base Asset** | 3D mesh geometry | 2D sprite texture |
| **Albedo** | Solid color parameter OR texture (palette-tinted) | Sprite sheet texture |
| **Lighting** | PBR or cel-shaded on 3D geometry | Normal map-based (pseudo-3D) |
| **Normal Maps** | Not used (geometry provides all shape) | Required for lighting response |
| **Transparency** | Rare (only special cases like effects) | Common (sprite edges, alpha) |
| **Edge Mutation** | World Position Offset (Persistent or Per-Frame modes) | Not applicable (pixel-based edges) |
| **Palette System** | Runtime parameter swapping, can tint textures | Same approach possible |
| **Performance** | Geometry + lighting cost, optional shader complexity | Sprite rendering, normal map sampling |

**Shared Concepts:**
- Both use master material approach for consistency
- Both support runtime color palette system
- Both integrate with same lighting setup (see [[Lighting]])
- Both use solid colors (3D = parameter, 2D = art style)

---

## Progress Tracking

### Implementation Status
- [ ] Master material created and tested
- [ ] Material Parameter Collection set up (if using)
- [ ] Base Material Instances created (Environment, Effects)
- [ ] Color palette system implemented (Option A / B / C - see above)
- [ ] Albedo texture system implemented and tested
- [ ] Texture palette tinting system functional
- [ ] Edge mutation Persistent mode implemented and tested
- [ ] Edge mutation Per-Frame mode implemented and tested
- [ ] Lighting approach integrated: Naturalistic / Cel-Shaded / Hybrid (see [[Lighting]])
- [ ] Performance benchmarked and optimized
- [ ] Performance comparison validated: Solid vs. Texture, Persistent vs. Per-Frame

### Decisions Made
- [ ] Palette system approach chosen: MPC / Texture / Instances
- [ ] Edge mutation default settings decided: Enabled/Disabled, Mode preference (Persistent/Per-Frame/Both)
- [ ] Lighting integration: Naturalistic / Cel-Shaded / Hybrid
- [ ] Performance acceptable: Yes / Needs optimization

### Documentation
- [ ] Master material graph documented (shader code/screenshot)
- [ ] Material instance naming convention established
- [ ] Per-asset setup workflow validated
- [ ] Performance data recorded

---

## Related Documentation

- **[[Pipeline3D]]** - When and how to apply materials
- **[[Materials2D]]** - 2D sprite material system
- **[[Lighting]]** - Lighting approaches and material integration
- **[[ColorPalettes]]** - Color selection and palette definitions
- **[[Tools]]** - Clay-style material research resources
- **[[PostProcessing]]** - How materials interact with post effects

---

## Next Steps

1. Create master material in UE5 with base parameters
2. Implement solid color albedo approach (test with sample asset)
3. Set up color palette system (choose Option A/B/C)
4. Research and test edge mutation (optional)
5. Integrate with chosen lighting approach (see [[Lighting]])
6. Create base Material Instances for asset categories
7. Document final master material graph and parameters
8. Test performance and optimize as needed
