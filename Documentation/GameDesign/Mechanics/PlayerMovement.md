# Player Movement

> **Status**: Design Exploration  
> **Last Updated**: 2025-12-16

---

## Overview

Player movement design for Lament prioritizes responsive, Celeste-inspired controls that support both precision platforming and bullet-hell combat scenarios. Movement should feel quick and fluid while maintaining control clarity in dense combat situations.

**Design Goals**:
- Quick, responsive movement (Celeste reference)
- Support for bullet-hell projectile density (Cuphead reference)
- Wall interaction mechanics for vertical exploration
- Movement options that complement magic combat
- Balance between speed and precise control

**Design Philosophy**:
- Forgiveness through coyote time and jump buffering
- Skill expression through movement combos (slide-jump, wall chains)
- Committed actions (dash has no mid-animation control)
- Multiple options for navigating vertical spaces

**Cross-References**:
- [[Systems/GameFeel|Game Feel]] - Animation techniques, particles, camera feel
- [[Mechanics/Combat|Combat]] - (Future) Shooting mechanics, spell wheel details
- [[Systems/CompanionSystem|Companion System]] - (Future) Healing interaction
- [[Systems/UI|UI System]] - (Future) Health display, heal count UI

---

## Core Movement

### Walking & Running

**Concept**: Movement speed determines animation state - no separate run button required.

- **Walk animation** plays at lower speeds
- **Run animation** automatically triggers when speed threshold is reached
- Reduces button complexity, keeps controls focused on platforming and combat

**Design Questions**:
- [ ] Walk speed value
- [ ] Run speed threshold
- [ ] Acceleration curve (instant vs gradual speed-up)
- [ ] Deceleration/friction when stopping

---

### Jumping

#### Double Jump

Player can jump a second time while airborne.

- Second jump can be used at any point during first jump
- _[Double jump height relative to first jump - TBD]_
- _[Visual/audio distinction from first jump - see GameFeel doc]_

**Design Questions**:
- [ ] Double jump height (same as first, lower, higher?)
- [ ] Can double jump reset/refresh air momentum?
- [ ] Double jump available after other air actions? (wall jump, dash, etc.)

---

#### Coyote Time

Grace period after leaving platform edge where jump input still registers.

- Allows player to jump slightly after walking off ledge
- Improves feel and forgiveness for platforming
- Invisible to player but significantly improves game feel

**Design Rationale**: Players often input jump slightly too late when walking off edges. Coyote time forgives this timing without making the game feel less responsive.

**Reference**: Celeste uses ~0.1 seconds of coyote time to great effect.

**Design Questions**:
- [ ] Coyote time duration (frames/milliseconds)
- [ ] Visual indicator for players or completely invisible?
- [ ] Applies to all platform types or only certain surfaces?

---

#### Jump Buffering

Jump input registered slightly before landing still executes on touchdown.

- Press jump just before hitting ground → character jumps immediately on landing
- Reduces input precision requirements
- Maintains sense of responsiveness

**Design Rationale**: Without buffering, players must time jump input precisely on landing frame. Buffering allows slightly early inputs, making movement feel more responsive.

**Reference**: Celeste uses jump buffering extensively for smooth platforming flow.

**Design Questions**:
- [ ] Buffer window duration (frames/milliseconds)
- [ ] Applies to landing from any state? (fall, double jump, dash, wall jump, etc.)
- [ ] Visual/audio feedback when buffered jump executes?

---

#### Air Control

Horizontal movement control while airborne.

**Enhanced Control at Apex**:
- Player has **better air control at the peak of jump arc**
- Allows for more precise mid-air adjustments at the highest point
- Creates skill opportunity for threading tight gaps

**Design Rationale**: 
- Full air control can make platforming too easy
- No air control feels unresponsive and frustrating
- Variable air control (more at apex) rewards skilled timing
- Apex control allows for "changing your mind" mid-jump

**Reference**: Celeste provides strong air control throughout jump with slight apex boost.

