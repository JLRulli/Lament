# Level Design

> **Status**: Design Exploration  
> **Last Updated**: 2025-12-17

---

## Overview

This document catalogs the mechanical building blocks for constructing levels in Lament. These interactables, obstacles, and encounter patterns support the game's dual focus on precision platforming (Celeste-inspired) and bullet-hell combat (Cuphead-inspired) within a linear world progression.

**Design Philosophy**:
- Mechanics support tight, responsive movement (see [[Mechanics/PlayerMovement]])
- Elements are reusable across multiple worlds with different aesthetics
- Complexity layers across game progression
- Clarity maintained even in dense combat scenarios
- Environmental elements reinforce dark fantasy/surrealist themes

**Cross-References**:
- [[Mechanics/PlayerMovement|Player Movement]] - Movement mechanics these elements are designed around
- [[Systems/GameFeel|Game Feel]] - Visual/audio polish for interactables and obstacles
- [[Worlds/WorldConcepts|World Concepts]] - Thematic contexts for these mechanics
- [[Bosses/BossOverview|Boss Design]] - Boss arenas utilize these elements

---

## Interactables

### Movement Platforms

#### Moving Platform

**Concept**: Platform that moves along a fixed path, requiring timing and prediction.

**Mechanics**:
- Moves on predetermined path (horizontal, vertical, circular, etc.)
- Player movement relative to platform (platform velocity transfers to player)
- Constant or variable speed options

**Design Considerations**:
- **Movement patterns**: Linear, circular, pendulum, figure-eight
- **Speed variations**: Constant speed vs acceleration/deceleration
- **Player control**: Full movement while on platform vs restricted
- **Chaining**: Multiple moving platforms in sequence
- **Combat integration**: Moving platforms during enemy encounters

**Platforming Applications**:
- Timing challenges (jump from/to moving platform)
- Extended traversal across gaps
- Vertical ascent/descent
- Rhythm-based platforming sequences

**Combat Applications**:
- Mobile cover during bullet-hell encounters
- Dynamic arena elements during boss fights
- Positioning challenges while dodging projectiles

**Reference**: **Mega Man series** - Classic moving platform challenges

**Design Questions**:
- [ ] Platform collision with player (solid, one-way, fall-through?)
- [ ] What happens at path endpoints? (Reverse, stop, loop, disappear?)
- [ ] Visual telegraph for movement direction/speed?
- [ ] Can enemies stand on moving platforms?
- [ ] Interaction with player dash/jump momentum?

---

#### Disappearing Platform

**Concept**: Platform that vanishes after player stands on it (timed) or in patterns.

**Mechanics**:
- **Timer-based**: Disappears X seconds after player contact
- **Pattern-based**: Appears/disappears on fixed cycle
- **Trigger-based**: Vanishes based on other level events

**Visual Telegraph**:
- Color change, flashing, transparency increase before disappearing
- Audio cue warning imminent disappearance
- Particle effects on vanish/reappear

**Design Considerations**:
- **Timing windows**: How long player has to react
- **Coyote time interaction**: Does coyote time work after platform disappears? (see [[Mechanics/PlayerMovement]])
- **Respawn timing**: How quickly platform returns
- **Player consequence**: Fall into pit, hazard, or lower area?

**Platforming Applications**:
- Pressure challenges (must move quickly)
- Memorization (pattern-based disappearing platforms)
- Risk/reward (optional harder path with disappearing platforms)

**Combat Integration**:
- Arena elements that change mid-fight
- Forces player movement during bullet-hell encounters
- Reduces safe spaces over time

**Reference**: **Celeste** - Disappearing platform timing and visual clarity

**Design Questions**:
- [ ] Timer duration before disappearance?
- [ ] Visual/audio clarity - is warning obvious enough?
- [ ] Can player trigger early disappearance (e.g., dash through platform)?
- [ ] Does platform disappear instantly or fade gradually?
- [ ] Respawn location: Same spot or different position?

---

#### Fall-Through Platform

**Concept**: One-way platforms player can drop through or jump up through.

**Mechanics**:
- Player lands on platform from above (solid from top)
- Player passes through platform from below (intangible from bottom)
- **Drop-through input**: Player can intentionally fall through platform (see [[Mechanics/PlayerMovement]] - Platform Interactions)

**Design Considerations**:
- **Input method**: Down + Jump, Hold Down, or separate button
- **Visual distinction**: Must be visually distinct from solid platforms
- **Enemy interaction**: Can enemies use fall-through platforms?
- **Combat flow**: Allows vertical repositioning during fights

**Platforming Applications**:
- Vertical level design (ascent and descent through same areas)
- Shortcut routes
- Multi-tiered arena designs
- Escape routes from danger

**Combat Applications**:
- Quick repositioning during bullet-hell encounters
- Evasive movement options
- Arena design with vertical layers

**Reference**: **Hollow Knight** - One-way platform clarity and usage

