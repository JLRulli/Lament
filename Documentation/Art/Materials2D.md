# 2D Sprite Materials System

This document details the material setup for 2D sprite-based characters and animations in Lament, with focus on normal map integration for dynamic lighting.

**Related Documentation:**
- [[Pipeline2D]] - Where sprite materials are applied in the workflow
- [[Materials3D]] - Comparison with 3D material system
- [[Lighting]] - How dynamic lights interact with sprite normal maps
- [[Tools]] - Normal map generation tools

---

## Overview

The 2D sprite material system enables dynamic lighting response on flat 2D sprites through normal map integration. This creates depth and atmosphere while maintaining the 2D art style.

**Core Goals:**
- **Dynamic Lighting:** 2D sprites react to moving lights in 3D space
- **Depth Illusion:** Normal maps create illusion of 3D form on flat sprites
- **Art Style Consistency:** Lighting enhances rather than fights the 2D aesthetic
- **Performance:** Efficient sprite rendering with normal map support

**Philosophy:** Flat 2D art elevated by 3D lighting techniques for best of both worlds

---

## Sprite Material Architecture

### Master Material for Sprites

**Base Master Material:** `M_Master_Sprite` (name TBD)

**Material Type:** Sprite (Paper2D compatible) or Translucent (for alpha)

**Material Instances:**
```
M_Master_Sprite (Master Material)
├── MI_Character_Sprite (Character preset)
│   ├── MI_Player_Sprite
│   ├── MI_Companion_Sprite
│   └── MI_Enemy_Sprite
└── MI_Effect_Sprite (Special effects preset)
```

**Benefits:**
- Shared features across all sprites (normal map integration, lighting response)
- Category-level presets for common configurations
- Easy to update all sprites by modifying master

---

### Master Material Parameters

**Exposed Parameters:**

**Textures:**
- `AlbedoTexture` (Texture2D): Sprite sheet or single sprite
- `NormalMap` (Texture2D): Normal map for lighting (required)
- `UseNormalMap` (Bool): Enable/disable normal map effect

**Color & Palette:**
- `TintColor` (Vector3/Color): Color tint overlay (white = no tint)
- `PaletteID` (Scalar): Runtime palette swapping (optional - see [[Materials3D]])
- `UsePaletteSystem` (Bool): Enable runtime color palette

**Lighting Response:**
- `NormalStrength` (Scalar): Intensity of normal map effect (0 = flat, 1 = full)
- `LightingIntensity` (Scalar): How strongly sprite responds to lights
- `AmbientOcclusion` (Scalar): Darken base (fake AO effect)
- `ReceiveShadows` (Bool): Accept shadows from 3D objects

**Rendering:**
- `Opacity` (Scalar): Sprite alpha (if using alpha channel)
- `AlphaCutoff` (Scalar): Threshold for alpha masking (sharp vs. soft edges)
- `TwoSided` (Bool): Render both sides (typically true for sprites)

**Advanced:**
- `EmissiveColor` (Vector3/Color): Glow/self-illumination
- `EmissiveIntensity` (Scalar): Glow strength
- `SpecularIntensity` (Scalar): Specular highlights (optional - may look odd on 2D)

---

### Master Material Graph Overview

**High-Level Structure:**

1. **Albedo (Base Color)**
   - Sample `AlbedoTexture` (sprite sheet)
   - Apply `TintColor` if needed
   - (Optional) Apply palette color if `UsePaletteSystem` enabled

2. **Normal Map**
   - Sample `NormalMap` texture
   - Unpack normal (tangent space)
   - Blend with flat normal based on `NormalStrength`
   - If `UseNormalMap` = false: Use flat normal (0, 0, 1)

3. **Lighting Calculation**
   - Use normal to calculate light response
   - Apply `LightingIntensity` to control brightness variation
   - (Optional) Apply `AmbientOcclusion` to darken

4. **Transparency**
   - Sample alpha channel from `AlbedoTexture`
   - Apply `Opacity` multiplier
   - Use `AlphaCutoff` for masking if needed

5. **Output**
   - Base Color → Material output
   - Normal → Material output (critical for lighting)
   - Emissive (if used)
   - Opacity → Opacity output

**Detailed graph implementation:** TBD during UE5 setup (document when built)