**Design Questions**:
- [ ] Base horizontal air control percentage (vs ground control)
- [ ] Apex control multiplier amount
- [ ] Apex window duration (how long is "apex"?)
- [ ] Air control after double jump (same, more, less?)
- [ ] Air control during/after dash
- [ ] Can change direction in air or only adjust speed?

---

### Crouching & Ducking

**Duck**: Reduces player hitbox height.

- Used to avoid overhead attacks and projectiles
- Required for navigating low passages
- Shares button with slide (context-sensitive)

**Button Behavior**:
- Press crouch button **while stationary** → duck
- Press crouch button **while moving** → slide (see Advanced Movement)

**Design Questions**:
- [ ] Duck hitbox height reduction
- [ ] Movement speed while ducking (penalty amount or prevented entirely)
- [ ] Can attack while ducking?
- [ ] Transition time between standing and ducking

---

## Advanced Movement

### Slide

**Concept**: Slide maintains momentum while giving player duck-height hitbox.

**Mechanics**:
- **Same button as crouch/duck** (context-sensitive)
  - Press while moving → slide
  - Press while stationary → duck
- **Slide physics**: Gradually loses speed over time until player is crouched
- **Hitbox**: Same height as duck (can go under same obstacles)
- **Ground only** - cannot slide in air

**Design Rationale**: 
- Combines mobility with reduced hitbox
- Creates risk/reward: maintain speed vs lose it while low
- Natural transition from slide to duck as momentum bleeds off

**Design Questions**:
- [ ] Initial slide speed (maintains run speed, boosts, or reduces?)
- [ ] Friction/deceleration curve
- [ ] Slide duration before full stop
- [ ] Can extend slide by maintaining button hold?
- [ ] Can cancel slide early by releasing button?
- [ ] Can attack while sliding?
- [ ] Slide-specific particle effects (dust trail)

---

#### Slide Jump

Jump out of slide gives **extra burst of speed and distance**.

- **Celeste-style momentum boost**
- Rewards skilled movement combo
- Creates fast traversal option when chained with other movement

**Design Rationale**: 
- Rewards players who understand slide mechanics
- Provides skill expression through movement combos
- Maintains high-speed flow when mastered
- Risk/reward: commit to slide to gain speed boost

**Reference**: Celeste's crouch-dash mechanics provide similar speed boost on exit.

**Design Questions**:
- [ ] Slide jump speed boost amount
- [ ] Slide jump distance boost
- [ ] Slide jump height (same as normal jump, higher, lower?)
- [ ] Minimum slide speed/duration needed for boost?
- [ ] Does boost diminish if slide has lost too much momentum?
- [ ] Air control after slide jump (same as normal jump?)

---

### Dash

**Concept**: Quick burst movement with invincibility frames (i-frames).

**Mechanics**:
- **8-way directional dash** (up, down, left, right, 4 diagonals)
- **No control during dash** - only before and after
  - Commit to direction when initiating
  - No mid-dash steering or canceling
  - Control returns fully after dash animation completes
- **I-frames during dash** (brief invincibility)
- **Cooldown-based** (not charge system)

**Design Rationale**: 
- Provides defensive option in bullet-hell scenarios
- Limited control creates commitment and risk
- I-frames allow threading through bullet patterns
- Cooldown prevents spam, rewards thoughtful use

**Reference**: Celeste dash mechanics - committed direction, used for both offense and defense.

**Design Questions**:
- [ ] Dash distance per direction (uniform or directional variation?)
- [ ] Dash duration (frames/milliseconds)
- [ ] Cooldown duration
- [ ] Visual cooldown indicator (UI or character-based?)
- [ ] Can queue dash input during cooldown?
- [ ] I-frame duration (entire dash or partial?)
- [ ] Can dash in air or ground only? Both?
- [ ] Can attack during/immediately after dash?
- [ ] Dash momentum carry-over to other actions

---

### Wall Interactions

#### Wall Slide

Reduces fall speed when in contact with wall.

**Trigger**: Hold direction toward wall while airborne

