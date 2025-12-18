# Companion Mechanics - "Her"

> **Status**: Design Exploration  
> **Last Updated**: 2025-12-17

---

## Overview

"Her" is the companion character who follows the player throughout their journey in Lament. She serves as the player's only source of healing, but every heal comes at the cost of her own vitality. Her mechanics are designed to create emotional weight through visible, mechanical consequences - making every healing decision feel significant and costly.

**Design Goals**:
- Always accessible for healing (teleport from anywhere)
- Clear visual/behavioral feedback of her declining state
- Never interferes with combat or platforming (immune, untargeted, floats over terrain)
- Checkpoint-based recovery system that provides relief
- Silent companion (emotion through animation and sound, not dialogue)

**Design Philosophy**:
- Hybrid following AI creates character personality without pathfinding complexity
- Peach-style floating smooths movement transitions and prevents awkward falling
- Discrete vitality stages with continuous speed degradation show cost of healing
- She's not a helper - she's a sacrifice you must make to survive
- Success means using her less, not more (inverted companion design)

**Cross-References**:
- [[PlayerMovement]] - Healing mechanics integration, movement during heal
- [[Systems/GameFeel]] - Visual/audio feedback techniques, animation juice
- [[Narrative/Her]] - (Future) Character identity, emotional arc, narrative role
- [[Systems/HealthDamage]] - (Future) Player health system, fail states
- [[Overview]] - Core companion sacrifice mechanic, design pillars

---

## Following Behavior

### Hybrid Following System

Her following AI uses a **hybrid approach** that combines character-driven movement with smooth rubber-banding:

**Normal Movement (Diddy Kong-style)**:
- Activates when player walks/runs at normal speed
- She follows with her own walking/running animation
- Maintains set distance behind player
- Shows character personality and allows degradation to be visible
- Creates emotional presence - she feels like a person, not an object

**Advanced Movement (Rubber Band-style)**:
- Activates when player uses dash, wall jump, slide-jump, or other fast movement
- She smoothly transitions to rubber band mode
- Maintains position relative to player without complex pathfinding
- Uses floating mechanic to keep up naturally
- Prevents her from being left behind during skilled movement

**Design Rationale**: 
- Normal following creates character presence and personality during slow gameplay
- Rubber band ensures she never interferes with fast-paced platforming/combat
- Hybrid approach provides personality without pathfinding complexity
- Transition between modes should be subtle and natural

**Design Questions**:
- [ ] Follow distance behind player (units/pixels)
- [ ] Speed threshold for triggering rubber band mode (when player exceeds X speed)
- [ ] Transition smoothness between normal following and rubber band
- [ ] Catch-up speed when rubber banding
- [ ] Does she avoid obstacles during normal following or move through them?

---

### Floating Mechanic

**Concept**: Inspired by Peach in Super Smash Bros - she floats/descends slowly rather than falling normally.

**Mechanics**:
- She descends gently when airborne instead of falling with normal gravity
- Makes rubber banding look natural (she floats to keep up)
- Smooths transition between normal following and rubber band mode
- No need to solve platforming puzzles (she floats over gaps and obstacles)
- Prevents awkward falling/terrain navigation issues

**Design Rationale**: 
- Floating gives visual justification for rubber band movement
- Prevents situations where she'd need complex jump/climb AI
- Creates dreamlike, ethereal quality that fits the surreal tone
- Allows her to always stay near player without looking broken

**Design Questions**:
- [ ] Float descent speed (how fast does she descend?)
- [ ] Visual effect for floating (particle trail, animation, etc.)
- [ ] Does floating activate only during rubber band or always when airborne?
- [ ] Float vs normal fall transition (gradual or instant?)

---

### Teleport System

**Triggers**:
1. **Distance Threshold**: When she gets too far from player, she teleports back
2. **Heal Call**: When player presses heal button, she teleports to player immediately

**Mechanics**:
- Teleport-out effect at old position
- Instant repositioning
- Teleport-in effect at new position
- Returns to following state after teleport completes

**Design Rationale**: 
- Ensures she never gets permanently stuck or lost
- Heal teleport allows consistent animation timing (fixed frame count)
- Distance teleport is failsafe for edge cases
- Prevents frustration from companion pathfinding failures

**Design Questions**:
- [ ] Distance threshold before teleport triggers (how far?)
- [ ] Teleport duration (frames/milliseconds)
- [ ] Teleport visual/audio effects
- [ ] Heal teleport position (next to player? specific offset?)
- [ ] Can teleport be interrupted or always completes?

---

### Positioning & Combat Behavior

**Positioning**:
- Stays behind player during normal gameplay
- Maintains consistent distance when following
- Moves to player position during heal (teleport)
- Returns to behind-player position after heal completes

