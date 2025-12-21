# Color Palettes & Theory

This document defines the color palette approach for Lament, including color theory principles, reference analysis, and palette guidelines for different game areas and moods.

**Related Documentation:**
- [[ArtOverview]] - Color inspirations (Skyrim, Elden Ring, Mushishi)
- [[Materials3D]] - In-engine color palette system
- [[PostProcessing]] - LUT color grading integration
- [[Lighting]] - Colored lighting for mood

---

## Overview

Lament's color approach prioritizes muted, desaturated palettes with selective use of color for mood and emphasis. The primary palette type is monochromatic, with analogous and complementary palettes used strategically.

**Core Principles:**
- **Mostly Monochromatic:** Single-hue variations (different values/saturations of one color)
- **Desaturated/Muted:** Low saturation for melancholic, moody atmosphere
- **Strategic Accents:** Complementary or analogous colors for emphasis (not everywhere)
- **Mood-Driven:** Color palette reflects emotional tone of area/moment

**Philosophy:** Restraint in color creates impact when color is used

**Inspiration:** Skyrim (desaturated Nordic), Elden Ring (golden accents on muted backgrounds), Mushishi (soft naturalistic)

---

## Color Theory Primer

### Palette Types

**Monochromatic:**
- Single hue with variations in value (lightness/darkness) and saturation
- Example: Blues ranging from pale ice blue to deep navy
- **Effect:** Unified, cohesive, calm or melancholic
- **Best For:** Single-mood areas, meditative spaces, oppressive environments

**Analogous:**
- Adjacent hues on color wheel (e.g., blue, blue-green, green)
- Harmonious, natural color relationships
- Example: Yellow-green, green, blue-green (forest palette)
- **Effect:** Natural, harmonious, subtle variety
- **Best For:** Organic environments, transitions, nuanced moods

**Complementary:**
- Opposite hues on color wheel (e.g., orange and blue)
- High contrast, dynamic tension
- Example: Warm firelight (orange) on cool shadows (blue)
- **Effect:** Dramatic, energetic, attention-grabbing
- **Best For:** Key moments, boss fights, emphasis, conflict

**Split-Complementary:**
- Base hue + two colors adjacent to its complement
- Example: Blue + red-orange + yellow-orange
- Softer than pure complementary but still dynamic
- **Best For:** Variation on complementary without full intensity

### Saturation & Value

**Saturation (Chroma):**
- How pure/intense the color is
- High saturation: Vivid, vibrant (use sparingly in Lament)
- Low saturation: Muted, grayed, desaturated (primary approach)
- **Lament Approach:** Generally low saturation (20-40% typical)

**Value (Lightness):**
- How light or dark the color is
- High value: Pale, light (highlights, skies)
- Low value: Deep, dark (shadows, night)
- **Lament Approach:** Wide range of values for contrast, but often mid-to-low (darker mood)

**Desaturation Technique:**
- Add gray to pure hue
- Creates muted, sophisticated palettes
- Reduces visual fatigue (not overwhelming)
- Matches film photography aesthetic (see [[PostProcessing]])

---

## Reference Analysis

### Skyrim

**Color Characteristics:**
- Cool-toned (blues, grays, desaturated greens)
- Very low saturation (almost grayscale in many areas)
- Nordic/winter atmosphere
- Contrast between cold environments and warm firelight (interior taverns)

**Palette Examples:**