---

## Normal Map Integration

### Why Normal Maps for 2D Sprites

**Problem:** Flat 2D sprites don't respond to dynamic lighting (always same brightness)

**Solution:** Normal maps encode surface direction information, allowing lighting calculations

**Benefits:**
- Sprites react to moving lights in 3D space
- Creates depth illusion (character appears to have form)
- Atmospheric lighting (torches, firelight, environmental lights)
- Consistent with 3D lit environment

**Inspiration:** Modern 2D games with dynamic lighting (e.g., Hollow Knight, Dead Cells)

### Normal Map Generation Approaches

See [[Pipeline2D]] Step 9 for full workflow details.

**Option A: From 3D Model (Blender Render Pass)**
- Render normal pass alongside albedo during Blender export
- Geometrically accurate normals
- Consistent with 3D rig

**Option B: AI-Generated (Post-2D Conversion)**
- Generate normals from final 2D stylized art
- Matches art style better
- May be less accurate

**Decision:** Test both and choose based on results (see [[Pipeline2D]] progress tracking)

### Normal Map Format

**Technical Requirements:**
- **Format:** RGB texture (8-bit per channel typically sufficient)
- **Color Space:** Tangent space normals (most common)
  - R channel: X direction (left-right)
  - G channel: Y direction (up-down)
  - B channel: Z direction (depth/out-of-surface)
- **Default Color:** RGB(128, 128, 255) or normalized (0.5, 0.5, 1.0) = flat surface
- **Compression:** BC5 (two-channel) or BC7 (higher quality) in UE5

**UE5 Import Settings:**
- Texture Group: `Normal Map`
- sRGB: **Disabled** (critical - normals are directional data, not color)
- Compression: BC5 or BC7

---

## Dynamic Lighting Setup

### UE5 Paper2D Configuration

**Sprite Setup:**
1. Import sprite sheet texture (albedo) and normal map texture
2. Create Paper2D Flipbook or Sprite asset
3. Assign sprite material (Material Instance from `M_Master_Sprite`)
4. Set material parameters (normal map texture, strength, etc.)

**Flipbook Animation:**
- Each frame references different UV region of sprite sheet
- Normal map should match sprite sheet layout (same frame positions)
- Material samples both albedo and normal from same UV coordinates

### Lighting in UE5

**Light Types That Affect Sprites:**

**Point Lights:**
- Good for torches, fires, magical effects
- Attenuation radius controls range
- Color and intensity create mood

**Spot Lights:**
- Directional lighting (e.g., beam of light)
- Cone angle and attenuation

**Directional Lights:**
- Main environmental lighting (e.g., sun, moon)
- Affects all sprites uniformly

**Testing Lighting:**
1. Place sprite in test level
2. Add various light types (point, spot, directional)
3. Move lights around sprite
4. Observe normal map lighting response
5. Adjust `NormalStrength` and `LightingIntensity` for desired look

**✓ Checkpoint: Lighting Response Validation**
- Sprite responds to dynamic lights correctly?
- Normal map effect looks natural (not too flat, not too extreme)?
- Lighting enhances depth illusion?
- Performance acceptable with multiple sprites and lights?

---

## Sprite Sheet Workflow

### Albedo Sprite Sheet

Created in [[Pipeline2D]] Step 12 (sprite sheet conversion).

**Format:**
- PNG with alpha (transparency at edges)
- Power-of-two dimensions (1024, 2048, 4096)
- Frames arranged in grid or packed layout
- Metadata defines frame positions

**UE5 Import:**
- Import as Texture2D
- Texture Group: `2D Pixels (Unfiltered)` for pixel-perfect, or `World` for filtered
- sRGB: **Enabled** (albedo is color data)

### Normal Map Sprite Sheet

Generated in [[Pipeline2D]] Step 9 (normal map generation).

**Format:**
- **Must match albedo sprite sheet layout exactly** (same frame positions)
- RGB texture (no alpha needed typically)
- Same dimensions as albedo sprite sheet
- Power-of-two dimensions

**Alignment Critical:**
- Frame 1 in albedo must align with Frame 1 in normal map
- UVs sample both textures at same coordinates
- Misalignment = lighting on wrong part of sprite

