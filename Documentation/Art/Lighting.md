# Lighting Approaches

This document explores three different lighting approaches for Lament and provides a framework for testing and choosing the final implementation.

**Related Documentation:**
- [[Materials3D]] - How 3D materials integrate with lighting
- [[Materials2D]] - How 2D sprite normals interact with lights
- [[ArtOverview]] - 90s anime lighting inspiration
- [[PostProcessing]] - Post effects that complement lighting

---

## Overview

Lighting is critical to Lament's moody, atmospheric aesthetic. Three primary approaches are being considered, each with different strengths and visual characteristics.

**Goal:** Test all three approaches and select the one (or hybrid) that best achieves the art direction goals.

**Key Considerations:**
- **Mood & Atmosphere:** Supports melancholic, mysterious, dramatic tone
- **Art Style Consistency:** Works with lower-poly 3D and 2D sprites
- **90s Anime Influence:** High contrast, dramatic shadows, colored lighting
- **Performance:** Maintains target frame rate with dynamic lights
- **Iteration Speed:** Easy to adjust and refine during development

---

## Three Approaches to Test

### Approach A: Naturalistic Lighting

**Description:** Physically-based rendering (PBR) with realistic light behavior, but styled toward dramatic 90s anime aesthetics.

**Characteristics:**
- Soft shadow edges (penumbra)
- Realistic light falloff (inverse square)
- Subtle gradients in shading
- Natural color blending
- High dynamic range (bright highlights, deep shadows)

**Inspiration:**
- 90s anime dramatic lighting (high contrast, colored key lights)
- Moody film photography (see [[ArtOverview]])
- Naturalistic but exaggerated for mood

**Implementation:**
- Use UE5 default Lit shading model
- Standard directional, point, and spot lights
- Adjust light intensity, color, and attenuation for drama
- No custom shader code needed

**Pros:**
- Familiar, well-supported by engine
- Easy to iterate (standard UE5 lighting tools)
- Works well with PBR materials
- Natural-looking depth and form
- Flexible light types (directional, point, spot)

**Cons:**
- May look too realistic for stylized game
- Soft shadows might lack punch/drama
- Can be harder to control mood (requires careful tuning)
- Gradient shading might not match 2D art style

**Best For:**
- Realistic but atmospheric mood
- Detailed 3D environments
- If going for film-like aesthetic

---

### Approach B: Cel-Shaded Lighting

**Description:** Toon/anime-style shading with hard shadow boundaries and limited shade steps (e.g., light, mid, dark).

**Characteristics:**
- Hard shadow edges (no gradients)
- Limited shade steps (typically 2-4 bands: highlight, mid-tone, shadow, core shadow)
- Flat color regions
- Optional rim lighting (outline in light)
- Stylized, graphic look

**Inspiration:**
- Traditional anime cel animation
- Games like Jet Set Radio, Breath of the Wild, Borderlands
- Simplified, graphic aesthetic

**Implementation:**
- Custom shading model in materials (see [[Materials3D]])
- Quantize lighting calculation into steps
- Hard threshold for shadow boundaries
- May require custom shader code (HLSL)

**Material Graph (Simplified):**
```
[Light Vector dot Normal]
  → [Quantize into N steps (e.g., 3 bands)]
  → [Apply hard threshold]
  → Shading output
```

**Pros:**
- Strong, graphic visual style
- Clear readability (shapes very defined)
- Matches anime aesthetic directly
- Consistent with 2D art style
- Lower performance cost (simpler shading)

**Cons:**
- Less depth/realism in 3D assets
- Can look overly simplistic
- Hard to make moody/atmospheric (flatter look)
- May clash with film post-processing (grain, etc.)
- Requires custom shader development

**Best For:**
- Strong anime/cartoon aesthetic
- Highly stylized, graphic look
- If prioritizing readability over realism

---

### Approach C: Hybrid Lighting

**Description:** Combine naturalistic and cel-shaded approaches selectively for best of both worlds.

**Characteristics:**
- Mix of soft and hard shadows
- Naturalistic lighting with stylized accents
- Different approaches for 3D vs. 2D assets
- Cel-shaded character outlines with naturalistic environment lighting
- Artistic control over which elements are stylized

**Inspiration:**
- Modern anime-styled games (Guilty Gear Xrd, Granblue Fantasy Versus)
- Mixing 2D and 3D aesthetics seamlessly
- Studio Ghibli films (soft but stylized lighting)

**Implementation Options:**

**Option 1: Asset-Based**
- 3D environments: Naturalistic lighting
- 2D sprites: Cel-shaded or stylized response
- Characters: Cel-shaded outlines + naturalistic shading