**Exterior (Snow/Mountains):**
- Base: Cool gray (#A0A8B0)
- Shadows: Deep blue-gray (#4A5560)
- Highlights: Pale ice blue (#D0E0F0)
- Accent: None (pure monochromatic)

**Interior (Tavern/Firelight):**
- Base: Warm brown-gray (#8A7A6A)
- Shadows: Deep cool gray (#3A3540)
- Highlights: Warm orange (#D89060)
- Accent: Fire orange (#E07030) - complementary to cool exterior

**What We're Taking:**
- Desaturated approach (barely any pure color)
- Cool monochromatic for oppressive/lonely moods
- Warm accents in safe spaces (contrast with hostile world)

---

### Elden Ring

**Color Characteristics:**
- Muted, desaturated backgrounds (gray, brown, green)
- Golden/amber key lighting (sunlight, grace sites)
- High contrast between light and dark
- Complementary orange/blue in many scenes

**Palette Examples:**

**Limgrave (Open World):**
- Base: Desaturated green (#6A7A5A)
- Shadows: Cool gray-brown (#4A4540)
- Highlights: Golden amber (#D0A060)
- Sky: Pale desaturated blue (#B0C0D0)

**Catacombs (Dark Interior):**
- Base: Deep brown-gray (#3A3530)
- Shadows: Near-black blue-black (#1A1820)
- Highlights: Pale stone (#8A8A7A)
- Accent: Warm torch orange (#E08040)

**Boss Arena (Dramatic):**
- Base: Dark desaturated environment (varies)
- Key Light: Saturated golden or colored (boss-specific)
- Effect Light: Magic colors (purple, blue, red - depending on boss)
- High contrast (deep blacks, bright highlights)

**What We're Taking:**
- Golden/amber accent lighting on muted backgrounds
- High contrast dramatic lighting
- Desaturated base with selective saturated accents
- Boss-specific colored lighting for emphasis

---

### Mushishi

**Color Characteristics:**
- Soft, naturalistic palettes
- Muted saturation (gentle, not gray)
- Analogous color harmonies (natural color relationships)
- Organic, earthy tones (greens, browns, soft blues)
- Melancholic, peaceful atmosphere

**Palette Examples:**

**Forest (Daytime):**
- Base: Muted green (#6A8A6A)
- Shadows: Deeper green-brown (#4A5A4A)
- Highlights: Pale yellow-green (#C0D0A0)
- Sky: Soft desaturated blue (#A0B8C8)

**Twilight/Dusk:**
- Base: Warm gray-purple (#8A7A8A)
- Shadows: Deep purple-blue (#3A3550)
- Highlights: Pale orange-pink (#E0C0B0)
- Sky: Gradient purple to orange (analogous warm)

**Interior (Traditional Japanese Home):**
- Base: Warm beige-brown (#B0A090)
- Shadows: Cool gray-brown (#6A6560)
- Highlights: Pale cream (#E0D8C8)
- Accent: Muted indigo or green (textiles, minimal)

**What We're Taking:**
- Analogous harmonies for natural, organic moods
- Muted but not lifeless (subtle color warmth)
- Melancholic atmosphere through soft colors
- Gentle gradients (not harsh transitions)

---

## Lament Palette Guidelines

### Primary Approach: Monochromatic

**When to Use:**
- Single-emotion areas (pure melancholy, pure dread, pure peace)
- Oppressive environments (dungeons, hostile areas)
- Minimalist, focused moments

**How to Build:**
1. Choose base hue (e.g., blue for cold/lonely, brown for decay)
2. Create variations: pale (highlights), mid (base), deep (shadows)
3. Desaturate heavily (20-30% saturation max)
4. Ensure wide value range (contrast)

**Example: Cold Dungeon (Blue Monochromatic):**
```
Highlights: #B0C0D0 (pale ice blue, 25% saturation)
Base: #6A7A8A (mid blue-gray, 20% saturation)
Shadows: #2A3A4A (deep blue-black, 15% saturation)
```

**Example: Decaying Forest (Brown Monochromatic):**
```
Highlights: #C0B0A0 (pale tan, 20% saturation)
Base: #8A7A6A (mid brown-gray, 25% saturation)
Shadows: #3A3530 (deep brown-black, 10% saturation)
```

---

### Secondary Approach: Analogous

**When to Use:**
- Organic/natural environments (forests, meadows, wetlands)
- Transition areas (between major zones)
- Nuanced moods (melancholy + mystery, peace + unease)

**How to Build:**
1. Choose primary hue (dominant color)
2. Add adjacent hues (1-2 neighbors on color wheel)
3. Keep saturation low (similar to monochromatic)
4. One hue dominates, others support

**Example: Twilight Forest (Blue-Purple-Pink Analogous):**
```
Primary (Sky): #8A7AA0 (desaturated purple, 30% saturation)
Secondary (Trees): #6A7A8A (desaturated blue, 25% saturation)
Accent (Highlights): #C0A0B0 (pale pink, 20% saturation)
Shadows: #3A3550 (deep purple-blue, 15% saturation)
```

**Example: Autumn Decay (Yellow-Orange-Brown Analogous):**
```
Primary (Foliage): #A08A60 (desaturated orange, 30% saturation)
Secondary (Ground): #8A7A50 (desaturated yellow-brown, 25% saturation)
Accent (Highlights): #C0A070 (pale orange, 25% saturation)
Shadows: #4A3A2A (deep brown, 15% saturation)
```

---

### Accent Approach: Complementary

**When to Use:**
- High-drama moments (boss fights, key story beats)
- Contrast/emphasis (safe vs. hostile, fire vs. ice)
- Dynamic energy (action, conflict)
- Selective use (not entire palette, just accent)

**How to Build:**
1. Establish muted monochromatic or analogous base
2. Add complementary color as accent (not dominant)
3. Accent can be slightly more saturated (40-50% vs. 20-30% base)
4. Use sparingly (highlights, key elements, lighting)

**Example: Fire in Ice Cave (Orange/Blue Complementary):**
```
Base Environment (Cool):
  Walls: #6A7A8A (blue-gray, 20% saturation)
  Shadows: #2A3A4A (deep blue, 15% saturation)
  Ice: #B0C0D0 (pale blue, 25% saturation)

Accent (Warm Fire):
  Firelight: #E08040 (orange, 50% saturation) - small area
  Fire Glow: #D09050 (amber, 45% saturation)
```

**Example: Boss Arena (Purple Magic vs. Gold Light):**
```
Base Environment (Muted):
  Floor: #4A4540 (gray-brown, 10% saturation)
  Walls: #3A3A40 (cool gray, 5% saturation)

Accent (Boss Magic - Purple):
  Magic Effects: #A060C0 (purple, 60% saturation)
  Magic Glow: #8050A0 (deep purple, 55% saturation)

Accent (Player/Grace - Gold):
  Key Light: #D0A050 (golden, 50% saturation) - complementary to purple
```

---

## Palette Application Workflow

### In-Engine Color Palette System

See [[Materials3D]] for technical implementation.

**Workflow:**
1. Define palette in this document (hex colors, names, mood)
2. Create Material Parameter Collection or Material Instances (see [[Materials3D]])
3. Assign palette colors to materials
4. Apply to assets in level/area
5. Adjust based on actual in-game look (lighting, post-processing)

**Runtime Swapping:**
- Change entire area's palette by updating Material Parameter Collection
- Useful for dynamic mood shifts (e.g., world corruption effect)
- See [[Materials3D]] for implementation options

---

### Palette Testing Process

1. **Define Palette** (use guidelines above, reference analysis)
2. **Create Test Scene** with variety of assets (3D props, environment, 2D sprites)
3. **Apply Palette** to materials
4. **Add Lighting** appropriate to scenario (see [[Lighting]])
5. **Apply Post-Processing** (LUT, grain, vignette - see [[PostProcessing]])
6. **Evaluate:**
   - Does it achieve intended mood?
   - Is contrast sufficient (readability)?
   - Does it fit game's overall aesthetic?
   - Do colors work with lighting/post?
7. **Iterate** on palette colors if needed
8. **Document Final Palette** in this file (see templates below)

---

## Palette Library

Document finalized palettes here as they're created. Use this format:

---

### [Palette Name]

**Mood/Area:** [Describe intended mood and where used]

**Palette Type:** Monochromatic / Analogous / Complementary (accents)

**Color Scheme:**
```
Primary Color: [Hex] [Name] [Saturation %]
Secondary Color: [Hex] [Name] [Saturation %] (if analogous)
Shadow Color: [Hex] [Name] [Saturation %]
Highlight Color: [Hex] [Name] [Saturation %]
Accent Color: [Hex] [Name] [Saturation %] (if complementary)
```

**Lighting Notes:** [How to light this palette - colored lights, intensity, etc.]

**Post-Processing Notes:** [LUT recommendations, any special adjustments]

**Usage:** [Which levels/areas use this palette]

**Reference:** [Inspiration - Skyrim, Elden Ring, Mushishi, or other]

**Status:** [ ] Concept / [ ] Testing / [ ] Finalized

---

### Example: Nordic Desolation (Placeholder)

**Mood/Area:** Cold, lonely, oppressive exterior environments (mountains, tundra)

**Palette Type:** Monochromatic (Cool Blue-Gray)

**Color Scheme:**
```
Primary Color: #6A7A8A (Steel Blue-Gray, 20% saturation)
Shadow Color: #2A3A4A (Deep Blue-Black, 15% saturation)
Highlight Color: #B0C0D0 (Pale Ice Blue, 25% saturation)
Accent Color: None (pure monochromatic)
```

**Lighting Notes:**
- Directional light (sun/overcast) - cool white or very pale blue
- Low ambient (deep shadows)
- No accent lights (barren environment)

**Post-Processing Notes:**
- Cool-toned LUT (blue bias in shadows)
- Moderate grain (harsh environment)
- Moderate vignette

**Usage:** World 1 - Exterior zones, mountain paths, frozen wastelands

**Reference:** Skyrim (Nordic/winter areas)

**Status:** [ ] Concept / [X] Testing / [ ] Finalized

---

### Example: Ember Refuge (Placeholder)

**Mood/Area:** Safe haven, warm respite from hostile world (village, campfire, rest area)

**Palette Type:** Analogous (Warm Yellow-Orange-Brown) with Cool Shadows

**Color Scheme:**
```
Primary Color: #A08A60 (Warm Tan, 30% saturation)
Secondary Color: #C09A50 (Amber, 35% saturation)
Shadow Color: #3A3540 (Cool Purple-Gray, 10% saturation) - contrast
Highlight Color: #E0C090 (Pale Warm Beige, 30% saturation)
Accent Color: #E08040 (Fire Orange, 50% saturation) - firelight only
```

**Lighting Notes:**
- Point lights (fires, lanterns) - warm orange
- Directional light (if exterior) - cool to contrast warmth
- Moderate ambient (inviting, not harsh)

**Post-Processing Notes:**
- Warm-toned LUT (orange/amber bias)
- Less grain (comfortable, not harsh)
- Subtle vignette (intimate)

**Usage:** Safe areas - villages, campsites, rest zones

**Reference:** Skyrim (tavern interiors), cozy game aesthetics

**Status:** [ ] Concept / [X] Testing / [ ] Finalized

---

### [Add more palettes as created]

---

## Mood-to-Palette Quick Reference

Use this guide to choose starting palette based on intended mood:

| Mood | Palette Type | Hue(s) | Saturation | Value | Example |
|------|--------------|--------|------------|-------|---------|
| **Melancholic** | Monochromatic | Blue, Purple, Gray | Very Low (10-25%) | Mid to Low | Mushishi twilight |
| **Mysterious** | Analogous | Purple, Blue, Teal | Low (20-35%) | Mid | Elden Ring catacombs |
| **Hostile/Tense** | Monochromatic or Complementary (accents) | Red, Orange, Deep Brown | Moderate (30-45%) | Low to Mid | Dark Souls lava areas |
| **Peaceful** | Analogous | Green, Blue-Green, Yellow-Green | Low to Moderate (25-40%) | Mid to High | Mushishi forest |
| **Oppressive** | Monochromatic | Gray, Brown, Desaturated Green | Very Low (5-20%) | Low | Skyrim dungeons |
| **Lonely/Cold** | Monochromatic | Blue, Blue-Gray, Cyan | Low (15-30%) | Mid | Skyrim exterior winter |
| **Warm/Safe** | Analogous | Orange, Yellow, Brown | Moderate (30-45%) | Mid | Firelight interiors |
| **Eerie/Unnatural** | Complementary or Analogous (unusual) | Green, Purple, Sickly Yellow | Low to Moderate (20-40%) | Low to Mid | Poison swamps, cursed areas |
| **Dramatic/Epic** | Complementary | Any (boss-specific) | Moderate to High (40-60% accents) | High Contrast | Boss arenas, key moments |
| **Decaying** | Analogous or Monochromatic | Brown, Desaturated Green, Gray | Very Low (10-25%) | Low to Mid | Elden Ring ruins |

**How to Use:**
1. Identify intended mood for area/moment
2. Find mood in table above
3. Use suggested palette type and hues as starting point
4. Refer to Reference Analysis (Skyrim/Elden Ring/Mushishi) for examples
5. Build palette using guidelines in this document
6. Test and iterate

---

## Integration with Other Systems

### Lighting

See [[Lighting]] for lighting approach details.

**Colored Lighting:**
- Use palette colors for light tints (e.g., warm orange lights in warm palette)
- Complementary light/shadow (warm key light, cool fill light)
- Dramatic lighting can push saturation higher than base palette

**Testing:**
- Always test palette with actual lighting setup
- Lighting can shift perceived colors (cool light on warm palette = desaturation)
- Adjust palette colors if lighting changes the look too much

---

### Post-Processing

See [[PostProcessing]] for post details.

**LUT Color Grading:**
- LUT should enhance palette, not fight it
- Choose LUT with similar color bias (cool LUT for cool palette, etc.)
- Desaturated LUT + muted palette = cohesive look
- Test LUT with various palettes (may need per-area LUT adjustments)

**Film Grain:**
- Grain adds texture to solid-color assets (helps muted palettes)
- Doesn't significantly affect colors (safe to use with any palette)

**Vignette:**
- Darkens edges (affects value, not hue)
- Can enhance monochromatic look (keeps focus on center)

---

### Materials

See [[Materials3D]] and [[Materials2D]].

**3D Solid Colors:**
- Palette colors applied as material parameters
- Muted palettes work well with solid-color approach (no texture detail needed)
- Lighting and post-processing add visual interest

**2D Sprites:**
- Sprite art should use palette colors (or AI style should match)
- Normal maps react to colored lighting (enhances palette)
- Muted sprite colors + dynamic lighting = cohesive with 3D

---

## Progress Tracking

### Palette Creation Status
- [ ] Nordic Desolation palette finalized
- [ ] Ember Refuge palette finalized
- [ ] [Other palettes TBD based on game worlds/areas]
- [ ] Palette library populated with all needed palettes

### Implementation Status
- [ ] Color palette system implemented in materials (see [[Materials3D]])
- [ ] Runtime palette swapping tested (if needed)
- [ ] Palettes tested with lighting setups (see [[Lighting]])
- [ ] Palettes tested with LUTs/post-processing (see [[PostProcessing]])

### Integration Testing
- [ ] All palettes tested in-engine
- [ ] Palette guidelines validated with actual usage
- [ ] Mood-to-palette reference confirmed accurate
- [ ] Lighting color guidelines documented per palette

---

## Related Documentation

- **[[ArtOverview]]** - Color inspirations and overall aesthetic
- **[[Materials3D]]** - In-engine palette system implementation
- **[[Lighting]]** - Colored lighting and palette interaction
- **[[PostProcessing]]** - LUT color grading
- **[[Pipeline3D]]** - Where to apply palette colors to 3D assets
- **[[Pipeline2D]]** - Color considerations for 2D sprite art

---

## Next Steps

1. Analyze reference games more deeply (screenshot specific scenes, extract palettes)
2. Define initial palette set based on known game areas/worlds
3. Implement color palette system in materials (see [[Materials3D]])
4. Create first test palette (e.g., Nordic Desolation)
5. Test palette with lighting and post-processing
6. Iterate and finalize first palette
7. Document in Palette Library section above
8. Repeat for additional palettes as areas are designed
9. Create mood board with reference images for each palette (separate from docs)
