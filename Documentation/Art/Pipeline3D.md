# 3D Asset Pipeline

This document outlines the complete workflow for creating and implementing 3D assets in Lament, from sourcing premade assets through final in-engine integration.

**Related Documentation:**
- [[Tools]] - Software and tools reference
- [[Materials3D]] - Master materials and color palette system
- [[Lighting]] - Lighting approach decisions
- [[PostProcessing]] - Film effects and final polish

---

## Pipeline Overview

The 3D asset workflow emphasizes efficiency through asset modification rather than creation from scratch. Premade assets are simplified to solid-color albedo and elevated through UE5's material, lighting, and post-processing systems.

**Key Principles:**
- Source quality premade assets (lower poly preferred)
- Simplify textures to solid colors (minimal albedo detail)
- Apply master materials with runtime color palette system
- Test multiple lighting approaches
- Leverage post-processing for final visual quality

**Philosophy:** Simple base assets + sophisticated engine systems = distinctive visual style with minimal manual art creation

---

## Workflow Steps

### Step 1: Asset Sourcing

**Goal:** Find or acquire premade 3D assets suitable for modification

**Process:**
1. Identify asset needs (character, environment prop, enemy, etc.)
2. Search asset marketplaces/libraries (see [[Tools]] for sources)
3. Evaluate candidates based on criteria below
4. Download/purchase selected asset

**Selection Criteria:**
- **Polycount:** Lower poly preferred (specific range TBD - balance performance vs. shape quality)
  - Target: Maintains shape integrity without excessive triangles
  - Avoid: Ultra high-poly sculpts or extremely low-poly blocky models
  - Test range: TBD during first asset tests
- **Topology:** Clean mesh flow, good silhouette, no excessive subdivision
- **UV Mapping:** Clean UVs (though texture simplification may reduce importance)
- **License:** Commercial use for games allowed
- **Format:** FBX preferred for UE5 compatibility
- **Modularity:** Separate parts/meshes useful for variations (optional)

**Tips:**
- Search for "low poly" or "game ready" assets
- Stylized assets often better than photorealistic (simpler to modify)
- Inspect wireframe/polycount before purchasing
- Check reviews for quality issues

**✓ CHECKPOINT: Asset Selection Approval**
- Does the asset have good shape/silhouette?
- Is polycount acceptable?
- Does it fit the game's aesthetic direction?
- Is topology clean enough for potential edge mutation effects?

**Stop here if asset is unsuitable - find alternative before proceeding**

---

### Step 2: Import to UE5.7

**Goal:** Import asset into Unreal Engine with correct settings

**Process:**
1. Prepare asset file (FBX format)
2. Import to UE5.7 Content Browser
3. Configure import settings
4. Verify import success

**Import Settings:**
- **Skeletal vs. Static:** 
  - Static Mesh for non-animated props/environments
  - Skeletal Mesh if rigging/animation needed (rare for this pipeline)
- **Materials:** Import materials (will be replaced, but useful for reference)
- **Normals:** Import normals (may affect edge mutation experiments)
- **Scale:** Verify units match expected size in-game
- **Collision:** Auto-generate or import custom collision

**Initial Validation:**
- Check asset in viewport (lighting, scale, orientation)
- Test collision (if applicable)
- Verify materials imported correctly (even if temporary)

**✓ CHECKPOINT: Import Validation**
- Asset visible and correctly scaled?
- No import errors or missing elements?
- Topology intact (no corruption)?

**Common Issues:**
- Scale mismatch (adjust import scale)
- Inverted normals (flip in modeling software and re-import)
- Missing textures (expected - will replace anyway)

---

### Step 3: Texture Simplification

**Goal:** Reduce textures to solid colors for minimal albedo approach

**Approach A: External Editing (Photoshop, GIMP, etc.)**
1. Export current textures from UE5 or source files
2. Open in image editor (see [[Tools]])
3. Identify dominant color or select desired solid color
4. Fill texture with solid color (preserve alpha if needed)
5. Save and re-import to UE5

**Approach B: In-Engine Material Override**
1. Create new master material (see [[Materials3D]])
2. Replace texture sampling with solid color parameter
3. Apply material to asset
4. Skip texture editing entirely

**Recommended:** Approach B (material override) for flexibility and speed

**Color Selection:**
- Reference [[ColorPalettes]] for mood-appropriate colors
- Consider where asset will appear (world area, lighting conditions)
- Monochromatic palette default; analogous/complementary as needed
- Keep saturation lower (will be enhanced by lighting/post)

**Notes:**
- No detail maps needed (no roughness variation, no AO baking, no normal details)
- Preserve mesh normals for lighting variation
- If asset has multiple materials, can assign different solid colors per material slot