**Option 2: Light-Based**
- Key lights: Naturalistic (directional sun, main scene lighting)
- Fill/accent lights: Cel-shaded or stylized (rim lights, colored accents)

**Option 3: Material-Based**
- Some materials use naturalistic shading
- Others use cel-shaded (per Material Instance setting)
- Mix within single scene

**Pros:**
- Flexibility (best of both approaches)
- Can tailor lighting per asset type
- Balances realism and style
- Allows for creative expression
- Can adjust balance during development

**Cons:**
- More complex to set up
- Requires careful planning (can look inconsistent if not managed)
- May need multiple material variants
- Harder to establish clear art direction (more variables)

**Best For:**
- Want atmospheric naturalism + graphic style
- Mixing 3D and 2D assets with different needs
- Flexible, experimental approach

---

## Testing Framework

### Test Setup

**Test Level:**
Create dedicated lighting test level:
- Variety of asset types (3D props, environment, 2D sprites)
- Controlled scene (neutral gray background)
- Standardized camera angles
- Reference lighting setups for each approach

**Assets to Test:**
- 3D character (if using)
- 3D environment prop (simple, medium complexity)
- 2D sprite character (with normal maps - see [[Materials2D]])
- 2D sprite effect (optional)

**Lighting Setups to Test:**

**Setup 1: Directional Light Only**
- Single directional light (sun/moon)
- Test shadow hardness, intensity
- Observe form definition on assets

**Setup 2: Point Light**
- Single point light (torch, magic effect)
- Test falloff, color, range
- Observe how light wraps around forms

**Setup 3: Multiple Lights**
- Directional + point + spot
- Test color mixing, fill lighting
- Observe complex lighting scenarios

### Testing Procedure

**For Each Approach (A, B, C):**

1. **Implement Approach**
   - Set up materials (see [[Materials3D]], [[Materials2D]])
   - Configure lights
   - Apply to test assets

2. **Capture Screenshots**
   - All three lighting setups
   - Multiple camera angles
   - High resolution for comparison

3. **Evaluate Based on Criteria** (see below)

4. **Document Findings**
   - What works well?
   - What doesn't work?
   - Technical challenges?
   - Artistic assessment?

### Evaluation Criteria

**Visual Quality:**
- [ ] Supports moody, atmospheric tone?
- [ ] High contrast and drama (90s anime style)?
- [ ] Shape readability (clear silhouettes)?
- [ ] Depth and form definition?
- [ ] Consistency across 3D and 2D assets?

**Art Direction Alignment:**
- [ ] Matches 90s anime inspiration? (see [[ArtOverview]])
- [ ] Works with moody film aesthetic? (see [[ArtOverview]])
- [ ] Complements solid color / lower poly style?
- [ ] Supports color palette mood (see [[ColorPalettes]])?

**Technical Performance:**
- [ ] Acceptable frame rate with multiple lights?
- [ ] Dynamic lights performant (moving torches, etc.)?
- [ ] Shadow rendering cost reasonable?
- [ ] Easy to iterate and adjust?

**Integration:**
- [ ] Works with 3D materials? (see [[Materials3D]])
- [ ] Works with 2D sprite normal maps? (see [[Materials2D]])
- [ ] Complements post-processing? (see [[PostProcessing]])
- [ ] Fits into existing pipeline?

**Workflow:**
- [ ] Easy to set up and configure?
- [ ] Artists/designers can adjust without programmer?
- [ ] Clear parameters for tweaking mood?
- [ ] Supports rapid iteration?

---

## 90s Anime Lighting Techniques

Regardless of approach chosen, incorporate these 90s anime lighting principles:

### High Contrast

**Technique:** Strong difference between light and shadow areas

**Implementation:**
- Increase light intensity
- Reduce ambient/fill lighting
- Use deep shadows
- Avoid flat, even lighting

**Example:** Character lit from one side, other side in deep shadow

### Dramatic Shadows

**Technique:** Shadows as compositional element, not just realism

**Implementation:**
- Hard or semi-hard shadow edges
- Exaggerated shadow shapes
- Colored shadows (not just black/gray)
- Long shadows for mood

**Example:** Venetian blind shadows, character silhouette in backlight

### Colored Lighting

**Technique:** Non-white, saturated light colors for mood

**Implementation:**
- Warm key light (orange, amber) + cool fill (blue, cyan)
- Monochromatic scenes (all one color temperature)
- Colored accent lights (magic effects, environmental)

**Color Mood:**
- Warm (orange/red): Aggressive, tense, passionate
- Cool (blue/cyan): Melancholic, mysterious, lonely
- Green: Sickly, unnatural, eerie
- Purple/magenta: Magical, dreamlike, surreal