**UE5 Import:**
- Import as Texture2D
- Texture Group: `Normal Map`
- sRGB: **Disabled**
- Compression: BC5 or BC7

### Material Instance Setup

Per sprite/character:

1. **Create Material Instance** from `MI_Character_Sprite` (or appropriate parent)
2. **Name Instance:** `MI_Player_Idle`, `MI_Enemy_Walk`, etc.
3. **Set Parameters:**
   - `AlbedoTexture` → Sprite sheet texture
   - `NormalMap` → Normal map sprite sheet texture
   - `NormalStrength` → Adjust to taste (default: 0.7-1.0)
   - `LightingIntensity` → Adjust lighting response (default: 1.0)
   - `Opacity` → Usually 1.0 (alpha from texture)
4. **Assign to Flipbook/Sprite**

---

## Comparison with 3D Materials

See [[Materials3D]] for 3D material system.

**Key Differences:**

| Feature | 2D Sprite Materials (This Doc) | 3D Materials ([[Materials3D]]) |
|---------|-------------------------------|-------------------------------|
| **Base Asset** | Sprite texture (2D image) | 3D mesh with geometry normals |
| **Albedo Source** | Sprite sheet texture | Solid color parameter |
| **Normal Source** | Normal map texture (required) | Mesh geometry (optional normal map) |
| **Lighting** | Normal map-based (fake 3D) | True 3D lighting on mesh |
| **Transparency** | Common (sprite edges) | Rare (special cases only) |
| **UV Mapping** | Sprite sheet frames | Standard mesh UVs |
| **Paper2D** | Yes (flipbooks/sprites) | No (static/skeletal meshes) |

**Shared Concepts:**
- Both use master material architecture
- Both can support runtime color palettes (optional)
- Both integrate with same lighting setup (see [[Lighting]])
- Both prioritize simplicity (sprites = flat art, 3D = solid colors)

---

## Advanced Techniques

### Specular Highlights (Optional)

**Concept:** Add shiny highlights to sprites (e.g., metallic armor, wet surfaces)

**Implementation:**
- Add specular calculation in material (based on normal and view direction)
- Expose `SpecularIntensity` parameter
- May look odd on flat 2D art (test carefully)

**Recommendation:** Use sparingly - may break 2D aesthetic if too strong

### Emissive Effects

**Concept:** Self-illuminated parts of sprite (glowing eyes, magic effects)

**Implementation:**
- Create emissive mask texture (where to glow)
- Sample mask and multiply by `EmissiveColor` and `EmissiveIntensity`
- Add to Emissive output

**Use Cases:**
- Character special states (powered up, damaged)
- Magical effects
- Environmental sprites (glowing crystals, lanterns)

### Runtime Palette Swapping

**Concept:** Same as 3D materials - change sprite colors at runtime

**Implementation Options:**

**Option A: Tint Color (Simplest)**
- Use `TintColor` parameter to overlay color
- Multiplicative blending: white tint = original colors, red tint = reddish sprite
- Limited control but very simple

**Option B: Palette Lookup (Advanced)**
- Similar to [[Materials3D]] palette system
- Replace specific colors in sprite with palette colors
- Requires shader code to identify and replace colors

**Recommendation:** Option A (tint) for simple cases, Option B for full palette control

---

## Performance Considerations

### Optimization Tips

**Texture Memory:**
- Sprite sheets more efficient than individual textures (fewer draw calls)
- Use appropriate texture compression (BC7 for albedo with alpha, BC5 for normals)
- Mipmap settings: Enable for filtered sprites, disable for pixel-perfect

**Draw Calls:**
- Batch sprites with same material instance
- Use sprite sheet atlases to reduce texture swaps
- Consider instancing for many identical sprites

**Shader Complexity:**
- Normal map lighting is relatively cheap (standard feature)
- Avoid complex custom lighting if possible
- Use static switches to disable unused features (emissive, specular)

**Transparency:**
- Translucent materials are more expensive than opaque
- Use Masked blend mode if possible (hard edges, no partial transparency)
- Minimize overdraw (many transparent sprites layered)

### Performance Testing

**Metrics to Track:**
- Frame time with many sprites on-screen
- Draw call count (stat SceneRendering)
- Texture memory usage (stat Streaming)
- GPU cost (stat GPU)