**✓ CHECKPOINT: Simplified Texture Review**
- Solid color looks appropriate for asset type?
- Shape still reads clearly without texture detail?
- Color fits intended palette/mood?

**If shape loses definition:** Consider slightly lighter/darker color to emphasize form, or rely on lighting (see Step 6)

---

### Step 4: Material Assignment

**Goal:** Apply master material with color palette system

**Process:**
1. Create or reference master material (see [[Materials3D]] for setup)
2. Create Material Instance from master material
3. Set color parameters for this specific asset
4. Assign Material Instance to mesh
5. Test in-engine with basic lighting

**Material Instance Parameters:**
- **Base Color:** Solid color from texture simplification step
- **Palette ID:** (If using runtime palette system) Which palette set to use
- **Edge Mutation Amount:** (If implemented) Intensity of edge wobble effect
- **Roughness:** Base roughness value (since no roughness map)
- **Metallic:** Typically 0 for most assets (matte look)

**Master Material Features:**
See [[Materials3D]] for detailed setup, but key features:
- Color palette parameter that can be swapped at runtime
- Optional edge mutation/distortion
- Simple lighting model (no complex subsurface or clearcoat)
- Support for toon/cel-shaded lighting (if chosen - see [[Lighting]])

**✓ CHECKPOINT: Material Look Verification**
- Material applied correctly to all parts?
- Color parameters working as expected?
- Asset still readable and visually clear?
- Ready for lighting tests?

**Common Issues:**
- Material slots mismatched (reassign to correct slots)
- Parameters not exposed in instance (check master material)
- Performance concerns (test in typical gameplay scenario)

---

### Step 5: Edge Mutation (Optional/Experimental)

**Goal:** Add subtle edge wobble/distortion for "human error" aesthetic

**Status:** Experimental - test with individual assets to determine if worth pursuing

**Approach:**
- Research clay-style materials and vertex/pixel displacement (see [[Tools]])
- Add edge distortion to master material shader
- Control via Material Instance parameter (enable/disable per asset)

**Techniques to Explore:**
- **Vertex Displacement:** Offset vertices slightly with noise (preserve silhouette)
- **Pixel/Normal Manipulation:** Distort edges at pixel level
- **World Position Offset:** Subtle wobble over time (animated imperfection)

**Considerations:**
- Performance cost (especially for many instances)
- May clash with clean 3D aesthetic (test carefully)
- Should be subtle - not distracting or "melting" look
- May work better for some assets (organic) than others (architecture)

**✓ CHECKPOINT: Effect Approval (If Used)**
- Edge mutation enhances or detracts from look?
- Performance acceptable?
- Consistent with overall art direction?
- Apply to all assets or selective use?

**Decision:** 
- [ ] Edge mutation adopted for all 3D assets
- [ ] Edge mutation used selectively (which types: _________)
- [ ] Edge mutation abandoned (clean edges preferred)

---

### Step 6: Lighting Testing

**Goal:** Determine which lighting approach works best for this asset type

**Three Approaches to Test:**
See [[Lighting]] for full details on each approach.

**A. Naturalistic Lighting**
- Standard PBR lighting with soft shadows
- 90s anime-inspired dramatic contrast
- Test asset under directional, point, and spot lights

**B. Cel-Shaded Lighting**
- Hard shadow boundaries, limited shade steps
- Requires material shader support (see [[Materials3D]])
- Test asset with toon lighting setup

**C. Hybrid Approach**
- Mix of naturalistic and cel-shaded elements
- May apply different approaches to 3D assets vs. 2D sprites
- Test asset with hybrid lighting setup

**Testing Process:**
1. Place asset in test level with controllable lighting
2. Try each approach (A, B, C)
3. Capture screenshots for comparison
4. Evaluate based on criteria below