**Combat Immunity**:
- **Immune to all damage** from enemies and environment
- **Not targeted by enemy AI** - enemies ignore her completely
- **Doesn't block player** - player can move through her
- **Doesn't block projectiles** - enemy/player projectiles pass through her
- **Only healing can harm her** - her vitality only decreases when player heals

**Design Rationale**: 
- She never interferes with combat or platforming
- Players can't "lose" her to enemy damage
- Focus remains on player skill, not companion protection from external threats
- Her only vulnerability is to your healing choices (emotional weight)

**Design Questions**:
- [ ] Exact positioning offset (directly behind, slight angle, variable?)
- [ ] Does she try to avoid standing in hazards even though immune?
- [ ] Visual feedback when enemies attack through her (shows immunity)?

---

## Healing System

### Activation & Teleport

**Button Press**:
- Single button press from anywhere in the level
- No range restriction - she always responds
- Cannot be used when heal count = 0 (no charges remaining)

**Immediate Teleport**:
- Pressing heal button triggers instant teleport to player
- Teleport-out effect at her current position
- Teleport-in effect at player position (or nearby offset)
- Ensures consistent animation timing regardless of where she was

**Design Rationale**: 
- Always accessible healing removes frustration of "companion too far away"
- Teleport-to-player allows fixed animation duration (consistent frames)
- Maintains combat flow - no waiting for her to path to you
- Button press (not hold) allows quick activation in frantic moments

**Design Questions**:
- [ ] Heal button input (dedicated button or context-sensitive?)
- [ ] Teleport destination (exact player position or offset?)
- [ ] Visual effect for heal teleport (different from distance teleport?)
- [ ] Audio cue when heal button pressed (before teleport)
- [ ] Can queue heal input during cooldown/animation?

---

### Heal Animation & Mechanics

**Animation**:
- **Fixed duration** - consistent frame count every time
- **Shows her suffering** - pain expression, effort, visible cost
- **Cannot be cancelled** - once initiated, must complete
- **Silent but expressive** - no voice lines, but pain sounds (breathing, gasps)

**Player State During Heal**:
- **Can move** (planned - pending playtesting confirmation)
- **Cannot cancel heal** - animation must play to completion
- **Fast animation** - quick enough to use in combat without excessive vulnerability
- Movement speed during heal: TBD (full speed, reduced, or locked?)
- Can perform other actions? TBD (shoot, jump, dash?)

**Heal Effect**:
- Restores **fixed HP amount** to player (value TBD)
- Consumes **one heal charge**
- Player health bar increases
- Her vitality decreases (visible through behavior/appearance)
- UI updates to show remaining heals

**Design Rationale**: 
- Fixed duration prevents heal spamming while allowing combat use
- Her visible suffering creates emotional cost of healing
- Cannot cancel prevents abuse (commitment to heal choice)
- Movement during heal (tentative) maintains player agency
- Silent pain sounds create intimacy without dialogue

**Design Questions**:
- [ ] Heal animation duration (frames/milliseconds)
- [ ] Exact heal amount (HP value or percentage of max HP?)
- [ ] Player movement speed during heal (full, reduced, locked?)
- [ ] Can player attack/jump/dash during heal animation?
- [ ] Cooldown between heals or instant re-use if charges available?
- [ ] Visual effect on player during heal (glow, particles, health transfer?)
- [ ] Does heal interrupt player's current action (attack, dash, etc.)?

---

### Heal Resource System

**Discrete Heal Count**:
- Player has a **finite number of heals** available
- Each heal consumes one charge
- Heal count shown on **UI bar**
- Not percentage-based - discrete, countable charges (like Dark Souls Estus)

**Zero Heals State**:
- When heals = 0: **Player cannot heal anymore**
- **Not immediate game over** - player can still proceed if skilled enough
- She appears **extremely weak** visually at 0 heals
- Creates desperation to reach next checkpoint
- Makes game significantly harder (no healing safety net)

**Checkpoint Recovery**:
- **All heal charges restore** at checkpoints/save points
- Her visual state returns to "Healthy"
- Movement speed returns to maximum
- Animation state resets to healthy group
- Provides relief and highlights what was lost

**Design Rationale**: 
- Discrete charges make each heal feel significant (not just -10% of bar)
- Zero heals = can't heal creates tension without instant failure
- Checkpoint recovery provides relief and reset point
- Similar to Estus Flask system - limited resource that refills at safe points