**Benchmarks:** TBD - establish during initial sprite testing

**Document findings:** Update this section with actual performance data

---

## Material Setup Workflow

### Initial Setup (One-Time)

1. **Create Master Material** in UE5 Content Browser
   - Name: `M_Master_Sprite`
   - Material Domain: Surface
   - Blend Mode: Translucent (for alpha) or Masked
   - Shading Model: Default Lit
   - Set up base graph (albedo, normal, lighting - see Architecture above)

2. **Create Base Material Instances**
   - `MI_Character_Sprite` (characters/creatures)
   - `MI_Effect_Sprite` (special effects)

3. **Test Material** with sample sprite
   - Create simple test sprite with normal map
   - Verify normal map lighting works
   - Test with dynamic lights

### Per-Sprite Workflow

See [[Pipeline2D]] Step 13 for full context.

1. **Import Textures:**
   - Albedo sprite sheet (color + alpha)
   - Normal map sprite sheet (matching layout)

2. **Create Material Instance** from `MI_Character_Sprite`
   - Name: `MI_[CharacterName]_[AnimationName]`

3. **Set Parameters:**
   - Assign albedo and normal map textures
   - Adjust `NormalStrength` (test with lights)
   - Set other parameters as needed

4. **Create Flipbook/Sprite:**
   - Import sprite sheet into Paper2D
   - Define frame regions (from sprite sheet metadata)
   - Assign material instance

5. **Test in Level:**
   - Place in test level with various lights
   - Validate lighting response
   - Adjust material parameters if needed

---

## Troubleshooting

### Common Issues

**Normal Map Not Working:**
- Check sRGB is **disabled** on normal map texture
- Verify normal map texture assigned to material parameter
- Check `UseNormalMap` parameter is true
- Ensure normal map matches sprite sheet layout

**Lighting Too Flat:**
- Increase `NormalStrength` parameter
- Check normal map is not default flat (all blue)
- Increase `LightingIntensity`
- Add stronger lights to scene

**Lighting Too Extreme:**
- Decrease `NormalStrength` parameter
- Decrease `LightingIntensity`
- Check normal map isn't inverted (green channel may need flip)

**Sprite Edges Look Wrong:**
- Check alpha channel in albedo texture
- Adjust `AlphaCutoff` for masked materials
- Verify blend mode (Translucent vs. Masked)

**Misaligned Normal Map:**
- Verify sprite sheet and normal map have identical layouts
- Check UV coordinates in flipbook/sprite setup
- Regenerate normal map with correct frame positions

**Performance Issues:**
- Reduce sprite sheet texture sizes
- Use more aggressive compression
- Batch sprites with same material
- Reduce number of dynamic lights

---

## Progress Tracking

### Implementation Status
- [ ] Master sprite material created and tested
- [ ] Normal map integration working correctly
- [ ] Base Material Instances created (Character, Effect)
- [ ] Dynamic lighting tested with sprites
- [ ] Performance benchmarked

### Decisions Made
- [ ] Normal map generation approach: 3D-based / AI-generated (see [[Pipeline2D]])
- [ ] Palette system implemented: Yes (Tint / Lookup) / No
- [ ] Specular highlights used: Yes / No
- [ ] Performance acceptable: Yes / Needs optimization

### Documentation
- [ ] Master material graph documented (shader code/screenshot)
- [ ] Material instance naming convention established
- [ ] Per-sprite setup workflow validated
- [ ] Performance data recorded

---

## Related Documentation

- **[[Pipeline2D]]** - Sprite creation workflow, normal map generation
- **[[Materials3D]]** - 3D material system comparison
- **[[Lighting]]** - How lights interact with normal-mapped sprites
- **[[Tools]]** - Normal map generation tools
- **[[ArtOverview]]** - 2D art style and aesthetic goals

---

## Next Steps

1. Create master sprite material in UE5 with normal map support
2. Test with sample sprite and normal map (validate lighting)
3. Create base Material Instances for categories
4. Complete first full sprite animation through [[Pipeline2D]]
5. Determine normal map generation approach (3D vs. AI)
6. Test dynamic lighting with multiple sprites and light sources
7. Document final material graph and parameters
8. Benchmark performance and optimize as needed