**Design Questions**:
- [ ] Visual design to distinguish from solid platforms?
- [ ] Can player drop through while running or must be stationary?
- [ ] Audio feedback when dropping through?
- [ ] Interaction with slide mechanic (slide off edge vs drop through)?

---

#### Floating Water Platforms

**Concept**: Platforms made of/supported by water, unique physics or aesthetic.

**Mechanics**:
- _[Physics to be determined - buoyant, unstable, moving?]_
- Potential: Platform bobs up/down gently
- Potential: Splashing effects, ripples on landing

**Visual Design**:
- Water surface acting as solid platform
- Magical/surrealist justification (dreamlike logic)
- Particle effects: Water droplets, ripples, mist

**Design Considerations**:
- **Unique properties**: Different from standard platforms how?
  - Slippery surface (like ice)?
  - Bouncy (like trampoline)?
  - Temporary stability (disappears after weight limit)?
- **Thematic placement**: Caves (underground water), Storm world, Spring world

**Surrealist Potential**:
- Water defying gravity (floating in air)
- Platforms of frozen water mid-splash
- Liquid surfaces acting solid

**Design Questions**:
- [ ] Unique mechanical property or purely aesthetic?
- [ ] Bobbing movement affects player control?
- [ ] Visual clarity - how to show it's solid?
- [ ] World-specific or appears across multiple worlds?

---

### Traversal Elements

#### Elevators

**Concept**: Vertical transport between level sections or floors.

**Mechanics**:
- **Activation**: Automatic on entry, button press, or lever pull
- **Movement**: Smooth vertical travel between floors
- **Control**: Player can move while elevator moves, or locked in place?

**Design Considerations**:
- **Travel time**: Fast travel vs slow (opportunity for ambush?)
- **Combat potential**: Trapped elevator fight (see Level Concepts - Cuphead-style)
- **Safety**: Can player fall off during travel?
- **Multi-floor**: Stop at intermediate floors or direct travel?

**Platforming Applications**:
- Gateway between major level sections
- Shortcut unlocks after progression
- Safe transport vs dangerous alternatives

**Combat Applications**:
- **Trapped encounters**: Waves of enemies during elevator travel (Cuphead-inspired)
- Mobile arena during ascent/descent
- Time pressure (must survive until destination)

**Design Questions**:
- [ ] Elevator size (tight space or generous arena)?
- [ ] Can player control direction/speed or automatic?
- [ ] Visual indication of travel progress?
- [ ] What happens if player tries to exit mid-travel?

---

#### Lock / Key Doors

**Concept**: Gates that require specific key/item to unlock, blocking progression.

**Mechanics**:
- **Astro door (Mega Man style)**: Thematic locked doorways
- Key collected elsewhere in level/world
- Door unlocks permanently when key used

**Visual Design**:
- Clear visual indication door is locked
- Key iconography matches door design
- Satisfying unlock animation/effect (see [[Systems/GameFeel]])

**Design Considerations**:
- **Key proximity**: How far from door is key located?
- **Backtracking**: Requires returning to door after finding key?
- **Linear progression**: Key always found before door in linear path?
- **Multiple keys**: Different colored keys for different door types?

**Progression Applications**:
- Gate progress until player explores area
- Optional areas behind locked doors (secrets, upgrades)
- Environmental puzzles (find key hidden in level)

**Reference**: **Mega Man series** - Astro door aesthetic and clear gate design

**Design Questions**:
- [ ] Key as inventory item or instant-unlock on contact?
- [ ] Visual feedback when attempting locked door without key?
- [ ] Can keys be used on multiple doors or one-time use?
- [ ] Thematic door designs per world?

---

#### Breakable Obstacles

**Concept**: Environmental objects that can be destroyed to clear path or reveal secrets.

**Mechanics**:
- Destroyed by player attacks (shooting, melee)
- Some require specific attack types or multiple hits
- Permanent destruction vs respawning obstacles

**Obstacle Types**:
- **Walls/barriers**: Block paths, must be destroyed to progress
- **Crates/containers**: May contain items, pickups, or enemies
- **Environmental hazards**: Destroying obstacle removes danger

**Design Considerations**:
- **Health/durability**: One-hit break or multiple hits required?
- **Visual telegraph**: Clear indication object is breakable vs solid
- **Destruction feedback**: Satisfying particle effects, audio, screen shake (see [[Systems/GameFeel]])
- **Combat integration**: Breaking obstacles during fights (risk/reward)

**Platforming Applications**:
- Clearing paths to progress
- Revealing hidden platforms or routes
- Environmental puzzle solving

**Combat Applications**:
- Destroyable cover (temporary safety)
- Clearing line of sight for shooting
- Risk of destruction exposing player to danger

**Design Questions**:
- [ ] All obstacles breakable or only specific types?
- [ ] Do obstacles block enemy projectiles/movement?
- [ ] Penalty for breaking obstacles (e.g., releases hazard)?
- [ ] Visual distinction: Breakable vs indestructible?

---