**Mechanics**:
- **Automatic** when holding direction into wall and falling
- **Indefinite duration** - can wall slide as long as you hold toward wall
- **Reduced fall speed** (slower than normal fall)

**Design Rationale**: 
- Provides vertical exploration options
- Rewards wall proximity and positioning
- No time limit allows for observation and planning
- Hold requirement gives player control (can release to drop)

**Design Questions**:
- [ ] Fall speed reduction amount (gentle slow or very slow?)
- [ ] Must hold toward wall or automatic on contact?
- [ ] Visual/audio feedback (sparks, scraping sound?)
- [ ] Can attack while wall sliding?
- [ ] Stamina/grip limit or truly indefinite?

---

#### Wall Jump

Jump off wall while wall sliding.

**Mechanics**:
- **Slight forced direction** up and away from wall
- **Forced speed component** (like Celeste)
- **Maintains some limited control** during wall jump
- **Full control returns when jump completes**
- Can chain wall jumps (climb vertical shaft by alternating walls)

**Design Rationale**: 
- Forced away-from-wall component prevents "sticking" to wall
- Limited control maintains intended arc while allowing minor adjustments
- Enables climbing challenges and vertical exploration
- Skill expression through wall jump chains

**Reference**: Celeste wall jump - strong away-from-wall force, limited control, can chain effectively.

**Design Questions**:
- [ ] Wall jump height (vs normal jump)
- [ ] Away-from-wall force strength
- [ ] Limited control amount (percentage vs full control)
- [ ] When does full control return? (time-based, apex, landing?)
- [ ] Can double jump after wall jump?
- [ ] Can dash during/after wall jump?
- [ ] Can wall jump on same wall repeatedly or must alternate?
- [ ] Wall jump cooldown per wall surface?

---

### Platform Interactions

**Fall-Through Platforms**: Player can drop through certain platforms.

- Allows descent through one-way platforms
- _[Input method to be determined]_

**Design Questions**:
- [ ] Input method (down+jump, hold down, separate button?)
- [ ] Must be stationary or can fall-through while running?
- [ ] Visual indicator for fall-through platforms?
- [ ] Can enemies use fall-through platforms?

---

## Combat Integration

**Note**: See [[Mechanics/Combat|Combat System]] (future doc) for complete combat mechanics and spell details.

### Shooting (Brief Overview)

**8-Way Directional Shooting**: Up, down, left, right, and 4 diagonal directions.

- Full directional control for aiming
- **Shooting cooldown**: Varies per attack type (determined through playtesting)
- Can shoot while: moving, jumping, _[other actions TBD]_

**Design Questions**:
- [ ] Aim system (stick direction, button combinations, auto-aim assist?)
- [ ] Can shoot during: dashing? sliding? wall sliding? healing?
- [ ] Does shooting affect movement speed?
- [ ] Shooting animation priority (full-body or upper-body only?)

---

### Spell Wheel (Brief Overview)

**Concept**: Real-time spell selection system with quick-swap option.

**Mechanics**:
- **No time slow** - spell switching happens in real-time
- **Quick swap**: Tap button to swap between 2 active spells
- **Full wheel**: Hold button to see all 8 spell slots
  - Can replace one of the 2 active spells from the 8 available
- **8 total spell slots** in the wheel
- **Can switch spells whenever** - mid-combat allowed

**Design Rationale**: 
- Real-time switching maintains combat flow and tension
- Quick-swap for fast combat decisions (2 active spells)
- Full wheel for strategic loadout changes (choose from 8)
- Similar to Bioshock Infinite's vigor wheel system

**Reference**: Bioshock Infinite - tap to cycle between favorites, hold to see full wheel.

See [[Mechanics/Combat|Combat System]] for detailed spell mechanics and wheel UI.

**Design Questions**:
- [ ] Quick-swap input (single button tap cycles which direction?)
- [ ] Full wheel input (hold duration to open?)
- [ ] Can move while wheel is open?
- [ ] Wheel visual design and spell slot arrangement

---

### Healing (Brief Overview)

**Concept**: Call upon companion to heal player.

