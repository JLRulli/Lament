# 2D Sprite Animation Pipeline

This document outlines the complete workflow for creating 2D sprite animations in Lament, from AI-assisted character generation through sprite sheet integration in UE5.

**Related Documentation:**
- [[Tools]] - Software and tools reference
- [[Materials2D]] - Sprite materials and normal map integration
- [[ArtOverview]] - "Human error" aesthetic and 90s anime inspiration

---

## Pipeline Overview

The 2D animation workflow leverages AI image generation, automated rigging, and style conversion to create sprite-based characters with minimal manual art creation. The process converts between 2D and 3D multiple times to take advantage of each domain's strengths.

**Key Principles:**
- AI generates initial character design (Stable Diffusion + custom LoRA)
- 3D rigging and animation applied automatically
- AI converts back to 2D for final stylized look
- Normal maps enable dynamic lighting on 2D sprites
- "Human error" script adds imperfection to avoid rotoscoped look
- Manual checkpoints prevent wasted downstream processing

**Philosophy:** Combine AI generation, 3D animation tools, and procedural variation to create distinctive 2D animations efficiently

---

## Workflow Steps

### Step 1: Character Image Generation

**Goal:** Generate initial 2D character design using AI

**Process:**
1. Write detailed prompt for character (appearance, pose, style)
2. Generate character image using Stable Diffusion with custom LoRA
3. Iterate on prompt/seed until satisfactory result
4. Save final character image (high resolution recommended)

**Tools:** See [[Tools]] - Stable Diffusion implementation

**Prompt Guidelines:**
- Reference 90s anime aesthetic (see [[ArtOverview]])
- Specify neutral/T-pose for rigging compatibility
- Request front view initially (other angles in next step)
- Include style keywords consistent with LoRA training
- Specify simple, clear silhouette (matches The Red Turtle inspiration)

**LoRA Requirements:**
- Train LoRA on custom art style (see [[Tools]] for training workflow)
- Test LoRA with sample prompts before full character generation
- Validate style consistency across multiple generations
- Document effective prompts for future characters

**Image Quality Checks:**
- Clear silhouette and readable shape
- Proportions appropriate for animation
- Style consistent with game's aesthetic
- Sufficient detail for 2D→3D conversion

**✓ CHECKPOINT: Generated Character Approval**

**CRITICAL STOP POINT**

This is the most important checkpoint in the entire pipeline. A bad character design here wastes all downstream work.

**Evaluation Questions:**
- Is this character visually appealing?
- Does it match the intended design/concept?
- Will it work in-game (size, readability)?
- Is the style consistent with other characters?
- Does it fit the game's overall aesthetic?

**If NO to any question:** Generate new variations; do NOT proceed

**If YES:** Save approved image and proceed to Step 2

---

### Step 2: Character Sheet Creation

**Goal:** Generate multi-angle views and poses for 3D conversion

**Process:**
1. Extract pose skeleton from approved character using OpenPose
2. Generate additional angles (front, side, 3/4, back)
3. Generate additional poses (if needed for rigging reference)
4. Compile into character sheet

**Tools:** See [[Tools]] - OpenPose/pose estimation options

**Angles Needed:**
- **Front view** (already from Step 1)
- **Side view** (critical for side-scrolling game)
- **3/4 view** (helps 3D conversion)
- **Back view** (optional, depends on 2D→3D tool requirements)

**Pose Consistency:**
- Use same LoRA settings for all angles
- Same character prompt (only change angle)
- Same seed if possible (or similar seeds for consistency)
- Validate proportions match across angles

**Character Sheet Format:**
- Arrange views in grid or lineup
- Consistent scale across all views
- Clean backgrounds (white or transparent)
- Label each angle clearly

**✓ CHECKPOINT: Character Sheet Completeness Check**
- All needed angles generated?
- Proportions consistent across views?
- Style matches approved character from Step 1?
- Ready for 3D conversion?