**Evaluation Criteria:**
- Shape readability (does lighting enhance or obscure form?)
- Mood/atmosphere (fits game's aesthetic?)
- Consistency with other assets
- Visual interest (too flat or too busy?)
- Performance (shadow complexity, light count)

**✓ CHECKPOINT: Lighting Approach Decision**
- Which approach chosen: A / B / C / Other?
- Does this asset type need special lighting treatment?
- Document decision in [[Lighting]]

**Note:** This is often a project-wide decision, not per-asset, but testing with various asset types helps inform the choice.

---

### Step 7: Post-Processing Application

**Goal:** Apply film effects and finalize asset's in-engine look

**Process:**
1. Place asset in level with post-process volume
2. Apply post-processing settings (see [[PostProcessing]])
3. Evaluate final look with all effects active
4. Make final adjustments to material/lighting if needed

**Post-Processing Effects:**
See [[PostProcessing]] for detailed settings, key effects:
- **Film LUT:** Color grading for moody atmosphere
- **Film Grain:** Analog texture
- **Vignette:** Corner darkening
- **Lens Effects:** Corner softness, subtle distortion
- **Halation:** Highlight glow (film bloom)

**Final Look Validation:**
- Asset fits visually with game's aesthetic?
- Post effects enhance rather than obscure asset?
- Performance still acceptable with all effects active?
- Colors work well with LUT/grading?

**✓ CHECKPOINT: Final Asset Approval**
- Asset ready for gameplay integration?
- All materials, lighting, post-processing finalized?
- Performance benchmarked and acceptable?
- Documented any special setup or requirements?

**If approved:** Asset ready for level design / gameplay use  
**If not approved:** Identify which step needs revision and iterate

---

## Progress Tracking

### Technical Decisions
- [ ] Polycount guidelines finalized: _______ (target triangle range)
- [ ] Texture simplification workflow established: External editing / Material override
- [ ] Master material system implemented (see [[Materials3D]])
- [ ] Lighting approach chosen: Naturalistic / Cel-Shaded / Hybrid (see [[Lighting]])
- [ ] Edge mutation tested: Adopted / Selective use / Abandoned
- [ ] Post-processing settings documented (see [[PostProcessing]])

### Tool Selection
- [ ] Asset marketplace/source selected (see [[Tools]])
- [ ] Texture editing tool selected (if using external editing - see [[Tools]])
- [ ] Clay-style material resources found (if using edge mutation - see [[Tools]])

### Pipeline Testing
- [ ] First 3D asset completed through full pipeline: Date _______
- [ ] Pipeline documentation validated and updated based on test
- [ ] Performance benchmarked with typical asset count
- [ ] Workflow time estimated (for project planning)

### Asset Categories Completed
Track which types of assets have gone through pipeline:
- [ ] Environment props
- [ ] Architecture/structures  
- [ ] Characters (if using 3D characters)
- [ ] Enemies (if using 3D enemies)
- [ ] Interactive objects
- [ ] Special effects meshes

---

## Tips & Best Practices

### Asset Selection
- Build library of go-to asset sources (bookmark favorites)
- Keep polycount consistent across similar asset types
- Prioritize good silhouettes - they carry more weight than detail in this style

### Workflow Efficiency
- Create material instance templates for common asset types
- Use material instance parent/child hierarchies for variations
- Batch import similar assets together
- Keep import settings consistent (save presets)

### Iteration & Testing
- Test one asset fully before batch processing
- Create test levels for each asset category (props, characters, etc.)
- Compare new assets side-by-side with approved assets for consistency
- Screenshot before/after at each major step for documentation

### Performance Considerations
- Monitor triangle counts (stat commands in UE5)
- Use LODs if needed (though lower poly base may not require)
- Test edge mutation performance impact before wide adoption
- Batch similar materials to reduce draw calls

### Common Pitfalls
- **Over-simplifying color:** Solid colors can look flat - lighting is critical
- **Ignoring normals:** Even with flat colors, normal detail helps lighting
- **Inconsistent scale:** Verify world units early and often
- **Forgetting collision:** Non-rendering but essential for gameplay

---

## Non-Standard Workflows

### When to Deviate from Pipeline

**Custom 3D Modeling:**
If premade assets don't exist for specific needs:
1. Model in Blender (or other 3D software)
2. Keep polycount in target range
3. Use solid color materials during modeling
4. Export as FBX and resume at Step 2 (Import)

**Hero Assets:**
Critical assets (main character, key bosses) may need:
- Higher polycount budget
- Custom modeling/modification
- More detailed material setup
- Additional testing and iteration

**Interactive/Animated Assets:**
Assets with special requirements:
- Skeletal meshes for animation (rigging needed)
- Destructible meshes (fracture simulation)
- Morphing/blending (blend shapes)
- Document special workflows separately as needed

---

## Related Documentation

- **[[ArtOverview]]** - High-level vision and principles
- **[[Tools]]** - Software and asset sources
- **[[Materials3D]]** - Master material system setup
- **[[Lighting]]** - Lighting approach details and testing
- **[[PostProcessing]]** - Film effects settings
- **[[ColorPalettes]]** - Color selection guidelines
- **[[Pipeline2D]]** - Comparison with 2D sprite workflow

---

## Next Steps

1. Select initial 3D asset source/marketplace (see [[Tools]])
2. Download test asset and run through complete pipeline
3. Finalize polycount guidelines based on test results
4. Implement master material system (see [[Materials3D]])
5. Test all three lighting approaches (see [[Lighting]])
6. Document final settings and workflow refinements
7. Begin asset library creation for game levels