**Mechanics**:
- **Button press** to initiate heal (not hold)
- **Can move during heal** (will test feel during implementation)
- **Cannot cancel heal** - animation must complete
- **Fast animation** - quick enough to use in combat

**Design Rationale**: 
- Button press allows quick heal activation in frantic combat
- Movement during heal maintains player agency (tentative, pending testing)
- No cancel prevents heal spam abuse
- Fast animation keeps combat flowing

See [[Systems/CompanionSystem|Companion System]] for detailed healing mechanics, companion AI, and heal resource system.

**Design Questions**:
- [ ] Heal animation duration (frames/milliseconds)
- [ ] Movement speed during heal (full, reduced, or locked?)
- [ ] Can perform other actions during heal? (shoot, jump, dash?)
- [ ] Visual/audio feedback for heal activation and completion
- [ ] Heal amount (fixed or variable based on companion state?)

---

## Damage & Recovery

### Taking Damage

**Temporary I-Frames**: Brief invincibility after taking damage.

- Prevents multiple hits from same attack or attack wave
- Critical for bullet-hell balance (prevents instant death from overlapping projectiles)
- _[Duration to be tuned based on bullet density testing]_
- _[Visual feedback during i-frames - see GameFeel doc]_

**Knockback**: _[Player pushed back when hit - details TBD]_

**Design Questions**:
- [ ] I-frame duration (frames/milliseconds)
- [ ] Longer i-frames for bullet-hell balance vs shorter for difficulty?
- [ ] Knockback distance and direction
- [ ] Player control during knockback
- [ ] Visual i-frame indicator (flashing, transparency, outline?)
- [ ] I-frames stack with dash i-frames or separate systems?

---

### Fall System

**Pit/Void Falls**: Falling into pits or off-level triggers respawn.