**Design Questions**:
- [ ] Total heals per checkpoint (5? 10? Variable by difficulty/progression?)
- [ ] Does heal count vary by level/difficulty or stay consistent?
- [ ] Visual representation in UI (number, icons, bar segments?)
- [ ] What happens if player tries to heal at 0 charges? (button doesn't work? Error feedback?)
- [ ] Checkpoint recovery: instant or brief animation/transition?

---

## Vitality & Degradation System

### Visual & Behavioral Indicators

**UI Display**:
- Heal count bar showing remaining charges
- Potentially icon/portrait showing her current state
- Clear, readable display that doesn't clutter screen

**Animation States (3 Distinct Groups)**:
1. **Healthy** (High heal count remaining)
   - Normal walk/run animations
   - Upright posture
   - Smooth, confident movement
   
2. **Weak** (Mid heal count remaining)
   - Slower animations
   - Slight limp beginning
   - Tired posture, fatigue showing
   
3. **Weaker** (Low heal count remaining)
   - Pronounced limp
   - Struggling to move
   - Hunched, exhausted posture
   - Barely able to keep up (relies heavily on rubber band)

*Note: Better naming for these states TBD (e.g., Healthy/Tired/Exhausted, Vibrant/Fading/Depleted)*

**Movement Speed Degradation**:
- Movement speed **decreases continuously** relative to heals remaining
- Creates smooth degradation even within same animation state
- More heals used = slower she moves = more obvious rubber banding needed
- At 0 heals, she moves at minimum speed (barely walking)

**Design Rationale**: 
- UI provides mechanical information (how many heals left?)
- Animation states provide emotional information (how much is she suffering?)
- Continuous speed degradation ensures smooth decline, not stepped changes
- Slower movement makes rubber band more prominent (visual reminder of cost)

**Design Questions**:
- [ ] Heal count thresholds for animation state transitions (e.g., Healthy: 10-7, Weak: 6-3, Weaker: 2-0?)
- [ ] Movement speed degradation formula (linear, exponential, stepped?)
- [ ] Maximum movement speed (healthy state, as % of player speed)
- [ ] Minimum movement speed (0 heals state)
- [ ] Better names for the 3 animation states?
- [ ] Do different vitality stages affect heal animation speed/effectiveness?

---

### Visual Appearance Changes

As her vitality decreases, her appearance should reflect the cost:

**Potential Visual Markers** (TBD based on art direction):
- Posture changes (upright → slouched → hunched)
- Facial expression (calm → pained → exhausted)
- Wounds or fatigue marks appearing
- Pale skin or loss of color
- Torn/disheveled clothing
- Dark circles, visible exhaustion
- Particle effects (healthy glow fading, dark aura appearing)

**Design Rationale**: 
- Visual changes make mechanical cost emotionally visible
- Gradual degradation creates guilt and consequence
- Players should feel the weight of their healing choices
- Appearance should tell story of accumulated suffering

**Design Questions**:
- [ ] How drastic should visual changes be? (subtle vs obvious)
- [ ] Specific visual markers per animation state?
- [ ] Permanent appearance changes within checkpoint or reset each heal?
- [ ] Particle effects for vitality states (glow when healthy, dark aura when weak?)
- [ ] Should 0 heals state look critically injured or just completely exhausted?

---

### Fail State & Recovery

**Dual Fail State**:
- **Player Death**: Player health reaches 0 → game over
- **Companion Depletion**: Heal count reaches 0 → can't heal, game becomes much harder

**At Zero Heals**:
- Cannot heal anymore (button press has no effect)
- She appears extremely weak (worst visual state)
- Game continues - player must reach checkpoint without healing
- Creates desperation and tension
- Rewards skilled play (can proceed without healing if good enough)

**Checkpoint Recovery**:
- Reaching checkpoint/save point fully restores all heal charges
- Her visual state instantly (or smoothly) returns to healthy
- Movement speed resets to maximum
- Animation state returns to "Healthy" group
- UI updates to show full heal count

**Design Rationale**: 
- Zero heals ≠ game over allows skilled players to recover
- Checkpoint recovery provides relief and clean slate
- Recovery highlights what was lost (seeing her healthy again after suffering)
- Creates rhythm of degradation → relief → degradation

**Design Questions**:
- [ ] Audio/visual feedback when reaching 0 heals? (warning, UI change?)
- [ ] Checkpoint recovery: instant snap or transition animation?
- [ ] Does she show relief/happiness when restored at checkpoint?
- [ ] Recovery timing (instant on touching checkpoint or delayed?)
- [ ] Visual transition from weak to healthy (fade, animation, instant?)

---

## AI Behavior States

### State Definitions

**Idle**:
- **Trigger**: Player is stationary
- **Behavior**: Plays idle animation loop
- **Variations**: Different idle animations per vitality stage (healthy idle vs exhausted idle)
- **Optional**: Subtle environmental reactions (looking around, slight movements)

**Following - Normal**:
- **Trigger**: Player moving at walk/run speed
- **Behavior**: Diddy Kong-style following with walk/run animations
- **Maintains**: Set distance behind player
- **Speed**: Matches player speed (within degradation limits)

**Following - Rubber Band**:
- **Trigger**: Player uses advanced movement (dash, wall jump, slide-jump, fast movement)
- **Behavior**: Smoothly maintains position relative to player
- **Uses**: Floating mechanic to keep up
- **Speed**: Instantly matches player position (lerp/spring physics)

**Teleporting**:
- **Triggers**: 
  - Distance threshold exceeded
  - Heal button pressed
- **Behavior**: 
  - Teleport-out effect at current position
  - Instant repositioning
  - Teleport-in effect at new position

**Healing**:
- **Trigger**: Heal button pressed (teleport completes, then heal begins)
- **Behavior**: 
  - Plays healing animation (shows suffering)
  - Locked duration, cannot be interrupted
  - Player HP restored on completion
  - Heal charge consumed
- **After**: Returns to following state

---

### State Transitions

**Flow Diagram**:
```
Idle ↔ Following Normal (player starts/stops moving)
Following Normal ↔ Following Rubber Band (player speed changes)
Any State → Teleporting (distance threshold or heal call)
Teleporting → Healing (if heal triggered) OR Following Normal (if distance teleport)
Healing → Following Normal (after animation completes)
```

**Transition Smoothness**:
- Transitions should be smooth and natural
- No jarring snaps or instant changes (except teleport, which is intentional)
- Blend animations when transitioning between states
- Maintain player's sense of her as a character, not a system

**Design Questions**:
- [ ] Idle → Following transition timing (instant or brief delay?)
- [ ] Following Normal ↔ Rubber Band blend duration
- [ ] Does she return to Idle if player stops during rubber band, or stay in following?
- [ ] Teleport priority (can teleport interrupt healing or other states?)
- [ ] State priorities when multiple triggers occur simultaneously

---

## Animation States

### Required Animations

**Per Vitality Stage (3 groups: Healthy, Weak, Weaker)**:
- **Idle** - Standing still, breathing, subtle movement
- **Walk** - Normal walking locomotion
- **Run** - Faster movement (if distinct from walk)
- **Limp** - Especially important for weak stages, pronounced struggle

**Universal Animations (Same across all vitality stages)**:
- **Teleport Out** - Disappearing effect/animation
- **Teleport In** - Appearing effect/animation
- **Healing** - Shows suffering, pain, effort during heal transfer
- **Floating/Descent** - Peach-style slow fall/hover
- **Extreme Weakness** - Special state at 0 heals (barely standing/shuffling)

**Optional/Future Animations**:
- Checkpoint recovery (weak → healthy visual transition)
- Environmental reactions (idle variations based on context)
- Player damage reaction (worried look when player takes damage)
- Different healing animations per vitality stage (more suffering when weak?)

---

### Animation Progression by Vitality

**Healthy State**:
- Upright posture
- Smooth, fluid movement
- Normal walk/run cycle
- Alert, present idle animations
- Minimal signs of fatigue

**Weak State**:
- Slightly slouched posture
- Slower movement cycle
- Beginning to limp
- Tired idle animation (labored breathing)
- Visible fatigue

**Weaker State**:
- Hunched, struggling posture
- Very slow movement
- Pronounced limp, stumbling
- Exhausted idle (barely standing)
- Critical fatigue, on verge of collapse

**0 Heals (Extreme Weakness)**:
- Near-collapse posture
- Minimal movement (shuffling)
- Can barely walk
- Idle shows extreme exhaustion
- Visual peak of suffering

**Design Questions**:
- [ ] Animation blending between vitality stages (gradual or instant transition?)
- [ ] How many walk/run variations needed per stage? (1 set per stage or more?)
- [ ] Should healing animation differ by vitality stage? (shows more pain when weaker?)
- [ ] Transition animations between states or just cross-fade?
- [ ] Animation lock duration for various states?

---

## Visual & Audio Feedback

### Visual Effects

**Teleport**:
- Teleport-out effect at departure point (fade, particles, magical burst)
- Teleport-in effect at arrival point
- Brief moment of visibility/invisibility during teleport
- Distinct from normal movement (clearly supernatural)

**Healing**:
- Particle effect transferring from Her to player
- Visual indication of pain/suffering on her (expression, posture, particle color)
- Glow or aura on player receiving healing
- Clear visual moment when heal completes and HP restores

**Vitality Stages**:
- Posture changes across animation states
- Appearance degradation (wounds, fatigue markers, color loss)
- Potentially particle effects (healthy glow fading, dark aura appearing when weak)
- Movement quality (smooth → struggling → stumbling)

**UI Elements**:
- Heal count bar (clear, readable)
- Potentially portrait/icon showing her current state
- Visual warning when heals running low
- Clear feedback when heal count = 0

**Design Questions**:
- [ ] Teleport effect style (fade, particles, magical burst, other?)
- [ ] Healing particle direction/flow (Her → Player visualization)
- [ ] Vitality stage visual markers (how drastic should appearance changes be?)
- [ ] Particle effects for floating (trail, sparkles, aura?)
- [ ] UI design for heal count (bar, icons, numbers, portrait?)

---

### Audio Feedback

**Movement Sounds**:
- **Footsteps**: Sound changes based on vitality
  - Healthy: Normal footstep sounds
  - Weak: Dragging, heavier footsteps
  - Weaker: Shuffling, struggling sounds
- **Floating**: Subtle magical/wind sound during floating descent
- **Ambient Presence**: Potentially subtle sound indicating her proximity

**Teleport**:
- Teleport-out sound (whoosh, magical effect)
- Teleport-in sound (arrival effect)
- Distinct from normal movement sounds

**Healing**:
- Pain sounds from her (breathing, gasps, effort - **no words**)
- Magical transfer sound (energy moving from her to player)
- Player restoration sound (healing complete)
- Potentially different pain sounds based on vitality stage (more distressed when weak?)

**Vitality States**:
- **Healthy**: Normal breathing, quiet presence
- **Weak**: Labored breathing, occasional sounds of effort
- **Weaker**: Heavy breathing, struggle sounds, pain indicators
- **0 Heals**: Extreme exhaustion sounds, barely audible breathing

**Silent Companion**:
- **No voice lines or dialogue**
- Only non-verbal vocalizations (pain, breathing, effort sounds)
- Emotion conveyed through sound design and animation, not words
- Creates intimacy without dialogue dependency

**Design Questions**:
- [ ] Footstep sound variations (3 different sets per stage or continuous change?)
- [ ] Pain sounds during healing (subtle vs pronounced, how distressing?)
- [ ] Breathing audio (constant or triggered by context?)
- [ ] Audio cue for state transitions (sounds when entering weak/weaker states?)
- [ ] Teleport audio (same sound for distance teleport vs heal teleport?)
- [ ] Should audio be diagetic (exists in world) or non-diagetic (for player only)?

---

## Design Questions & To Be Determined

### Following Behavior

- [ ] Follow distance behind player (units/pixels/meters)
- [ ] Teleport distance threshold (how far before auto-teleport?)
- [ ] Speed threshold for triggering rubber band mode (player speed value)
- [ ] Transition speed between normal following and rubber band
- [ ] Rubber band catch-up speed (how quickly she matches player position?)
- [ ] Float descent speed (Peach-style falling rate)
- [ ] Does she avoid obstacles during normal following or move through them?
- [ ] Collision handling (passes through terrain, avoids obstacles, hybrid?)
- [ ] Following AI implementation (navmesh, direct positioning, lerp, spring physics?)

---

### Healing Mechanics

- [ ] Exact heal amount (HP value or percentage of max HP?)
- [ ] Heal animation duration (frames/milliseconds)
- [ ] Player movement speed during heal (full speed, reduced percentage, or locked?)
- [ ] Can player attack during heal animation?
- [ ] Can player jump during heal animation?
- [ ] Can player dash during heal animation?
- [ ] Cooldown between heals or instant re-use if charges available?
- [ ] Visual effect on player during heal (glow color, particle style, intensity)
- [ ] Heal teleport distance/position (exact player location or offset?)
- [ ] Does heal interrupt player's current action (attack, dash, etc.)?
- [ ] Audio cue timing (button press, teleport start, heal start, heal complete?)

---

### Vitality System

- [ ] Total heal count per checkpoint (5? 10? Variable by difficulty/progression?)
- [ ] Heal count thresholds for animation state transitions:
  - Healthy: X to Y heals remaining
  - Weak: X to Y heals remaining
  - Weaker: X to 0 heals remaining
- [ ] Movement speed degradation formula (linear, exponential, stepped?)
- [ ] Maximum movement speed when healthy (as % of player speed)
- [ ] Minimum movement speed at 0 heals
- [ ] Do different vitality stages affect heal animation duration or effectiveness?
- [ ] Visual appearance changes per stage (specific wounds, color changes, particle effects?)
- [ ] Better names for the 3 animation states? (Healthy/Weak/Weaker alternatives)
- [ ] Does heal count vary by level/world or stay consistent throughout game?

---

### AI Behavior

- [ ] Idle animation variations (random, timed, or environmental triggers?)
- [ ] Does she react to player taking damage (concerned animation, flinch)?
- [ ] Does she react to nearby enemies even though she's immune?
- [ ] Does she react to environmental hazards or just passes through?
- [ ] Behavior during player wall climb/wall jump (stay in rubber band mode?)
- [ ] Positioning preference (directly behind, slight offset left/right, variable?)
- [ ] Does she close gap when player stops or maintain distance?
- [ ] State transition blend durations (instant, 0.1s, 0.5s?)
- [ ] How to detect "advanced player movement" for rubber band trigger?
- [ ] Can teleport interrupt other states (healing, idle, animations)?

---

### Checkpoint Recovery

- [ ] Instant heal restoration or brief animation/transition?
- [ ] Visual transition from weak to healthy (snap change, fade, full animation?)
- [ ] Audio cue for restoration (relief sound, magical effect, music sting?)
- [ ] Does recovery happen automatically on checkpoint touch or require player proximity?
- [ ] Does she show relief/happiness when restored (animation, sound)?
- [ ] Timing of recovery (instant, 1 second delay, after respawn?)

---

### Visual & Audio Design

- [ ] Teleport effect style (fade, particles, magical burst, dissolve?)
- [ ] Healing particle direction/flow (straight line, arc, spiral?)
- [ ] Healing particle color (matches her? matches player? changes by vitality?)
- [ ] Vitality stage visual markers (how drastic should degradation be?)
- [ ] Pain sounds during healing (volume, intensity, frequency)
- [ ] Footstep sound variations (3 sets per stage or more gradual change?)
- [ ] Float sound (constant hum or only when actively floating?)
- [ ] UI design for heal count (bar style, icon count, number, portrait indicator?)
- [ ] Visual warning when heals running low (color change, flashing, icon?)
- [ ] Particle effects for floating (trail behind her, aura, sparkles?)

---

### Technical Implementation

- [ ] Following AI system (navmesh pathfinding, simple position matching, spring physics?)
- [ ] Rubber band smoothing algorithm (lerp, spring damping, other?)
- [ ] Player speed detection for rubber band trigger (velocity threshold, movement type detection?)
- [ ] Collision/physics handling (character controller, simple positioning, hybrid?)
- [ ] Animation blending system (cross-fade, blend trees, layered animations?)
- [ ] Teleport implementation (instant position change, movement interpolation, fade in/out?)
- [ ] Vitality tracking (separate resource, tied to heal count, separate degradation system?)

---

## Movement Values & Tuning

_This section reserved for specific numerical values to be determined through playtesting and iteration._

### Following Behavior

- [ ] Follow distance behind player (units)
- [ ] Follow speed - Healthy state (units/second or % of player speed)
- [ ] Follow speed - Weak state (units/second or %)
- [ ] Follow speed - Weaker state (units/second or %)
- [ ] Follow speed - 0 heals state (minimum speed)
- [ ] Speed degradation curve shape (linear formula, exponential, custom curve)
- [ ] Rubber band catch-up speed multiplier
- [ ] Rubber band smoothing factor (lerp value, spring stiffness)
- [ ] Teleport threshold distance (units from player)
- [ ] Float descent speed (units/second, % of normal gravity)

### Healing System

- [ ] Heal HP amount restored (flat value or % of max HP)
- [ ] Heal animation duration (frames at 60fps, or milliseconds)
- [ ] Teleport-to-player duration (frames/ms)
- [ ] Healing particle effect duration (frames/ms)
- [ ] Player movement speed during heal (if allowed - % of normal)
- [ ] Cooldown between heals (if any - seconds/frames)
- [ ] Heal teleport offset from player (units, direction)

### Vitality System

- [ ] Total heals per checkpoint (absolute number)
- [ ] Heal count thresholds for animation states:
  - Healthy state: X to Y heals
  - Weak state: X to Y heals
  - Weaker state: X to 0 heals
- [ ] Movement speed percentages at specific heal counts (speed curve data points)
- [ ] Visual degradation severity per stage (appearance change intensity)

### Animation Timing

- [ ] Idle animation loop duration (seconds)
- [ ] Walk cycle duration (frames/seconds)
- [ ] Run cycle duration (if different from walk)
- [ ] Teleport out duration (frames/ms)
- [ ] Teleport in duration (frames/ms)
- [ ] Healing animation duration (frames/ms)
- [ ] State transition blend times (seconds for cross-fades)
- [ ] Floating animation cycle (if looping)

### Audio Timing

- [ ] Footstep sound frequency (steps per second at different speeds)
- [ ] Pain sound duration during healing (seconds)
- [ ] Breathing audio loop timing (breath rate at different vitality levels)
- [ ] Teleport sound duration (seconds)

### Tuning Philosophy

Values should support:
- **Emotional weight** - Her degradation must be visible and impactful
- **Non-interference** - Following never disrupts player platforming or combat
- **Character presence** - She feels like a person, not an object or system
- **Accessibility** - Healing always available (teleport from anywhere)
- **Consequence** - Every heal decision carries visible cost
- **Relief** - Checkpoint recovery provides emotional reset
- **Desperation** - Zero heals creates tension without instant failure
- **Smooth degradation** - Speed/appearance changes feel continuous, not stepped

---

## Cross-References

- [[PlayerMovement]] - Healing mechanics integration, movement during heal, dash i-frames
- [[Systems/GameFeel]] - Visual/audio feedback techniques, animation juice, particles
- [[Narrative/Her]] - (Future) Character identity, emotional arc, backstory, relationship
- [[Systems/HealthDamage]] - (Future) Player health system, damage mechanics, dual fail states
- [[Systems/CompanionAI]] - (Future) Technical implementation details if separated from this doc
- [[Bosses/BossOverview]] - Mercy-kill mechanics, thematic connection to suffering
- [[Overview]] - Core companion sacrifice mechanic, design pillars, emotional consequences

---

## Notes

### Design Philosophy

Her mechanics exist to create **emotional weight through mechanical consequences**:

- Every heal is a visible, costly choice
- Her suffering is immediate and visible (animation, movement, appearance)
- Zero heals creates desperation without instant failure
- Checkpoint recovery provides relief while highlighting accumulated cost
- Silent companion creates intimacy without dialogue dependency
- Following AI maintains presence without interference

**Key Principle**: She's not a helper - she's a sacrifice you must make to survive.

This inverts typical companion design:
- She doesn't help you fight (she's just there)
- She can't be hurt by enemies (only by your healing)
- She doesn't solve puzzles (she floats over obstacles)
- Her only mechanical function is healing, which hurts her
- **Success means using her less, not more**