### Progression Points

#### Save Points

**Concept**: Safe havens where player saves progress and companion heals refill.

**Aesthetic Design**:
- **Stone bench with Shide** (zigzag paper streamers)
- **Paper rustling sound** - Ambient audio, peaceful atmosphere
- **Fire pit nearby** - Warm light source, safety beacon

**Mechanics**:
- **Save progress**: Checkpoint for respawn after death
- **Companion heal refill**: Restores companion's vitality, replenishes heal charges
- **Safe zone**: No enemy spawns or attacks near save point
- **Rest animation**: Player character sits on bench? (optional)

**Design Philosophy**:
- Save points as moments of respite in hostile world
- Safe harbors contrast with dangerous environments
- Thematic consistency: Benches/Shide appear across all worlds
- Audio/visual design creates calm, peaceful atmosphere

**Placement Strategy**:
- Before major challenges (difficult platforming, boss fights)
- After significant progress/level sections
- _[Density to be determined through playtesting]_

**Emotional Design**:
- Companions heals refilling represents reprieve from sacrifice
- Brief moment of safety before returning to danger
- Environmental contrast: Warmth and peace in dark world

**Reference**:
- **Hollow Knight** - Bench save points, consistent aesthetic, peaceful audio
- **Dark Souls** - Bonfire checkpoints, resource refill, safe zones

**Design Questions**:
- [ ] Save point density per level/world?
- [ ] Can player revisit save points to refill heals mid-level?
- [ ] Fast travel between save points or only checkpoints?
- [ ] Unique save point designs per world or universal aesthetic?
- [ ] Healing animation/duration when activating save point?
- [ ] Can player leave save point area and return to refill again?

---

## Obstacles & Hazards

### Environmental Hazards

#### Spikes

**Concept**: Static hazard that damages player on contact.

**Mechanics**:
- Instant damage on contact
- **No i-frame bypass**: Dash i-frames may or may not protect (to be determined)
- Permanent placement or retractable variants

**Visual Design**:
- Clear, obvious danger visual (sharp, menacing)
- Color coding: Red/dangerous tones
- Consistent aesthetic across worlds (stone spikes, ice spikes, metal spikes)

**Design Considerations**:
- **Damage amount**: Instant death or standard damage?
- **I-frame interaction**: Can player dash through safely? (see [[Mechanics/PlayerMovement]] - Dash)
- **Placement philosophy**: Punish blind jumps, create precision challenges
- **Retractable spikes**: Timing challenges (extend/retract on pattern)

**Platforming Applications**:
- Narrow safe paths between spike fields
- Precision landing zones
- Wall spikes preventing wall slide/climb (see [[Mechanics/PlayerMovement]])

**Combat Integration**:
- Arena hazards limiting safe movement space
- Environmental damage threat during bullet-hell dodging
- Risk/reward positioning (better shooting angle near spikes)

**Reference**:
- **Celeste** - Clear spike visual design and telegraphing
- **Hollow Knight** - Spike hazard placement and damage system

**Design Questions**:
- [ ] Damage amount (instant kill, percentage, or flat value)?
- [ ] Can player recover mid-fall if falling into spikes (double jump save)?
- [ ] Retractable spike timing and visual telegraph?
- [ ] Do spikes damage enemies or player-only?

---

#### Falling Stalagmites / Icicles

**Concept**: Ceiling-mounted hazards that fall when player passes beneath.

**Mechanics**:
- **Trigger**: Player proximity or timer-based
- **Warning phase**: Visual shake/crack before falling
- **Fall speed**: Fast enough to threaten, slow enough to react
- **Damage**: Contact damage during fall and brief time after landing

**Visual/Audio Telegraph**:
- **Pre-fall warning**: Shake, dust particles, cracking sound
- **Audio cue**: Distinct sound when triggered
- **Visual clarity**: Obvious shadow/indicator on ground below

**Design Considerations**:
- **Warning duration**: How much time player has to react
- **Reset timing**: Do stalagmites respawn? If so, how quickly?
- **Damage vs instant kill**: Flat damage or lethal?
- **Obstruction**: Does fallen stalagmite block path?

**Platforming Applications**:
- Timing challenges (run beneath during safe window)
- Environmental awareness tests
- Hazards on otherwise safe platforms

**Combat Integration**:
- Environmental hazard during enemy encounters
- Forces player movement/repositioning
- Risk: Focused on dodging projectiles, forget ceiling hazard

**World Placement**:
- Caves world (stalagmites)
- Winter world (icicles)
- Any world with ceiling hazards

**Reference**: **Cave Story** - Falling block hazards with clear telegraph

**Design Questions**:
- [ ] Warning duration (frames/milliseconds)?
- [ ] Respawn timing and location (same spot or random)?
- [ ] Can player destroy falling stalagmites with attacks?
- [ ] Multiple sequential triggers (gauntlet of falling hazards)?
- [ ] Does stalagmite damage enemies if it falls on them?

---