**Common Issues:**
- Proportion mismatch between angles (regenerate problem views)
- Style inconsistency (check LoRA settings)
- Poses not neutral enough for rigging (adjust prompts)

---

### Step 3: 2D to 3D Conversion

**Goal:** Convert 2D character sheet to 3D model

**Process:**
1. Prepare character sheet in required format for conversion tool
2. Run 2D→3D conversion (CLI tool - see [[Tools]])
3. Import resulting 3D model into Blender
4. Validate mesh quality and topology

**Tools:** See [[Tools]] - 2D→3D conversion options (TripoSR, Shap-E, etc.)

**Conversion Settings:**
- Output format: FBX or OBJ (Blender compatible)
- Resolution/detail level: Balance quality vs. polygon count
- Multi-view mode: Use all character sheet angles

**Mesh Validation:**
- Check in Blender viewport (solid and wireframe views)
- Verify humanoid proportions maintained
- Check for mesh errors (holes, inverted faces, non-manifold geometry)
- Assess topology for rigging (clean edge loops around joints)

**Mesh Cleanup (if needed):**
- Fix holes or inverted normals
- Remove floating vertices or duplicate geometry
- Simplify if polygon count excessive
- Ensure single manifold mesh (watertight)

**✓ CHECKPOINT: 3D Model Validation**
- Mesh resembles intended character?
- Topology clean enough for rigging?
- Proportions suitable for animation?
- No major errors or artifacts?

**If mesh quality poor:** Try different conversion settings or tool; may need to regenerate character sheet with clearer references

---

### Step 4: Auto-Rigging (Humanoid Only)

**Goal:** Automatically rig 3D character for animation

**Process:**
1. Export clean mesh from Blender (or use directly from conversion)
2. Run auto-rigging tool (see [[Tools]] - Mixamo, Rigify, etc.)
3. Import rigged character back into Blender
4. Validate rig (test basic poses)

**Tools:** See [[Tools]] - Auto-rigging options

**Humanoid Rigging Requirements:**
- Standard humanoid skeleton (biped)
- Major joints: spine, neck, head, shoulders, elbows, wrists, hips, knees, ankles
- Weight painting (automatic from rigging tool)
- FK/IK controls (depending on tool)

**Rig Validation:**
- Move each joint and verify deformation
- Test extreme poses (crouch, arms up, etc.)
- Check for broken weighting (mesh tearing or odd deformation)
- Verify skeleton hierarchy is standard

**Common Issues:**
- Poor auto-weighting (may need manual cleanup in Blender)
- Skeleton not aligned to mesh (adjust in rigging tool settings)
- Extra bones or non-standard hierarchy (simplify if possible)

**✓ CHECKPOINT: Rig Approval**
- All joints working correctly?
- Deformation acceptable for animation?
- Skeleton compatible with standard animations (see Step 5)?
- Ready for animation application?

**Non-Humanoid Note:**
For non-humanoid characters, this pipeline does not yet apply. Alternative rigging workflows TBD.

Document any non-humanoid character needs separately for future workflow development.

---

### Step 5: Animation Application

**Goal:** Apply premade animations to rigged character in Blender

**Process:**
1. Acquire animation files (FBX, BVH, etc. - see [[Tools]] for sources)
2. Import rigged character into Blender
3. Apply animation to character rig
4. Verify animation playback
5. Repeat for all needed animations

**Tools:** Blender + animation asset libraries (see [[Tools]])

**Animation Types Needed:**
- Idle
- Walk/run
- Jump
- Attack (shooting, melee)
- Hit reaction
- Death
- Special actions (context-specific)

**Animation Application Methods:**

**Manual (One-at-a-Time):**
1. Import animation FBX
2. Retarget to character rig (if needed)
3. Bake animation to character's bones
4. Export character with animation

**Automated (Batch Script - Recommended):**
Develop Python script for Blender (see [[Tools]] - Blender automation):
1. Point script at character file and animations directory
2. Script loops through all animations
3. Automatically applies, bakes, and exports each
4. Saves massive time for multiple animations