**Mechanics**:
- Fall into pit/void → lose health, respawn at edge where you fell
- **No height-based fall damage** - only void falls cause damage
- Can fall from any height without damage (unless it's into a void)

**Design Rationale**: 
- Punishes careless platforming (health penalty)
- No height damage encourages exploration and risk-taking
- Respawn at fall point maintains flow (no backtracking)

**Design Questions**:
- [ ] Health penalty amount (flat amount or percentage?)
- [ ] Respawn location (exact edge, last safe platform, checkpoint?)
- [ ] Respawn invincibility duration
- [ ] Fall animation and respawn transition (instant, fade, other?)
- [ ] Does fall death count toward death counter/statistics?

---

## Animation States

Required animation states for player character:

1. **Walk / Run** - Automatic transition based on speed
2. **Idle** - Standing still
3. **Jump / Fall** - Airborne states
4. **Shooting** - Attack animations _[see [[Mechanics/Combat|Combat]] for details]_
5. **Switch Ability** - Spell wheel interaction
6. **Wall Slide / Jump** - Wall interaction animations
7. **Hit** - Taking damage reaction
8. **Death** - Player death animation
9. **Heal** - Calling upon companion
10. **Mercy Kill Boss** - Boss execution animation _[see [[Bosses/BossOverview|Boss Design]]]_

**Notes**:
- Animation blending and priorities to be determined during implementation
- Potential need for upper/lower body animation separation (e.g., shoot while running)
- Transition animations between major states may be needed
- See [[Systems/GameFeel|Game Feel]] for animation techniques (squash/stretch, anticipation, etc.)

---

## Movement Values & Tuning

_This section reserved for specific numerical values to be determined through playtesting and iteration._

**Core Movement**:
- [ ] Walk speed
- [ ] Run speed threshold
- [ ] Acceleration and deceleration curves
- [ ] Friction values

**Jumping**:
- [ ] Jump height (first jump)
- [ ] Jump duration
- [ ] Double jump height
- [ ] Gravity strength
- [ ] Jump arc shape

**Air Control**:
- [ ] Base air control percentage (vs ground control)
- [ ] Apex control multiplier
- [ ] Apex window duration

**Forgiveness Systems**:
- [ ] Coyote time duration
- [ ] Jump buffer window duration

**Slide**:
- [ ] Initial slide speed
- [ ] Slide friction/deceleration curve
- [ ] Slide duration to full stop
- [ ] Slide jump speed boost amount
- [ ] Slide jump distance boost amount

**Dash**:
- [ ] Dash distance (per direction if varies)
- [ ] Dash duration
- [ ] Dash cooldown duration
- [ ] I-frame duration during dash

**Wall Interactions**:
- [ ] Wall slide fall speed
- [ ] Wall jump height
- [ ] Wall jump away-from-wall force
- [ ] Wall jump control percentage
- [ ] Wall jump control return timing

**Damage**:
- [ ] I-frame duration after hit
- [ ] Knockback distance
- [ ] Fall damage health penalty

**Tuning Philosophy**: 
Values should support:
- Celeste-inspired responsive feel
- Bullet-hell combat viability (fast dodge reactions)
- Precision platforming challenges
- Skill expression through movement combos
- Balance between accessibility and mastery

---

## Design Questions & To Be Determined

### Movement Feel & Physics

**Core Movement**:
- [ ] Overall movement speed targets (fast/medium/slow feel)
- [ ] Instant speed changes vs acceleration curves
- [ ] Friction and stopping distance
- [ ] Ground material variations (ice, mud, normal, etc.)

**Jumping**:
- [ ] Jump arc shape (floaty vs tight, linear vs curved)
- [ ] Variable jump height (hold button longer = higher jump)?
- [ ] "Fast fall" option (press down in air to fall faster)?

### Air Control & Aerial Movement

- [ ] Base horizontal air control percentage
- [ ] Apex control boost amount and window
- [ ] Direction change responsiveness in air
- [ ] Air control after double jump (same, more, less?)
- [ ] Air control interactions with dash/wall jump
- [ ] Can change direction or only adjust speed in air?

### Advanced Movement Mechanics

**Slide**:
- [ ] Slide momentum behavior (maintain, boost, or friction?)
- [ ] Slide-to-crouch transition timing and control
- [ ] Can button-mash to maintain slide speed or automatic deceleration only?
- [ ] Slide friction curve shape
- [ ] Slide jump requirements (minimum speed/distance traveled?)
- [ ] Slide jump boost scaling (based on slide speed remaining?)

**Dash**:
- [ ] Can dash in air, ground, or both?
- [ ] Dash distance variation by direction (diagonal shorter?)
- [ ] Visual cooldown indicator design
- [ ] Can queue dash input during cooldown?
- [ ] Dash momentum transfer to next action
- [ ] Can cancel dash into other actions early (with i-frame loss)?

**Wall Mechanics**:
- [ ] Wall slide trigger: automatic or button hold required?
- [ ] Wall slide fall speed (gentle slow or dramatic reduction?)
- [ ] Wall jump direction control amount (percentage)
- [ ] Wall jump control return timing (gradual, at apex, on landing?)
- [ ] Can chain wall jumps on same wall or must alternate?
- [ ] Wall surface types (some walls not slideable/jumpable?)

### Combat Integration

**Movement During Combat Actions**:
- [ ] Can shoot while: dashing? sliding? wall sliding? ducking? healing?
- [ ] Can use spell wheel while: dashing? jumping? any time?
- [ ] Does shooting affect movement speed or animation?
- [ ] Can move during heal animation? (planned yes, but pending testing)
- [ ] Priority system when actions conflict

**Aiming & Targeting**:
- [ ] 8-way shooting: stick direction, button combo, or other input?
- [ ] Auto-aim assist strength (none, subtle, strong?)
- [ ] Aim while moving vs stationary (same precision?)

### Damage & Survivability

- [ ] I-frame duration balance (bullet-hell forgiveness vs difficulty)
- [ ] I-frame visual clarity (must be obvious to player)
- [ ] Knockback amount and player control retention
- [ ] Fall damage health penalty (flat or percentage-based?)
- [ ] Fall respawn location (exact edge, safe platform, checkpoint?)
- [ ] Invincibility period after respawn from fall?

### Platform & Environment

- [ ] Fall-through platform input method
- [ ] Can fall through while moving or must be stationary?
- [ ] Environmental surface type variations (slippery, sticky, bouncy, etc.)
- [ ] Moving platform interactions

### Animation & Feel

- [ ] Animation blending priorities
- [ ] Upper/lower body split for simultaneous actions
- [ ] Transition animation needs
- [ ] Animation lock duration for various actions

---

## Cross-References

- [[Systems/GameFeel|Game Feel]] - Animation juice, particles, camera feel, hit feedback
- [[Mechanics/Combat|Combat System]] - (Future) Shooting mechanics, spell wheel, magic abilities
- [[Systems/CompanionSystem|Companion System]] - (Future) Healing mechanics, companion AI behavior
- [[Systems/UI|UI System]] - (Future) Health display, heal count, spell wheel UI
- [[Bosses/BossOverview|Boss Design]] - Mercy-kill animation context
- [[Overview|Game Overview]] - Core design pillars and philosophy

---

## Notes

### Design Philosophy

Movement is the foundation of player experience in Lament. It must support:
- **Precision platforming** - Tight controls for navigating complex level geometry
- **Bullet-hell combat** - Fast, responsive dodging and positioning
- **Skill expression** - Mastery through movement combos and advanced techniques
- **Accessibility** - Forgiveness systems (coyote time, buffering) help all players
- **Flow state** - When mastered, movement should feel effortless and fluid

### Reference Games

**Celeste** (Primary Movement Reference):
- Responsive controls with excellent feel
- Coyote time and jump buffering
- Dash commitment mechanics
- Wall jump and climb systems
- Slide-jump momentum mechanics
- Air control with apex consideration

**Cuphead** (Combat Context):
- Bullet-hell navigation requirements
- Dash i-frames for defensive play
- Fast, responsive dodging
- Clear visual feedback

**Hollow Knight** (General Feel):
- Tight platforming with simple moveset
- Wall interactions
- Dash as core mechanic
- I-frame timing importance

**Bioshock Infinite** (Spell Wheel Reference):
- Quick-swap between favorites
- Hold for full selection wheel
- Real-time (no pause) selection

**Dark Souls** (Heal System Reference):
- Limited heal charges (Estus Flask)
- Checkpoint refill system
- Risk/reward of healing timing

### Implementation Approach

**Phase 1 - Core Movement**:
1. Walk/run with proper acceleration
2. Jump with tunable height/arc
3. Basic air control
4. Crouch/duck

**Phase 2 - Forgiveness Systems**:
1. Coyote time implementation
2. Jump buffering
3. Tuning for feel

**Phase 3 - Advanced Movement**:
1. Slide mechanics
2. Slide jump
3. Dash with i-frames and cooldown
4. Wall slide and wall jump

**Phase 4 - Combat Integration**:
1. Shooting while moving
2. Spell wheel integration
3. Healing animation and movement
4. Action priority system

**Phase 5 - Polish & Tuning**:
1. Animation blending
2. Particle effects and juice
3. Extensive playtesting
4. Value tuning for optimal feel

### Tuning Priorities

When tuning movement values, prioritize:
1. **Responsiveness** - Controls must feel immediate and precise
2. **Predictability** - Consistent physics and behavior
3. **Skill ceiling** - Advanced techniques available for mastery
4. **Accessibility** - Forgiveness for imperfect inputs
5. **Combat viability** - Fast enough for bullet-hell dodging
6. **Platforming precision** - Tight enough for challenging platforming

Test scenarios:
- Tight platforming challenges (precision jumps, wall climb sequences)
- Dense bullet-hell encounters (dodge patterns, positioning)
- Movement combo sequences (slide-jump chains, wall climb speed)
- Combat mobility (shoot while moving, reposition during fights)

### Success Criteria

Movement system succeeds when:
- Players feel in control at all times
- Failures feel like player mistakes, not control issues
- Mastery provides satisfying skill expression
- Both platforming and combat feel good
- New players can learn easily while experts can optimize
- Movement enhances rather than hinders the dark, somber tone