This creates **empathy-driven mastery motivation** - you improve not to gain power, but to protect her from suffering.

---

### Reference Games

**Companion Following & AI**:
- **Donkey Kong Country** - Diddy Kong following behavior (normal movement reference)
- **Super Mario Galaxy** - Key/Luma rubber band following (fast movement reference)
- **ICO** - Yorda companion, protection feeling, emotional attachment, silent presence
- **The Last Guardian** - Trico companion AI, non-verbal communication, bond through mechanics

**Movement Mechanics**:
- **Super Smash Bros** - Peach floating mechanic (descent control, airborne movement)

**Resource & Healing Systems**:
- **Dark Souls** - Estus Flask discrete heal count, checkpoint refill, limited resource tension
- **Resident Evil** - Limited healing resources create tension and resource management

**Silent Companion Storytelling**:
- **ICO** - Yorda (minimal dialogue, emotion through animation and sound)
- **Journey** - Companion presence without words, emotional connection
- **The Last Guardian** - Trico (non-verbal communication, behavior-based personality)
- **Inside/Limbo** - Environmental storytelling without dialogue

**Emotional Mechanics**:
- **Shadow of the Colossus** - Agro (horse companion), emotional attachment to AI
- **The Last of Us** - Ellie companion, protection instinct
- **BioShock Infinite** - Elizabeth companion, emotional investment