**Validation:**
- Animation plays back smoothly
- No broken joints or extreme deformation
- Timing/speed appropriate for game feel
- Looping animations loop cleanly

**✓ CHECKPOINT: Motion Validation in 3D**
- All needed animations applied successfully?
- Motion quality acceptable (no major artifacts)?
- Character deformation looks good during movement?
- Ready for rendering to 2D?

---

### Step 6: Side View Export

**Goal:** Render side-view animations from Blender for 2D conversion

**Process:**
1. Set up camera in Blender (side orthographic view)
2. Configure render settings (resolution, frame rate, output format)
3. Render animation to image sequence
4. Repeat for each animation

**Tools:** Blender rendering + automation script (see [[Tools]])

**Camera Setup:**
- **Orthographic projection** (no perspective distortion)
- **Side view** (90° from character's front)
- **Framing:** Enough space for character's full range of motion
- **Consistent across all animations** (don't move camera between renders)

**Render Settings:**
- **Resolution:** High enough for AI style conversion (e.g., 1024x1024 or higher)
- **Frame Rate:** Match game's target (e.g., 30fps, 60fps) or render higher and re-time later
- **Background:** Transparent or solid color (white/green for easy removal)
- **Output Format:** PNG sequence (numbered frames)
- **Lighting:** Flat/neutral (AI will re-light in style conversion) or omit lighting entirely

**Automation Script:**
Develop Python script to batch-process all animations:
1. Load character file with animation
2. Set up camera (if not already in scene)
3. Set output path (organize by animation name)
4. Render animation
5. Move to next animation
6. Repeat

See [[Tools]] for script development notes.

**✓ CHECKPOINT: Export Quality Check**
- Renders clean and clear?
- Animation motion preserved correctly?
- Framing consistent across all animations?
- File organization clear (easy to identify which animation is which)?

---

### Step 7: 3D to 2D Style Conversion

**Goal:** Convert 3D-rendered animations back to 2D art style using AI

**Process:**
1. Prepare rendered frames (image sequence from Step 6)
2. Use Stable Diffusion + LoRA to convert each frame to art style
3. Process entire animation sequence
4. Validate style consistency across frames

**Tools:** See [[Tools]] - Stable Diffusion img2img with LoRA

**Conversion Settings:**
- **img2img mode:** Use rendered frames as input
- **LoRA:** Same custom LoRA from character generation (Step 1)
- **Denoising strength:** Balance between keeping motion and applying style (test range: 0.3-0.7)
- **Prompt:** Style keywords + character description (consistent with Step 1)
- **Seed:** May vary per frame or use consistent seed (test both approaches)

**Batch Processing:**
- Process all frames of animation in sequence
- Maintain frame numbering/order
- Monitor for consistency issues (flickering, major style shifts)

**Frame-by-Frame Review:**
- Spot-check frames throughout animation
- Look for flickering or inconsistency
- Verify motion still reads clearly
- Ensure character design stays consistent

**✓ CHECKPOINT: Style Conversion Approval**
- AI conversion maintains character's design?
- Art style consistent with original approved character (Step 1)?
- Motion still clear and readable?
- Flickering acceptable or needs deflickering step?

**If major flickering:** Proceed to Step 8 (Deflickering)  
**If minimal flickering:** May skip Step 8 and proceed to Step 9

---

### Step 8: Deflickering (Conditional)

**Goal:** Reduce frame-to-frame inconsistencies from AI conversion

**Status:** Conditional - only if Step 7 produces noticeable flickering

**Process:**
1. Assess flickering severity (minor vs. major)
2. If minor: Proceed to Step 9 (may be acceptable or addressed by "human error" script)
3. If major: Apply deflickering tool/technique

**Tools:** See [[Tools]] - Deflickering options

**Deflickering Techniques:**

**Option A: Post-Processing Tools**
- After Effects or DaVinci Resolve deflicker plugins
- Temporal smoothing filters
- Optical flow frame blending

**Option B: Video Processing (FFmpeg)**
- Temporal filters (e.g., minterpolate, tmix)
- Frame averaging
- Command-line batch processing

**Option C: AI-Based Temporal Consistency**
- Models trained for video temporal consistency
- More advanced but may yield better results
- Research current options (field evolves rapidly)

**Settings/Intensity:**
- Balance between smoothing flicker and maintaining detail
- Too aggressive: Loss of detail, motion blur
- Too subtle: Flickering remains
- Test on short clip before processing full animations

**✓ CHECKPOINT: Flicker Assessment**
- Deflickering successful?
- Flickering reduced to acceptable level?
- No excessive blur or detail loss?
- Skip this step if deflickering not needed?

**Decision:**
- [ ] Deflickering applied successfully
- [ ] Deflickering skipped (not needed)
- [ ] Deflickering unsuccessful (try different tool/settings)

---

### Step 9: Normal Map Generation

**Goal:** Create normal maps for 2D sprites to enable dynamic lighting

**Two Approaches - Test Both and Decide:**

---

**Option A: From 3D Model (During Blender Phase)**

**When:** During/after Step 6 (render normal pass alongside color pass)

**Process:**
1. In Blender, set up normal map render pass
2. Render normal maps for each animation frame (same camera as color renders)
3. Save normal map image sequence alongside color sequence
4. Pair with final stylized 2D frames from Step 7

**Pros:**
- Geometrically accurate (matches 3D model's actual normals)
- Consistent and predictable
- Automated (part of Blender render process)
- No additional AI processing

**Cons:**
- May not match final 2D stylized look from AI conversion
- 3D model normals might not align with 2D art edges/details
- Less "hand-drawn" feeling

**Best For:**
- Accurate dynamic lighting
- Consistent results
- Characters with simple, clear shapes

---

**Option B: AI Generation (Post-2D Conversion)**

**When:** After Step 7 (generate from final stylized 2D frames)

**Process:**
1. Use AI tool to generate normal maps from 2D images
2. Options: ControlNet Normal, Substance Designer, specialized models
3. Process all animation frames
4. Validate normal map quality

**Tools:** See [[Tools]] - Normal map generation options

**Pros:**
- Matches final 2D art style (normals align with stylized edges)
- Can be more stylized/exaggerated
- May integrate better with hand-drawn aesthetic

**Cons:**
- Less geometrically accurate
- Additional processing step
- May have inconsistencies between frames
- Requires additional tool/workflow

**Best For:**
- Stylized lighting effects
- Characters with complex 2D details
- Maintaining hand-drawn aesthetic

---

**Testing & Decision:**

Test both options with a sample animation:
1. Render Option A normals during Blender export
2. Generate Option B normals from final 2D frames
3. Import both into UE5 with sprite material (see [[Materials2D]])
4. Compare under dynamic lighting

**Evaluation Criteria:**
- Which normals produce better lighting response?
- Which aligns better with final art style?
- Consistency across animation frames?
- Workflow complexity vs. result quality?

**✓ CHECKPOINT: Normal Map Quality Validation**
- Normal maps generated successfully?
- Lighting response acceptable in-engine (test in [[Materials2D]])?
- Approach decision made: Option A / Option B?
- Document decision for future characters?

**Decision:**
- [ ] Option A (3D-based normals) chosen
- [ ] Option B (AI-generated normals) chosen
- [ ] Hybrid approach (use both depending on character/situation)

---

### Step 10: "Human Error" Variation Script

**Goal:** Add imperfections and variations to avoid rotoscoped look

**Process:**
1. Run custom script on animation frames (see [[Tools]])
2. Apply randomized variations to frame positions, timing, and edges
3. Validate that variations enhance rather than distract

**Tools:** See [[Tools]] - Custom Python script (development needed)

**Script Parameters:**

**Frame Position Jitter:**
- Randomly offset frames by small pixel amounts (e.g., ±1-3 pixels X/Y)
- Creates subtle "bobble" effect like hand-drawn animation cels
- Avoid excessive jitter (too distracting)

**Line Edge Variation:**
- Subtle edge distortion or noise
- Mimics natural hand-drawn line wobble
- May require pixel-level processing (edge detection + noise)

**Timing Variation (Frame Holds):**
- Randomly hold certain frames for extra frames (limited animation technique)
- E.g., 2-frame holds scattered throughout animation
- Avoid mechanical smoothness of rotoscoping

**Noise Seed:**
- Consistent seed for predictable variation (per animation)
- Random seed for more organic feel
- Test both approaches

**Script Development:**
See [[Tools]] for implementation notes. Key steps:
1. Load animation frames
2. Apply jitter to frame positions (image translation)
3. (Optional) Apply edge variation (pixel processing)
4. (Optional) Insert frame holds based on timing rules
5. Export modified frames

**Inspiration:** 90s anime limited animation (see [[ArtOverview]])

**✓ CHECKPOINT: "Human Error" Effect Approval**
- Variations enhance aesthetic (not distracting)?
- Avoids rotoscoped/sterile look successfully?
- Maintains readability and motion clarity?
- Effect consistent with game's art direction?

**Adjustment:**
- If too subtle: Increase jitter amount, add more holds
- If too extreme: Reduce parameters, disable edge variation
- If inconsistent: Adjust seed/randomization approach

---

### Step 11: Re-timing

**Goal:** Adjust animation timing for game feel and anime aesthetic

**Two Approaches:**

---

**Option A: Automated (Preferred if Available)**

**Process:**
1. Research AI-based or algorithmic re-timing tools (see [[Tools]])
2. Define timing rules (holds, speed changes, smears)
3. Apply to animation automatically
4. Validate results

**Benefits:**
- Fast, repeatable
- Consistent application of timing rules
- Easy to iterate and adjust

**Challenges:**
- May not exist yet (research current tools)
- May require custom development
- Difficult to match artistic intent automatically

**Status:** Research needed - see [[Tools]]

---

**Option B: Manual (DaVinci Resolve)**

**Process:**
1. Import animation frames into DaVinci Resolve
2. Place frames on timeline
3. Manually adjust timing (extend frames, speed changes, reorder)
4. Export re-timed animation

**Tools:** DaVinci Resolve (see [[Tools]])

**Timing Techniques:**
- **Holds:** Extend important frames (anticipation, impact, follow-through)
- **Speed changes:** Slow-in/slow-out for weight, fast actions for impact
- **Frame removal:** Speed up overly-smooth sections
- **Smear frames:** Brief blur frames on very fast actions (may not be needed)

**Anime Timing Principles:**
- Not every frame needs to be unique (holds create emphasis)
- Vary timing (not constant frame rate)
- Anticipation and follow-through more important than smooth motion

**Benefits:**
- Full creative control
- Can make artistic decisions per animation
- No tool development needed

**Challenges:**
- Time-consuming for many animations
- Requires animation knowledge/skill
- Less consistent across animations

---

**✓ CHECKPOINT: Timing Approval**
- Animation timing feels good (game feel)?
- Matches anime aesthetic (limited animation techniques)?
- Motion clear and readable?
- Approach decided: Automated / Manual?

**Decision:**
- [ ] Automated re-timing tool found and used
- [ ] Manual re-timing in DaVinci Resolve
- [ ] Re-timing skipped (initial timing from Blender acceptable)

---

### Step 12: Sprite Sheet Conversion

**Goal:** Convert final animation frames to sprite sheet for UE5

**Process:**
1. Prepare final animation frames (after all previous steps)
2. Use sprite sheet tool to pack frames (see [[Tools]])
3. Generate metadata (frame positions, dimensions)
4. Import to UE5

**Tools:** See [[Tools]] - TexturePacker, Shoebox, custom script, etc.

**Sprite Sheet Settings:**
- **Layout:** Grid (uniform frame size) or packed (optimized for space)
- **Power-of-Two:** Texture dimensions (1024, 2048, 4096, etc.)
- **Padding:** Space between frames to avoid bleeding
- **Trim:** Remove empty space around frames (optional)

**Metadata:**
- Frame positions (X, Y coordinates in sprite sheet)
- Frame dimensions (width, height)
- Animation frame count
- Frame rate (if embedded)

**Output:**
- Sprite sheet image (PNG, usually)
- Metadata file (JSON, XML, or tool-specific format)

**Organization:**
- One sprite sheet per animation, or
- Multiple animations per sheet (if similar dimensions)
- Consistent naming convention

**✓ CHECKPOINT: Sprite Sheet Validation**
- All frames packed correctly?
- No frame bleeding or artifacts?
- Metadata accurate?
- Ready for UE5 import?

---

### Step 13: UE5 Integration

**Goal:** Import sprite sheet and set up material for in-engine use

**Process:**
1. Import sprite sheet texture to UE5
2. Import normal map texture (from Step 9)
3. Create sprite material (see [[Materials2D]])
4. Set up Paper2D flipbook or sprite animation
5. Test in-game with dynamic lighting

**UE5 Setup:**

**Paper2D Flipbook:**
- Create flipbook asset
- Import sprite sheet frames
- Set frame duration/timing
- Configure looping

**Sprite Material:**
- See [[Materials2D]] for full setup
- Assign albedo (sprite sheet texture)
- Assign normal map (from Step 9)
- Configure lighting response
- Set up transparency

**Dynamic Lighting Test:**
- Place sprite in test level
- Add moving point lights
- Verify normal map lighting response
- Adjust material if needed

**✓ CHECKPOINT: In-Engine Lighting Test**
- Sprite displays correctly in UE5?
- Animation plays smoothly?
- Normal maps react to dynamic lighting as expected?
- Performance acceptable?

**If successful:** Animation ready for gameplay integration  
**If issues:** Troubleshoot material setup (see [[Materials2D]]) or revisit normal map generation (Step 9)

---

## Progress Tracking

### Tool Selection & Setup
- [ ] Stable Diffusion implementation chosen (see [[Tools]])
- [ ] LoRA training workflow established (see [[Tools]])
- [ ] LoRA trained on custom art style
- [ ] OpenPose/pose tool selected (see [[Tools]])
- [ ] 2D→3D conversion tool selected (see [[Tools]])
- [ ] Auto-rigging tool selected (see [[Tools]])
- [ ] Animation source library chosen (see [[Tools]])
- [ ] Blender automation scripts developed (see [[Tools]])
- [ ] Normal map generation approach decided: Option A / Option B
- [ ] Deflickering tool selected (if needed - see [[Tools]])
- [ ] "Human error" script developed (see [[Tools]])
- [ ] Re-timing approach decided: Automated / Manual
- [ ] Sprite sheet tool selected (see [[Tools]])

### Pipeline Testing
- [ ] First character completed through full pipeline: Date _______
- [ ] Pipeline documentation validated and updated
- [ ] Normal map approach tested and finalized
- [ ] "Human error" script parameters tuned
- [ ] Re-timing workflow established
- [ ] Performance benchmarked in UE5

### Character Production
- [ ] Player character animation set completed
- [ ] Companion character animation set completed
- [ ] Enemy type 1 animations: _______
- [ ] Enemy type 2 animations: _______
- [ ] Boss animations: _______
- [ ] NPC animations: _______

---

## Tips & Best Practices

### Character Generation (Steps 1-2)
- Build prompt library for consistent character style
- Save successful seeds/settings for future use
- Generate multiple candidates before choosing (easier to approve good design than fix bad one)
- Test LoRA thoroughly before starting production characters

### 3D Conversion & Rigging (Steps 3-4)
- Keep reference images of approved 2D character visible during validation
- Document which conversion settings work best (reuse for future characters)
- Test rig with extreme poses, not just subtle ones
- Build library of successful auto-rigging profiles

### Animation & Rendering (Steps 5-6)
- Organize animation files clearly (folder structure, naming conventions)
- Develop automation scripts early (saves massive time for multiple characters)
- Use consistent Blender scene setup for all characters
- Batch render overnight for long animations

### AI Style Conversion (Step 7)
- Test denoising strength with short clip before processing full animations
- Monitor first few frames closely (catch issues early)
- Keep original 3D renders (can re-convert if AI settings need adjustment)
- Expect some trial and error - AI conversion is least predictable step

### Timing & Polish (Steps 10-11)
- Study reference animations (90s anime) for timing inspiration
- "Human error" should be subtle - easily overdone
- Re-timing has huge impact on feel - worth time investment
- Get feedback from gameplay tests (does it feel good in-game?)

### Technical Integration (Steps 12-13)
- Test sprite sheet early with placeholder material
- Validate normal map lighting before completing all animations
- Keep sprite sheet texture sizes reasonable (performance vs. quality)
- Document material setup for reuse with future characters

---

## Common Pitfalls

### Character Generation
- **Rushing approval at Step 1:** Most costly mistake - always get character design right first
- **Inconsistent LoRA settings:** Causes style variations between characters
- **Overly complex character designs:** Harder to convert and animate

### 3D Conversion
- **Poor topology from conversion:** May need to try different tools or settings
- **Proportions changing during conversion:** Use character sheet with clear references
- **Skipping mesh validation:** Problems multiply in later steps

### Animation Pipeline
- **Not automating Blender export:** Wastes hours on repetitive tasks
- **Inconsistent camera/render settings:** Causes frame size mismatches
- **Forgetting to save Blender files:** Can't re-render if issues found later

### AI Style Conversion
- **Flickering ignored:** Becomes very noticeable in-game
- **Denoising too strong:** Loses motion detail and character consistency
- **Not checking frame-by-frame:** Easy to miss issues in bulk processing

### Finishing & Integration
- **Skipping "human error" step:** Animations feel too sterile/CG
- **Poor re-timing:** Ruins otherwise good animation
- **Normal maps misaligned:** Lighting looks wrong in-game
- **Sprite sheet organization chaos:** Hard to maintain and debug

---

## Non-Humanoid Workflow

**Current Status:** TBD - This pipeline currently only supports humanoid characters

For non-humanoid characters (creatures, animals, abstract entities):

**Challenges:**
- Auto-rigging tools typically humanoid-specific
- Standard animation libraries may not fit
- Skeleton/rig needs custom development

**Potential Approaches:**
1. **Manual rigging in Blender:** Skip Step 4 auto-rigging, rig by hand
2. **Procedural animation:** Generate motion procedurally (walk cycles, flight, etc.)
3. **Simpler animation:** Frame-by-frame 2D without 3D intermediate step
4. **Hybrid:** Use parts of this pipeline where applicable

**Document separately when non-humanoid characters are needed.**

---

## Related Documentation

- **[[ArtOverview]]** - Vision, 90s anime inspiration, "human error" aesthetic
- **[[Tools]]** - Complete tool selection and status
- **[[Materials2D]]** - Sprite material setup, normal map integration
- **[[ColorPalettes]]** - Color selection for character design
- **[[Pipeline3D]]** - Comparison with 3D asset workflow
- **[[Lighting]]** - How dynamic lights interact with sprite normal maps

---

## Next Steps

1. Set up Stable Diffusion and train custom LoRA (see [[Tools]])
2. Generate first test character and run through complete pipeline
3. Validate each step and document actual settings/tools used
4. Make normal map approach decision (Option A vs. B)
5. Develop automation scripts (Blender export, "human error")
6. Determine re-timing workflow (automated vs. manual)
7. Refine pipeline based on first test and document lessons learned
8. Begin production of player character animation set
