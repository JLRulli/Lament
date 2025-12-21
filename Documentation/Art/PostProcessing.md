# Post-Processing & Film Effects

This document details the post-processing setup for achieving Lament's moody, film-inspired aesthetic through UE5's post-process volumes.

**Related Documentation:**
- [[ArtOverview]] - Film photography/video inspiration
- [[Lighting]] - How post-processing complements lighting
- [[ColorPalettes]] - Color grading and LUT selection
- [[Tools]] - Film LUT and grain resources

---

## Overview

Post-processing provides the final layer of visual polish, transforming the base rendering into a moody, atmospheric, film-inspired look.

**Core Goals:**
- **Film Aesthetic:** Emulate analog film photography/video characteristics
- **Atmospheric Mood:** Enhance melancholic, mysterious, moody tone
- **Analog Imperfection:** Add grain, vignette, lens artifacts for warmth
- **Color Grading:** Achieve desaturated, muted color palette (see [[ColorPalettes]])

**Philosophy:** Post-processing as the "final filter" that unifies and elevates all art elements

**Inspiration:** Moody film photography/video, 90s anime color grading (see [[ArtOverview]])

---

## UE5 Post-Process Volume Setup

### Post-Process Volume Basics

**What Is It:**
UE5 Post Process Volume = 3D volume in level that applies screen-space effects

**Types:**
- **Bounded:** Effects only apply within volume bounds
- **Unbound (Infinite):** Effects apply everywhere (use for global effects)

**Priority:**
- Higher priority volumes override lower priority
- Useful for per-area or per-scenario effects (e.g., different LUT per world)

**Blend Weight:**
- 0 = no effect
- 1 = full effect
- Allows smooth transitions between volumes

**Recommended Setup:**
- Global unbound volume for baseline effects (film grain, vignette, base LUT)
- Bounded volumes for area-specific adjustments (color grading per level)

---

## Film Effects Breakdown

### Film Grain

**Purpose:** Analog film texture, adds warmth and hides banding

**UE5 Settings (in Post Process Volume):**

**Film Grain Intensity:**
- Range: 0.0 - 1.0
- Recommended: 0.3 - 0.6 (visible but not overwhelming)
- Too low: No effect
- Too high: Distracting noise

**Film Grain Jitter (Temporal Variation):**
- Grain animates frame-to-frame (like real film)
- Recommended: Enabled (more authentic)
- Disable if grain should be static

**Film Grain Highlights:**
- Grain intensity in bright areas
- Recommended: Lower than shadows (grain more visible in darks)

**Film Grain Shadows:**
- Grain intensity in dark areas
- Recommended: Higher (accentuates moodiness)

**Custom Grain Texture (Optional):**
- Can use custom grain texture instead of procedural
- Source scanned film grain or create custom
- See [[Tools]] for grain texture resources

**Testing:**
- View at target resolution/screen size
- Grain looks different at different scales
- Test in bright and dark scenes

**Recommended Starting Values:**
```
Grain Intensity: 0.4
Grain Jitter: 1.0 (enabled)
Grain Highlights: 0.2
Grain Shadows: 0.6
```

---

### Vignette

**Purpose:** Darken corners/edges of screen, focus attention center, film lens characteristic

**UE5 Settings:**

**Vignette Intensity:**
- Range: 0.0 - 1.0
- Recommended: 0.3 - 0.5 (subtle to moderate)
- Too strong: Looks like tunnel vision

**Vignette Falloff:**
- Controls how quickly vignette darkens from center to edge
- Higher = sharper falloff (more dramatic)
- Lower = softer falloff (more gradual)
- Recommended: 0.3 - 0.5 (soft transition)

**Vignette Color (Optional):**
- Default: Black (darkens)
- Can use colored vignette (e.g., warm edges for nostalgia)
- Recommended: Stick with black or very subtle color