---

### Implementation Phases

**Phase 1 - Basic Following**:
1. Simple Diddy Kong-style following at normal player speeds
2. Teleport when distance threshold exceeded
3. Basic walk/run animations
4. Maintains distance behind player
5. Basic collision/positioning

**Phase 2 - Heal Mechanic Core**:
1. Button press triggers heal call
2. Teleport to player on heal activation
3. Basic healing animation
4. Restore player HP (fixed amount)
5. UI showing heal count
6. Consume heal charge

**Phase 3 - Rubber Band System**:
1. Detect player advanced movement (dash, wall jump, slide-jump)
2. Switch to rubber band following mode during fast movement
3. Smooth position matching relative to player
4. Transition between normal following and rubber band
5. Tune smoothing and catch-up speed

**Phase 4 - Floating Mechanic**:
1. Implement Peach-style float descent
2. Apply during airborne/rubber band situations
3. Smooth vertical position transitions
4. Prevent awkward falling or terrain navigation
5. Visual/audio feedback for floating

**Phase 5 - Vitality System**:
1. Heal count resource tracking
2. Checkpoint restoration of heals
3. UI display for heal count
4. Zero heals state (can't heal, not game over)
5. Heal count persistence across level

**Phase 6 - Visual Degradation**:
1. Create 3 animation state groups (Healthy/Weak/Weaker)
2. Movement speed degradation formula implementation
3. Animation transitions based on heal count thresholds
4. Visual appearance changes per vitality stage
5. Extreme weakness state at 0 heals (barely moving)

**Phase 7 - Audio & Polish**:
1. Footstep sound variations by vitality
2. Teleport audio effects
3. Healing pain sounds (non-verbal, breathing, gasps)
4. Labored breathing when weak
5. Particle effects for teleport, healing, vitality states
6. Animation polish and blending
7. UI polish and clarity
8. Camera considerations (keep her in frame when needed?)

**Phase 8 - Playtesting & Tuning**:
1. Balance heal count per checkpoint
2. Tune movement speed degradation curve
3. Adjust animation state thresholds
4. Test healing accessibility in combat
5. Verify emotional impact (does degradation create guilt?)
6. Test edge cases (teleport bugs, animation glitches)
7. Polish timing and feel

---

### Success Criteria

The companion mechanics succeed when:

**Mechanical Success**:
- She never interferes with player platforming or combat
- Following feels natural (like a character, not an object/cursor)
- Healing is always accessible regardless of where she is
- Zero heals creates tension without feeling unfair
- Checkpoint recovery provides clear relief
- Floating/rubber banding feels smooth, not awkward
- Teleport system handles all edge cases gracefully

**Emotional Success**:
- Players genuinely want to minimize healing to protect her
- Visual degradation creates visible guilt and consequence
- Her suffering is immediate and impactful
- Players form emotional attachment through mechanics alone (not just narrative)
- Silent presence creates intimacy without dialogue
- Checkpoint recovery highlights what was lost (relief when she's healthy again)
- Zero heals creates desperation to reach checkpoint
- Players feel responsible for her state

**Design Success**:
- Mechanics create emotional experience, not just narrative
- Healing cost is felt mechanically (resource) and emotionally (her suffering)
- Success in combat means protecting her (inverted reward structure)
- Players improve to minimize her pain, not to gain power
- The companion sacrifice system feels unique and meaningful
- System supports core pillar: "Mastery Through Empathy"

---

### Key Differentiators

**Inverted Companion Design**:

Most companion systems in games exist to help the player - they fight alongside you, solve puzzles, provide resources, or assist in traversal. Her design inverts this:

- **No combat assistance** - She doesn't fight, doesn't distract enemies, provides no tactical advantage
- **No puzzle help** - She doesn't activate switches, open doors, or solve challenges
- **No resource gathering** - She doesn't find items or provide currency
- **Only function hurts her** - The one thing she does (heal you) causes her pain

This creates a unique emotional dynamic:
- **Using her more = worse outcome** (she suffers more)
- **Getting better at the game = protecting her** (need healing less)
- **Failure is visible** (her degraded state shows your mistakes)
- **Success is invisible** (staying healthy means she stays healthy)

**Empathy as Skill Motivation**:

Traditional games motivate mastery through:
- Power acquisition (better gear, stronger abilities)
- Score/ranking systems (leaderboards, grades)
- Unlocks and progression (new content, cosmetics)

Lament motivates mastery through **empathy**:
- Getting better = she suffers less
- Perfect play = she never has to heal you
- Skill expression = protecting someone you care about
- Failure = guilt (watching her limp because of your mistakes)

This creates a fundamentally different emotional relationship with difficulty and mastery. You're not improving for yourself - you're improving for her.

---

### Narrative Integration (Brief)

*Full narrative details in [[Narrative/Her]] - this section covers mechanical/narrative intersection only*

**Mechanical Support for Narrative**:
- Silent companion allows player projection (who is she to you?)
- Visual degradation tells story of accumulated sacrifice
- Her suffering is player's fault (creates guilt, responsibility)
- Checkpoint recovery could tie to narrative beats (why does she recover? What are checkpoints narratively?)
- Zero heals state could have narrative implications (what does it mean when she can't help anymore?)
- Her presence throughout journey creates bond through time spent together

**Narrative Support for Mechanics**:
- Why does healing hurt her? (narrative explanation)
- Why does she follow you? (motivation, relationship)
- Why can't enemies hurt her? (narrative justification for immunity)
- What are checkpoints narratively? (places of power, rest, safety?)
- What happens if you don't heal at all? (narrative acknowledgment of player choice?)

**Design Note**: Mechanics should work emotionally even without narrative context. The degradation, the guilt, the desire to protect her - these should emerge from the mechanics themselves. Narrative should enhance, not create, the emotional experience.