**Example:** Orange sunset light + blue shadow fill (classic anime technique)

### Rim Lighting

**Technique:** Backlight or edge light separating character from background

**Implementation:**
- Spot or point light behind character
- Light only edges (grazing angle)
- Often colored (not white)

**Effect:** Character "pops" from background, dramatic silhouette

**Example:** Character backlit by setting sun (orange rim light)

### Volumetric Effects (Light Shafts)

**Technique:** Visible light beams through atmosphere

**Implementation:**
- UE5 volumetric fog
- Directional light with volumetric scattering
- Dust/particle effects in light beams

**Effect:** Atmospheric, moody, reveals light source

**Example:** Sunbeams through window, fog in forest

---

## Lighting Scenarios for Game

Consider typical in-game scenarios when testing:

### Scenario 1: Exterior Day (Overcast/Moody)

**Lighting:**
- Soft directional light (overcast sun)
- Desaturated, cool-toned
- Low contrast (diffuse light)

**Mood:** Melancholic, oppressive, somber

**Inspiration:** Skyrim overcast, Mushishi outdoor scenes (see [[ColorPalettes]])

### Scenario 2: Exterior Night (Moonlight)

**Lighting:**
- Directional light (moon) - cool blue
- Very low ambient
- High contrast (dark shadows)

**Mood:** Mysterious, lonely, eerie

**Inspiration:** Elden Ring nighttime, dark fantasy

### Scenario 3: Interior Dungeon (Torchlight)

**Lighting:**
- Point lights (torches, fires) - warm orange
- Dynamic, flickering
- Deep shadows between lights

**Mood:** Tense, foreboding, claustrophobic

**Inspiration:** Dark Souls dungeons, classic dungeon crawlers

### Scenario 4: Boss Arena (Dramatic)

**Lighting:**
- Colored accent lights (boss magic effects)
- High contrast, dramatic
- Possibly dynamic (lighting changes with boss state)

**Mood:** Epic, intense, supernatural

**Inspiration:** Elden Ring boss arenas, dramatic anime fight scenes

### Scenario 5: Safe Area (Village/Camp)

**Lighting:**
- Warm, inviting lights (lanterns, campfire)
- Moderate contrast
- Soft, comfortable

**Mood:** Safe, restful, peaceful (contrast with hostile areas)

**Inspiration:** Firelink Shrine (Dark Souls), safe havens

---

## Decision Framework

### How to Choose

**After testing all three approaches:**

1. **Review Screenshots**
   - Compare side-by-side for each scenario
   - Identify clear winner or hybrid opportunities

2. **Assess Against Criteria**
   - Score each approach on evaluation criteria (1-5 scale)
   - Identify strengths and weaknesses

3. **Consider Artistic Vision**
   - Which aligns best with [[ArtOverview]] goals?
   - Which feels right for the game's mood?

4. **Evaluate Technical Feasibility**
   - Development time required
   - Performance implications
   - Complexity for iteration

5. **Test with Gameplay**
   - Not just static screenshots - see in motion
   - How does it feel during actual play?
   - Does it enhance or distract from gameplay?

6. **Make Decision**
   - Document chosen approach
   - Note any hybrid elements
   - Record rationale for future reference

### Decision Matrix

Use this matrix to score each approach:

| Criteria | Weight | Approach A (Naturalistic) | Approach B (Cel-Shaded) | Approach C (Hybrid) |
|----------|--------|---------------------------|-------------------------|---------------------|
| Mood/Atmosphere | High | ___ / 5 | ___ / 5 | ___ / 5 |
| Art Style Fit | High | ___ / 5 | ___ / 5 | ___ / 5 |
| Visual Quality | High | ___ / 5 | ___ / 5 | ___ / 5 |
| 90s Anime Match | Medium | ___ / 5 | ___ / 5 | ___ / 5 |
| Performance | Medium | ___ / 5 | ___ / 5 | ___ / 5 |
| Ease of Iteration | Medium | ___ / 5 | ___ / 5 | ___ / 5 |
| Technical Complexity | Low | ___ / 5 | ___ / 5 | ___ / 5 |
| **TOTAL** | | **___** | **___** | **___** |

**Weighting:**
- High: 3x score
- Medium: 2x score
- Low: 1x score

**Fill out after testing each approach**

---

## Implementation Notes

### Approach A: Naturalistic

**UE5 Setup:**
- Use default Lit shading model in materials
- Standard light types (Directional, Point, Spot)
- Adjust light properties: Intensity, Color, Attenuation Radius, Source Radius (softness)
- Enable/adjust shadows: Shadow Bias, Shadow Filter Sharpen