**Testing:**
- View in actual gameplay scenarios
- Should be noticeable but not distracting
- Works with UI elements? (doesn't obscure HUD)

**Recommended Starting Values:**
```
Vignette Intensity: 0.4
Vignette Falloff: 0.4
Vignette Color: Black (0, 0, 0)
```

---

### Film LUTs (Color Grading)

**Purpose:** Color grading lookup table - transforms colors for mood

**What Is a LUT:**
- 3D lookup table: Input color → Output color
- Applies color grading (hue shifts, saturation, contrast)
- Emulates film stocks or custom color grades

**UE5 Settings:**

**Color Grading LUT:**
- Assign LUT texture (.cube file or UE texture)
- See [[Tools]] for LUT sources (film emulation packs, custom)

**LUT Intensity:**
- Range: 0.0 - 1.0
- 1.0 = full LUT effect
- Can blend between original and LUT-graded

**Creating/Finding LUTs:**

**Option A: Use Existing Film LUTs**
- Download film emulation LUT packs (Kodak, Fuji stocks)
- Moody/desaturated presets
- See [[Tools]] for LUT libraries

**Option B: Create Custom LUTs**
- Export neutral LUT from UE5
- Grade in DaVinci Resolve or Photoshop
- Re-import to UE5
- Full creative control

**Recommended LUT Characteristics:**
- Desaturated (muted colors - see [[ColorPalettes]])
- Cool or warm bias (depending on scene mood)
- Lifted blacks (slightly gray, not pure black - film look)
- Rolled-off highlights (not blown out)
- Subtle color shifts (teal shadows, orange highlights - teal/orange look)

**Testing:**
- Test LUT with various lighting scenarios (day, night, interior)
- Ensure colors still readable and mood appropriate
- Check with [[ColorPalettes]] - does LUT support intended palettes?

**Recommended Starting Point:**
- Find desaturated film LUT (search "cinematic LUT" or "film LUT")
- Set intensity to 0.7-1.0
- Fine-tune or create custom if needed

---

### Lens Effects

**Purpose:** Emulate camera lens characteristics - corner softness, distortion, imperfections

#### Lens Distortion

**UE5 Settings:**

**Barrel/Pincushion Distortion:**
- Slight curvature to image (lens characteristic)
- Barrel: Edges bulge outward
- Pincushion: Edges pinch inward
- Recommended: Very subtle (0.01 - 0.05 range)

**Testing:**
- Can be disorienting if too strong
- May affect UI layout (corners shift)

**Recommended:**
- Use sparingly or disable (can add motion sickness)
- Consider if fits aesthetic (more modern camera look than film)

#### Chromatic Aberration

**Purpose:** Color fringing at edges (lens imperfection)

**UE5 Settings:**

**Chromatic Aberration Intensity:**
- Range: 0.0 - 1.0
- Separates RGB channels slightly at edges
- Recommended: 0.0 - 0.2 (very subtle or disabled)

**Testing:**
- Looks like slight red/blue fringe at high-contrast edges
- Can look like a bug if too strong

**Recommended:**
- Very subtle (0.1) or disabled
- More noticeable on high-res displays

#### Corner Softness (Lens Blur)

**Purpose:** Soften edges/corners like vintage lenses

**Implementation Options:**

**Option A: Via Vignette**
- Use vignette effect (already darkens corners)
- Adds darkness but not blur

**Option B: Custom Post-Process Material**
- Create custom material with radial blur at edges
- More complex but true lens softness
- Apply as blendable post-process material

**Recommended:**
- Start with vignette (simpler)
- If true corner blur needed, research custom post materials

**Corner Softness Notes:**
- Subtle effect (shouldn't be obvious)
- Emulates old lenses (adds analog character)
- May not be necessary (test with and without)

---

### Halation (Highlight Glow)

**Purpose:** Film halation - glow/bloom in highlights with red/orange tint (light scattering in film)

**UE5 Settings (Bloom Section):**

**Bloom Intensity:**
- Overall glow amount
- Recommended: 0.5 - 2.0 (moderate bloom)

**Bloom Threshold:**
- Brightness threshold for bloom to kick in
- Lower = more bloom (glows appear in darker areas)
- Higher = only very bright areas glow
- Recommended: 0.5 - 1.0 (selective highlights)

**Bloom Size Scale:**
- How far bloom spreads
- Larger = softer, more diffuse glow
- Smaller = tighter glow around source
- Recommended: 3.0 - 6.0 (moderate spread)

**Bloom Tint (Halation Effect):**
- Color of bloom
- For halation: Red, orange, or warm color (film characteristic)
- Recommended: Subtle warm tint (RGB: 255, 200, 150) or similar

**Bloom Dirt Mask (Optional):**
- Texture overlay for lens dirt/smudges
- Can add realism but may be too much
- Recommended: Skip unless going for dirty lens look

**Halation-Specific Settings:**
- Enable Bloom
- Set warm tint (orange/red)
- Moderate intensity and size
- Test with bright highlights (fire, magic, sun)

**Recommended Starting Values:**
```
Bloom Intensity: 1.0
Bloom Threshold: 0.8
Bloom Size: 4.0
Bloom Tint: (1.0, 0.8, 0.6) - subtle warm
```

---

## Additional Post-Processing Options

### Depth of Field (DOF)

**Purpose:** Blur out-of-focus areas (camera focus effect)

**Use Cases:**
- Cinematic moments (focus on character, blur background)
- Depth emphasis (foreground/background separation)

**Considerations:**
- Side-scrolling game: May not need DOF (everything in focus)
- Can be distracting during gameplay
- Useful for cutscenes or special moments

**Recommended:**
- Disable for general gameplay (keep everything sharp)
- Enable for cinematics if needed

### Motion Blur

**Purpose:** Blur from camera or object motion

**Considerations:**
- Can reduce visual clarity
- Some players dislike motion blur
- May conflict with "human error" aesthetic (already has imperfection)

**Recommended:**
- Disable or very subtle (0.0 - 0.2 intensity)
- Not essential for film aesthetic

### Ambient Occlusion (AO)

**Purpose:** Darken crevices and contact points (depth enhancement)

**UE5 Settings:**

**AO Intensity:**
- Strength of darkening
- Recommended: 0.5 - 1.0

**AO Radius:**
- How far AO effect reaches
- Smaller = tight contact shadows
- Larger = broader darkening

**Considerations:**
- Helps with depth perception (especially for lower-poly assets)
- Can make scenes feel grounded
- May darken solid-color assets too much (test carefully)

**Recommended:**
- Enable with moderate intensity (0.5-0.7)
- Fine-tune based on lighting approach (see [[Lighting]])

### Exposure (Auto/Manual)

**Purpose:** Control overall brightness (like camera exposure)

**Options:**

**Auto Exposure:**
- Camera adjusts brightness based on scene
- Adapts when moving from dark to bright areas

**Manual Exposure:**
- Fixed exposure value
- Consistent brightness

**Recommended:**
- Manual exposure for consistent look (avoid auto-adjust distractions)
- Set based on target brightness for mood
- Or use auto with narrow min/max range (constrained adaptation)

---

## Settings Profile Template

Use this template to document final post-processing settings:

### Global Post-Process Volume Settings

**Film Grain:**
```
Intensity: _______
Jitter: _______
Highlights: _______
Shadows: _______
Custom Texture: [ ] Yes: _______ / [ ] No (procedural)
```

**Vignette:**
```
Intensity: _______
Falloff: _______
Color: RGB(_____, _____, _____)
```

**Color Grading (LUT):**
```
LUT File: _______
Intensity: _______
Notes: _______
```

**Bloom (Halation):**
```
Intensity: _______
Threshold: _______
Size: _______
Tint: RGB(_____, _____, _____)
```

**Lens Effects:**
```
Distortion: _______ (or disabled)
Chromatic Aberration: _______ (or disabled)
Corner Softness: [ ] Vignette / [ ] Custom / [ ] Disabled
```

**Ambient Occlusion:**
```
Intensity: _______
Radius: _______
```

**Exposure:**
```
Type: [ ] Auto / [ ] Manual
Value/Range: _______
```

**Other:**
```
Depth of Field: [ ] Enabled / [ ] Disabled
Motion Blur: [ ] Enabled: _______ / [ ] Disabled
```

---

## Per-Area/Scenario Variations

While global volume provides baseline, bounded volumes can override for specific areas:

### Example: Dark Dungeon Override

**Adjustments:**
- Increase grain shadows (darker, grittier)
- Increase vignette (claustrophobic)
- Warmer LUT or color tint (torchlight)
- Higher bloom for torches (exaggerated fire glow)

### Example: Ethereal Dream Sequence

**Adjustments:**
- Decrease grain (cleaner, surreal)
- Decrease vignette (open, airy)
- Cooler LUT or desaturated (otherworldly)
- Higher bloom with cool tint (dreamlike glow)

### Example: Boss Arena

**Adjustments:**
- Increase contrast (dramatic)
- Colored LUT shift (red for aggression, purple for magic)
- Bloom with boss-color tint (magic effect)
- May disable grain (clarity for combat)

**Setup:**
- Place bounded Post Process Volume in specific level area
- Set higher priority than global volume
- Override only specific settings (others inherit from global)
- Smooth blend between volumes (blend radius)

---

## Integration with Other Systems

### Lighting

See [[Lighting]] for lighting approach details.

**Considerations:**
- LUT interacts with light colors (test together)
- Bloom responds to bright lights (adjust threshold if lights too glowy)
- AO complements dramatic lighting (shadow enhancement)
- Vignette frames lighting composition

**Testing:**
- Always test post effects with actual game lighting
- Different lighting approaches (naturalistic/cel-shaded) may need different post settings

### Color Palettes

See [[ColorPalettes]] for palette details.

**Considerations:**
- LUT shifts colors (test with intended palettes)
- Don't fight palette with LUT (LUT should enhance, not override)
- Desaturated LUT + monochromatic palette = cohesive look

**Testing:**
- Apply final LUT to scenes with different palettes
- Ensure muted/desaturated aesthetic maintained

### Materials

See [[Materials3D]] and [[Materials2D]].

**Considerations:**
- Grain adds texture to solid-color 3D assets (beneficial)
- Bloom on emissive materials (magic effects)
- Vignette frames both 3D and 2D assets

**Testing:**
- View variety of materials with post effects active
- Ensure solid colors don't look too flat (grain helps)

---

## Performance Considerations

### Optimization

**Expensive Effects:**
- Depth of Field (especially high-quality)
- High-resolution bloom
- Complex LUTs

**Cheaper Effects:**
- Film grain (relatively cheap)
- Vignette (very cheap)
- Simple bloom

**Tips:**
- Disable effects not needed (DOF, motion blur if not using)
- Use lower-quality bloom if performance-critical
- LUTs are cheap (baked lookup table)

**Testing:**
- Profile with `stat GPU` and `stat RHI`
- Measure frame time impact of post-processing
- Balance visual quality vs. performance

### Scalability

**For Multiple Platforms/Quality Settings:**
- Create scalability settings for post effects
- Low: Minimal grain, no bloom, simple LUT
- Medium: Moderate grain, moderate bloom, LUT
- High: Full effects as designed

**UE5 Scalability System:**
- Post-processing quality can be controlled via scalability settings
- Users can adjust if performance issues

---

## Progress Tracking

### Implementation Status
- [ ] Global Post Process Volume created
- [ ] Film grain configured
- [ ] Vignette configured
- [ ] LUT selected/created and applied
- [ ] Bloom/halation configured
- [ ] Lens effects tested (distortion, chromatic aberration, corner softness)
- [ ] Ambient Occlusion configured
- [ ] Exposure settings finalized
- [ ] Per-area volume variations created (if needed)

### Decisions Made
- [ ] Film grain intensity finalized: _______
- [ ] Vignette settings finalized: _______
- [ ] LUT chosen: _______
- [ ] Bloom/halation settings finalized: _______
- [ ] Lens effects approach: Enabled / Disabled / Selective
- [ ] Depth of Field: Enabled / Disabled
- [ ] Motion Blur: Enabled / Disabled

### Testing
- [ ] Tested with all lighting approaches (see [[Lighting]])
- [ ] Tested with all color palettes (see [[ColorPalettes]])
- [ ] Tested in all key scenarios (dungeon, exterior, boss arena, etc.)
- [ ] Performance benchmarked and acceptable
- [ ] Final settings documented (use template above)

---

## Related Documentation

- **[[ArtOverview]]** - Film photography/video inspiration, moody aesthetic
- **[[Lighting]]** - Lighting integration with post-processing
- **[[ColorPalettes]]** - LUT color grading and palette interaction
- **[[Tools]]** - Film LUT sources, grain texture resources
- **[[Materials3D]]** - How post affects 3D solid-color materials
- **[[Materials2D]]** - How post affects 2D sprites

---

## Next Steps

1. Create global unbound Post Process Volume in test level
2. Configure film grain (start with recommended values, tune)
3. Configure vignette (start with recommended values, tune)
4. Find or create film LUT (see [[Tools]])
5. Apply LUT and test with various color palettes (see [[ColorPalettes]])
6. Configure bloom for halation effect (warm tint, moderate intensity)
7. Test lens effects (decide if needed or disable)
8. Configure AO to enhance depth
9. Set exposure (manual recommended)
10. Test complete post-processing with actual gameplay scenarios
11. Measure performance and optimize if needed
12. Document final settings using template above
13. Create per-area volumes if needed (dungeons, boss arenas, etc.)