#### Drills

**Concept**: Moving mechanical hazards inspired by Mega Man X drill enemies.

**Mechanics**:
- **Movement patterns**: Linear, circular, patrol routes
- **Damage type**: Continuous contact damage
- **Obstruction**: Blocks player path, must be avoided or destroyed

**Design Considerations**:
- **Destructible**: Can player destroy drills or must avoid?
- **Speed**: Fast enough to threaten, predictable enough to learn
- **I-frame interaction**: Dash i-frames protect player? (see [[Mechanics/PlayerMovement]])
- **Environmental integration**: Drills on tracks, emerging from walls, etc.

**Visual/Audio Design**:
- Clear mechanical aesthetic (fits industrial/mining worlds)
- Loud drilling audio (warning and atmosphere)
- Sparks, dust particles when active (see [[Systems/GameFeel]])

**Platforming Applications**:
- Timing challenges (pass between drill patterns)
- Moving obstacles creating safe/unsafe windows
- Precision movement under pressure

**Combat Integration**:
- Environmental hazard during combat encounters
- Limits safe positioning areas
- Can drill damage enemies or player-only?

**World Placement**:
- Caves world (mining equipment)
- Industrial/mechanical themed areas
- Surrealist contexts (drills in impossible locations)

**Reference**: **Mega Man X series** - Drill enemies and hazard design

**Design Questions**:
- [ ] Movement speed and pattern variety?
- [ ] Destructible or invincible hazards?
- [ ] Drill activation: Always active or triggered by player proximity?
- [ ] Visual telegraph for movement direction/timing?
- [ ] Can player wall slide on surfaces near drills?

---

### Dynamic Hazards

#### Ice on Floor

**Concept**: Slippery surface reducing player control and friction.

**Mechanics**:
- **Reduced friction**: Player slides when stopping/changing direction
- **Acceleration**: Faster speed buildup, harder to stop
- **Direction change**: Delayed response, skidding

**Design Considerations**:
- **Slide mechanic interaction**: Does ice affect slide mechanic from [[Mechanics/PlayerMovement]]?
  - Slide on ice lasts longer (extended momentum)
  - Slide-jump boost amplified on ice?
- **Combat challenge**: Bullet-hell dodging with reduced control
- **Precision platforming**: Harder to land exactly on target
- **Surrealist placement**: Ice in non-Winter worlds (dreamlike logic)

**Platforming Applications**:
- Sliding momentum puzzles
- Precision challenges with reduced control
- Speed-based challenges (must maintain high speed)

**Combat Integration**:
- Arena surfaces with ice patches
- Forces different positioning strategies
- Risk: Slide into hazards or off platforms