**Materials:**
- See [[Materials3D]] - standard PBR parameters (Roughness, Metallic)
- See [[Materials2D]] - normal maps for sprite lighting

**Tips:**
- Use colored lights for mood (warm/cool contrast)
- Push intensity higher than realistic (drama)
- Keep ambient very low (deep shadows)
- Use volumetric fog for atmosphere

### Approach B: Cel-Shaded

**UE5 Setup:**
- Custom shading model in materials (see [[Materials3D]])
- May still use standard light types (process lighting differently in shader)

**Materials:**
- Implement cel-shading in master material
- Parameters: `CelSteps` (number of bands), `CelThreshold` (shadow hardness)
- Quantize lighting calculation

**Shader Code (Pseudocode):**
```hlsl
float NdotL = dot(Normal, LightDirection);
float CelSteps = 3; // Light, Mid, Shadow
float Stepped = floor(NdotL * CelSteps) / CelSteps;
float3 Shading = lerp(ShadowColor, LightColor, Stepped);
```

**Tips:**
- Start with 2-3 steps (too many = looks like gradients)
- Experiment with shadow threshold (sharper = more graphic)
- Consider rim lighting (separate pass)
- Test with both 3D and 2D assets

### Approach C: Hybrid

**UE5 Setup:**
- Implement both naturalistic and cel-shaded materials
- Choose per asset which to use, or blend in single material

**Materials:**
- Add `UseCustomShading` parameter to master material
- Blend between PBR and cel-shaded based on parameter
- Different Material Instances for different assets

**Shader Code (Pseudocode):**
```hlsl
float3 NaturalisticShading = DefaultLit(Normal, Light, Roughness);
float3 CelShading = CelShade(Normal, Light, CelSteps);
float3 Final = lerp(NaturalisticShading, CelShading, UseCustomShading);
```

**Tips:**
- Define clear rules (which assets get which shading)
- Test transitions (e.g., 2D character in 3D environment)
- May use naturalistic base + cel-shaded accents (rim lights)
- Ensure visual consistency despite different approaches

---

## Progress Tracking

### Testing Status
- [ ] Test level created with sample assets
- [ ] Approach A (Naturalistic) tested
- [ ] Approach B (Cel-Shaded) tested
- [ ] Approach C (Hybrid) tested
- [ ] Screenshots captured for all approaches
- [ ] Evaluation matrix filled out
- [ ] Decision made

### Decision Record

**Chosen Approach:** [ ] A - Naturalistic / [ ] B - Cel-Shaded / [ ] C - Hybrid / [ ] Custom: __________

**Date Decided:** __________

**Rationale:**
- Why this approach was chosen:
- Key strengths that led to decision:
- Trade-offs accepted:

**Hybrid Details (if applicable):**
- Which assets use which approach:
- Blending strategy:
- Special cases:

**Implementation Notes:**
- Materials updated: [ ] Yes / [ ] No (see [[Materials3D]], [[Materials2D]])
- Shaders developed: [ ] Yes / [ ] No / [ ] Not needed
- Lighting guidelines documented: [ ] Yes / [ ] No
- Test scenarios validated: [ ] Yes / [ ] No

### Post-Decision
- [ ] Materials updated for chosen approach (see [[Materials3D]], [[Materials2D]])
- [ ] Lighting setups created for key scenarios
- [ ] Guidelines documented for level designers/artists
- [ ] Performance benchmarked and acceptable
- [ ] Integrates well with post-processing (see [[PostProcessing]])

---

## Related Documentation

- **[[ArtOverview]]** - 90s anime inspiration, moody aesthetic goals
- **[[Materials3D]]** - 3D material lighting integration
- **[[Materials2D]]** - 2D sprite normal map lighting
- **[[PostProcessing]]** - Film effects that complement lighting
- **[[ColorPalettes]]** - Color mood and lighting color choices
- **[[Pipeline3D]]** - Where lighting testing fits in 3D workflow
- **[[Pipeline2D]]** - Sprite normal map testing with lights

---

## Next Steps

1. Create lighting test level with sample assets
2. Implement Approach A (Naturalistic) - test and document
3. Implement Approach B (Cel-Shaded) - test and document
4. Implement Approach C (Hybrid) - test and document
5. Fill out evaluation matrix for all approaches
6. Review with fresh eyes (take screenshots, review later)
7. Make decision and document rationale
8. Update materials for chosen approach (see [[Materials3D]], [[Materials2D]])
9. Create lighting guidelines for level/scene setup
10. Validate decision with actual gameplay testing