**World Placement**:
- Winter world (primary)
- Caves world (frozen underground areas)
- Surrealist contexts (ice where it shouldn't be)

**Reference**: Classic platformer ice levels (Mario, Mega Man, etc.)

**Design Questions**:
- [ ] Friction reduction amount (subtle or extreme)?
- [ ] Affects all movement or only ground movement?
- [ ] Visual clarity: How to indicate icy surfaces?
- [ ] Does ice affect enemies or player-only?
- [ ] Can player break ice or permanent surface?
- [ ] Interaction with crouching/ducking?

---

## Environmental Hazards & Platforming Elements - Complete Reference

_This section provides comprehensive specifications for all environmental hazards and platforming gimmicks. Cross-referenced with [[Projects/LevelGenerationTool]] for implementation details._

### Damage-Dealing Hazards

#### Spikes (All Variations)

**Behavior**: Contact damage on touch  
**Variations**: 
- Standard spikes (stone, metal)
- Thorns (organic variant)
- Drills (mechanical variant)
- Jagged rocks (environmental variant)

**Damage**: [TBD - standard damage value]  
**I-Frame Interaction**: [TBD - can dash i-frames bypass?]  
**Respawn Behavior**: Player takes damage, brief i-frames, continues from position  
**Enemy Interaction**: [TBD - do spikes damage enemies or player-only?]

**Visual Design**:
- Clear, sharp, menacing appearance
- Red/danger color tones
- Variant-specific aesthetics (metal drills in industrial areas, thorns in organic areas)

**Level Generator Reference**: Tile ID 4, obstacle type "spike", variants "spike_thorn", "spike_drill"

**Design Intent**: Punish imprecise movement, create tension in tight spaces

---

#### Bottomless Pits/Gaps

**Behavior**: Falling off bottom of screen → damage + teleport to prior safe ledge  
**Damage**: [TBD - flat damage value]  
**Safe Ledge Logic**: Last ground/platform position player stood on before falling  
**Death Condition**: If damage kills player, no teleport (death state triggers)

**Visual Design**:
- Darkness/void below visible play area
- Optional: Fog effects obscuring depth
- Environmental variants (abyssal darkness, cloudy sky, lava glow from below)

**Level Generator Reference**: Tile ID 5, special handling for safe ledge tracking

**Design Intent**: Punish failed platforming without instant death, create risk in gap crossing

**Design Questions**:
- [ ] Damage amount? (e.g., 25% max health, flat 20 damage, etc.)
- [ ] Teleport animation/transition time?
- [ ] Can player be saved mid-fall with double jump or air dash?

---

#### Lava/Harmful Liquids

**Behavior**: Contact damage while player is in liquid  
**Damage Type**: [TBD - continuous per second or per tick?]  
**Damage Rate**: [TBD - damage per second value]

**Variations**:
- Lava (volcanic areas)
- Toxic water (sewers, swamps)
- Acid (industrial, alchemical areas)
- Corrupted liquid (No Man's Land)

**Visual Design**:
- Animated surface (bubbling lava, rippling toxic water)
- Particle effects (steam, toxic gas, corruption wisps)
- Danger color coding (orange/red for lava, green for toxic, purple for corrupted)

**Level Generator Reference**: Tile ID 20, obstacle type "liquid_hazard", property "damage_per_sec"

**Design Intent**: Area denial, time pressure in liquid sections

**Design Questions**:
- [ ] Can player swim or instant sink?
- [ ] Brief i-frames on initial contact or continuous damage immediately?
- [ ] Lingering damage effect after exiting liquid?

---

#### Crushing Mechanisms

**Behavior**: Timed crushing objects that deal heavy damage on contact  
**Damage**: [TBD - instant kill or heavy damage?]  
**Cycle Pattern**: [TBD - warning time → crush → reset time]

**Variations**:
- Vertical presses (ceiling crushers)
- Horizontal jaws (wall crushers)
- Compactors (room-scale crushing)

**Visual Design**:
- Warning animation before activation (shaking, grinding sound)
- Clear telegraph of danger zone
- Industrial/mechanical aesthetic

**Level Generator Reference**: Tile ID 21, obstacle type "crushing_mechanism", properties "damage", "cycle_time", "warning_time"

**Design Intent**: Timing-based hazard, predictable but deadly

**Design Questions**:
- [ ] Instant kill or heavy damage (e.g., 50 damage)?
- [ ] Warning duration before crush?
- [ ] Crush duration (how long player must avoid)?
- [ ] Can enemies be crushed?

---

#### Beam/Laser/Drill Hazards (Screen-Wide)

**Behavior**: Screen-wide linear hazard (horizontal or vertical)  
**Activation Pattern**: Warning animation → fills line with damage zone  
**Warning Time**: [TBD - seconds before activation]  
**Damage**: [TBD - damage on contact]  
**Active Duration**: [TBD - how long beam stays active]

**Variations**:
- **Horizontal beams**: Left-to-right or right-to-left sweep
- **Vertical beams**: Top-to-bottom or bottom-to-top sweep
- **Stationary beams**: Activates in place, no sweep
- **Moving beams**: Travels across screen at set speed

**Visual Design**:
- Warning indicators (floor/wall lights, alarm sounds)
- Charging animation before activation
- Bright, dangerous beam visual (laser, energy, drill line)

**Level Generator Reference**: Tile IDs 22 (horizontal), 23 (vertical), obstacle type "beam_hazard", properties "warning_time", "active_duration", "damage"

**Design Intent**: Large-scale hazard requiring repositioning, area denial

**Design Questions**:
- [ ] Warning duration (e.g., 1 second)?
- [ ] Can player dash through with i-frames?
- [ ] Beam sweep speed if moving variant?
- [ ] Audio/visual telegraph clarity?

---

### Platforming Gimmicks

#### Disappearing/Reappearing Platforms

**Behavior**: 
- Platform solid until player touches it
- After [TBD] seconds, platform collapses/disappears
- After [TBD] seconds collapsed, platform reappears

**Collapse Delay**: [TBD - time after player contact before collapse]  
**Respawn Delay**: [TBD - time before platform reappears]  
**Coyote Time Interaction**: [TBD - does coyote time work after platform disappears?]

**Visual Design**:
- Warning telegraph before collapse (flashing, color change, shaking)
- Disappearing animation (fade out, crumble)
- Reappearing animation (fade in, materialize)

**Level Generator Reference**: Obstacle type "disappearing_platform", properties "collapse_delay", "respawn_delay"

**Design Intent**: Timing pressure, forces player movement, can't wait on platform

**Design Questions**:
- [ ] Collapse delay (e.g., 1 second after contact)?
- [ ] Respawn delay (e.g., 2-3 seconds)?
- [ ] Visual warning duration before collapse?
- [ ] Can player trigger collapse without standing on it (e.g., dash through)?

---

#### Conveyor Belts/Moving Surfaces

**Behavior**: Ground surface that alters player ground speed  
**Speed Modifier**: [TBD - multiplier, e.g., 1.5x normal speed]  
**Direction**: Left or right (or toward/away from camera in 2.5D sections)

**Mechanics**:
- Modifies ground movement speed while player on surface
- Affects jump distance (momentum carries)
- Can move toward hazards or off ledges (requires countermovement)

**Visual Design**:
- Animated texture (scrolling arrows, moving treads)
- Direction indicators (arrows, tread direction)
- Industrial aesthetic (factory belts, mechanical surfaces)

**Level Generator Reference**: Tile ID 31, obstacle type "conveyor_belt", properties "speed_mult", "direction"

**Design Intent**: Precision platforming with momentum management, combine with other hazards

**Design Questions**:
- [ ] Speed multiplier value (e.g., 1.5x = 50% faster)?
- [ ] Does it affect air control after jumping off?
- [ ] Can enemies be affected by conveyor belts?
- [ ] Interaction with slide mechanic from [[Mechanics/PlayerMovement]]?

---

#### Ice Physics/Slippery Surfaces

**Behavior**: Reduces friction, making movement slippery  
**Friction Reduction**: [TBD - multiplier, e.g., 0.3 = 70% less friction]  
**Affected Actions**: Ground movement, stopping, direction changes

**Mechanics**:
- Player slides when stopping (momentum continues)
- Direction changes delayed/gradual
- Jumps may have altered control
- Slide mechanic potentially extended (see [[Mechanics/PlayerMovement]])

**Visual Design**:
- Icy, wet, or oily surface appearance
- Reflective/shiny material
- Particle effects (frost, water droplets, oil sheen)

**Level Generator Reference**: Tile ID 32, obstacle type "ice_floor", property "friction_mult"

**Design Intent**: Reduced control challenge, precise positioning harder

**Design Questions**:
- [ ] Friction reduction percentage?
- [ ] Does it affect air control?
- [ ] Interaction with slide mechanic (extends slide duration)?
- [ ] Affects enemies or player-only?

---

#### Moving/Timed Platforms

**Behavior**: Platforms that move along a set path  
**Path Type**: Linear (horizontal/vertical), circular, waypoint-based  
**Speed**: [TBD - units per second]  
**Loop**: Continuous loop or back-and-forth

**Mechanics**:
- Player inherits platform velocity (relative motion)
- Requires timing to jump on/off
- Can combine with other hazards (moving platform over spikes)

**Variations**:
- **Horizontal movers**: Left-right motion
- **Vertical movers**: Up-down motion
- **Circular movers**: Rotating around point
- **Waypoint movers**: Complex paths

**Visual Design**:
- Platform clearly distinct from static platforms
- Optional: Direction indicators, movement trail effects

**Level Generator Reference**: Tile ID 33, obstacle type "moving_platform", properties "path", "speed", "loop"

**Design Intent**: Timing-based platforming, momentum management

**Design Questions**:
- [ ] Movement speed (pixels per second)?
- [ ] Can platforms crush player against walls?
- [ ] Fall-through (one-way) or solid?
- [ ] Do enemies use moving platforms?

---

#### Destructible Blocks

**Behavior**: Objects that can be destroyed by player attacks  
**Health**: [TBD - number of hits to destroy]  
**Attack Types**: Shooting, melee, or both?  
**Respawn**: [TBD - permanent destruction or respawn after time?]

**Mechanics**:
- Block takes damage from player attacks
- Breaks after sufficient damage
- May block paths, hide secrets, or protect hazards
- Can be used tactically (create paths, expose enemies)

**Visual Design**:
- Cracked/damaged appearance after taking hits
- Breaking animation with debris
- Distinct from indestructible walls (cracks, weaker material)

**Level Generator Reference**: Tile ID 34, obstacle type "destructible_block", properties "health", "drops", "respawn_time"

**Design Intent**: Player agency, path creation, optional challenges

**Design Questions**:
- [ ] How many hits to break? (e.g., 3 hits?)
- [ ] Do they drop anything (resources, pickups)?
- [ ] Permanent destruction or respawn after time?
- [ ] Required for progression or optional paths only?
- [ ] Can enemies destroy blocks?

---

### Hazard & Gimmick Combinations

**Effective Combinations**:
- **Disappearing Platforms + Spikes**: Timed platforming with punishment
- **Conveyor Belts + Pits**: Momentum management to avoid falling
- **Ice Floor + Enemies**: Reduced control during combat
- **Moving Platforms + Beam Hazards**: Multi-layered timing challenge
- **Crushing Mechanisms + Narrow Spaces**: Precision timing under pressure

**Design Philosophy**:
- Introduce hazards individually first
- Combine hazards after player understands each individually
- Limit combinations to 2-3 simultaneous hazards (avoid overwhelming)
- Use combinations to create difficulty spikes

---

### Implementation Checklist

**For Each Hazard/Gimmick**:
- [ ] Finalize damage values
- [ ] Define timing parameters (delays, durations, cycles)
- [ ] Create visual telegraphs and feedback
- [ ] Test with player movement mechanics (see [[Mechanics/PlayerMovement]])
- [ ] Define enemy interaction rules
- [ ] Add to Level Generator obstacle catalog (see [[Projects/LevelGenerationTool]])
- [ ] Create UE5 assets and blueprints
- [ ] Balance difficulty placement (which hazards at which difficulty levels)

---

## Level Concepts & Encounter Designs

_These are specific level/encounter ideas that combine interactables and obstacles into cohesive challenges._

### Platforming Challenges

#### Lined-Up Pillars

**Concept**: Series of pillars player must jump between, fog obscures pits below.

**Mechanics**:
- Precision jumping between pillar tops
- **Fog visual**: Hides pit depths, creates tension
- No visual confirmation of safe landing below
- Tests player nerve and jump timing

**Design Elements**:
- Pillar spacing varies (short/long jumps)
- Some pillars may be moving platforms
- Potential: Disappearing platforms mixed in
- Fog density creates visibility challenge

**Emotional Design**:
- Leap of faith into obscured space
- Trust in level design vs fear of hidden hazards
- Tension through limited information

**World Placement**:
- Pillars/Ruins world (primary)
- Storm world (fog from storm clouds)
- No Man's Land (void spaces)

**Reference**: Atmospheric jumping challenges in dark/obscured spaces

**Design Questions**:
- [ ] Fog as pure visual or also affects gameplay (hidden hazards)?
- [ ] Audio cues for landing safely (footstep sounds)?
- [ ] Are pits below instant death or damage + respawn?
- [ ] Pillar stability: All solid or some crumble/disappear?

---

#### Death Wall Chase

**Concept**: Wall constantly pushes from left side of screen, forcing rightward movement.

**Mechanics**:
- **Auto-scroll**: Screen scrolls right at constant/increasing speed
- **Instant death**: Touching left wall kills player
- **Platforming under pressure**: Must navigate obstacles while maintaining speed
- **No backtracking**: Forward momentum only

**Design Elements**:
- Obstacles: Gaps, spikes, enemies, moving platforms
- Requires mastery of movement (slide-jump, dash, wall jump)
- Potential: Speed increases over time (escalating pressure)

**Platforming Applications**:
- Tests player movement skill under time pressure
- Requires quick decision making
- Rewards mastery of advanced movement (see [[Mechanics/PlayerMovement]])

**Emotional Design**:
- Panic and pressure
- Desperation and chase
- Triumph through skilled execution

**World Placement**:
- Storm world (wind pushing player)
- No Man's Land (corruption spreading)
- Any world for set-piece chase sequence

**Reference**: Auto-scrolling chase sequences in platformers

**Design Questions**:
- [ ] Death wall speed (constant or accelerating)?
- [ ] Can player push ahead and gain breathing room?
- [ ] Checkpoints during chase or single continuous run?
- [ ] Enemy encounters during chase or pure platforming?
- [ ] Visual design of death wall (storm, darkness, corruption)?

---

### Combat Encounters

#### Trapped Arena (Cuphead-Style)

**Concept**: Smaller enclosed space, waves of enemies, no escape until cleared.

**Mechanics**:
- **Arena lock**: Player cannot leave until all enemies defeated
- **Wave-based**: Enemies spawn in patterns/groups
- **Pure combat focus**: Minimal platforming, maximum bullet-hell challenge
- **Difficulty spike**: Tests player combat skill and damage minimization

**Design Elements**:
- Arena size: Small enough to pressure, large enough to dodge
- Platform layout: Multiple levels, fall-through platforms for repositioning
- Hazards: Environmental dangers adding pressure
- Enemy composition: Variety of bullet patterns and behaviors

**Combat Challenge**:
- Tests 8-way shooting precision
- Bullet-hell dodging with movement mechanics (dash, slide, jump)
- Companion healing resource management (minimize damage)
- Skill reward: No-damage clears protect companion

**Emotional Design**:
- High-pressure combat gauntlet
- Every hit taken costs companion vitality
- Mastery-driven: Improve to protect companion

**Placement Strategy**:
- Mid-level combat challenges
- Optional arenas (rewards for clearing)
- Escalating difficulty across game progression

**Reference**: **Cuphead** - Elevator wave encounters, tight combat spaces

**Design Questions**:
- [ ] Arena size variation (tight vs spacious)?
- [ ] Wave count and enemy density?
- [ ] Checkpoints between waves or restart from beginning?
- [ ] Environmental hazards present or pure combat?
- [ ] Rewards for clearing (health refill, upgrades, shortcuts)?
- [ ] Can player heal during encounter (risky healing windows)?

---

## Design Patterns

### Difficulty Progression

**Introduction Phase**:
- Introduce mechanics individually
- Safe environments to learn
- Clear visual/audio feedback
- Forgiving failure states

**Combination Phase**:
- Layer multiple mechanics together
- Increase challenge complexity
- Test player mastery of basics
- Introduce variations on known mechanics

**Mastery Phase**:
- Expect full mechanical understanding
- High-pressure scenarios
- Complex combinations
- Skill expression opportunities

**Design Questions**:
- [ ] Tutorial approach (explicit or environmental teaching)?
- [ ] Difficulty curve pacing across worlds?
- [ ] Optional high-difficulty challenges vs mandatory?

---

### Movement Integration

**Slide-Jump Platforms**:
- Long runways encourage slide mechanic
- Gaps requiring slide-jump boost to clear
- Rewards movement combo mastery

**Wall-Jump Chains**:
- Vertical shafts with parallel walls
- Alternating wall jumps to ascend
- Tests timing and direction control

**Dash Timing Challenges**:
- Disappearing platforms + dash cooldown management
- Hazards requiring i-frame dash-through
- Precision dash positioning

**Air Control Precision**:
- Narrow landing zones at jump apex
- Threading tight gaps mid-jump
- Apex control tests (see [[Mechanics/PlayerMovement]])

**Design Philosophy**:
- Level design teaches and tests movement mechanics
- Interactables placed to encourage specific techniques
- Mastery rewarded with faster/safer routes

---

### Combat Integration

**Arena Design for 8-Way Shooting**:
- Multiple elevation levels (platforms)
- Enemies positioned at various angles
- Cover/obstacles for tactical positioning

**Bullet-Hell Pattern Support**:
- Open spaces for dodging dense projectiles
- Fall-through platforms for quick vertical repositioning
- Dash cooldown considerations in arena size

**Healing Opportunity Windows**:
- Brief safe moments during wave encounters
- Arena design creates temporary cover
- Risk/reward: Heal now or push through?

**Environmental Hazard Integration**:
- Hazards limit safe space during combat
- Forces player into dangerous positions
- Increases pressure without more enemies

---

## Design Questions & Future Considerations

### Checkpoint & Save Point Density

- [ ] Checkpoints between major challenges or at world sections?
- [ ] Save point frequency (how often can player refill companion heals)?
- [ ] Can player backtrack to save points or one-way progression?

### Platforming vs Combat Balance

- [ ] Ratio of platforming to combat per world/level?
- [ ] Pure platforming sections vs pure combat vs mixed?
- [ ] Does ratio shift across game progression?

### Mechanic Introduction

- [ ] Tutorial philosophy: Explicit teaching or environmental learning?
- [ ] How much time between introducing mechanic and testing mastery?
- [ ] Optional tutorials for advanced techniques?

### Difficulty Scaling

- [ ] Difficulty curve across worlds (linear increase, spikes, plateaus)?
- [ ] Optional hard challenges vs mandatory progression?
- [ ] Accessibility options (assist mode, difficulty settings)?

### Interactable Combinations

- [ ] Which interactables work well together?
- [ ] Combinations that create unfair/frustrating challenges?
- [ ] Maximum complexity level before overwhelming player?

---

## Cross-References

- [[Mechanics/PlayerMovement|Player Movement]] - Movement mechanics these levels are designed around
- [[Systems/GameFeel|Game Feel]] - Polish and feedback for interactables/obstacles
- [[Worlds/WorldConcepts|World Concepts]] - Thematic world designs using these mechanics
- [[Bosses/BossOverview|Boss Design]] - Boss arenas incorporate level design elements
- [[Overview|Game Overview]] - Core design pillars and player experience goals

---

## Notes

### Design Philosophy Summary

Level design serves game pillars:

1. **Emotional Consequences**: Difficulty creates damage risk → forces healing → companion suffers
2. **Mastery Through Empathy**: Skillful play navigates challenges without damage → protects companion
3. **Surreal Fantasy**: Interactables/obstacles exist in dreamlike, Lynchian contexts
4. **Tight Combat Flow**: Level layouts support responsive platforming and bullet-hell combat

### Implementation Priority

**Phase 1 - Core Elements**:
- Basic platforms (moving, disappearing, fall-through)
- Essential hazards (spikes, pits)
- Save points

**Phase 2 - Complexity**:
- Advanced interactables (elevators, locked doors, breakable obstacles)
- Dynamic hazards (falling objects, drills, ice)
- Combat arenas

**Phase 3 - Set Pieces**:
- Unique level concepts (death wall chase, pillar jumping)
- World-specific mechanics
- Polish and juice

### Reference Games Summary

- **Mega Man series** - Moving platforms, Astro door gates, drill hazards, industrial level design
- **Celeste** - Disappearing platforms, spike design, precision platforming challenges
- **Hollow Knight** - Fall-through platforms, bench save points, hazard placement
- **Dark Souls** - Bonfire checkpoint system, safe haven design
- **Cave Story** - Falling hazard telegraph and timing
- **Mega Man X series** - Drill enemy/hazard design
- **Cuphead** - Trapped arena wave encounters, tight combat spaces

### Success Criteria

- Interactables feel responsive and predictable
- Hazards are clearly telegraphed and fair
- Level concepts teach and test mechanics effectively
- Difficulty progression feels natural and rewarding
- Combat and platforming sections both feel satisfying
- Elements support emotional journey and companion protection motivation
