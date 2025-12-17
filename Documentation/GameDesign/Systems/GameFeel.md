# Game Feel

> **Status**: Concept Development  
> **Last Updated**: 2025-12-16

---

## Overview

Game feel (or "game juice") refers to the visual, audio, and tactile feedback that makes gameplay satisfying and responsive. This document catalogs techniques to enhance player experience through polish and feedback.

**Philosophy**: Lament should feel quick and responsive (Celeste-style) while maintaining visual clarity despite bullet-hell density (Cuphead-style).

---

## Core Techniques

### Impact & Feedback

- **Time stop / Hit pause** - Brief freeze when attacks connect or player gets hit (similar to Hollow Knight)
  - On player taking damage: _[duration TBD]_
  - On enemy kill: _[duration TBD]_
  - On critical moments: _[TBD]_
- **Screen shake** - Camera shake on impacts
  - Intensity scaling: _[light/medium/heavy TBD]_
  - Stacking behavior: _[TBD - accumulate or cap?]_
  - Different patterns for different attack types
- **Camera punch** - Sharp directional camera movement on heavy hits (distinct from shake)
- **Knockback** - Enemies (and player) pushed back on hit
- **Flash/blink** - Hit entities flash white/color briefly
- **Impact particles** - Sparks, dust, magic effects on collision

### Animation

- **Squash / Stretch** - Character deformation on jumps and impacts
  - Jump squash on takeoff
  - Stretch during ascent/descent
  - Landing squash (intensity based on fall height)
- **Lean animation** - Character tilts in direction of movement/acceleration
- **Skid/slide** - Brief slide when changing direction at high speed
- **Secondary motion** - Hair/cloth/trailing elements continue moving after character stops
- **Anticipation frames** - Brief windup before actions (attacks, jumps, etc.)

### Movement Feedback

- **Dust particles** - On running, landing, direction changes
  - Run dust trail
  - Landing dust puff (scaled to fall height)
  - Skid dust on direction change
- **Footstep variety** - Different sounds and particles per surface type
- **Whoosh sounds** - Air movement on jumps, dashes, fast movement
- **Platform wobble** - Platforms react when landing on them

See [[Mechanics/PlayerMovement|Player Movement]] for movement mechanics (coyote time, jump buffer, etc.)

### Combat & Shooting

- **Muzzle flash** - Bright effect when firing projectiles
- **Recoil animation** - Character pushed back slightly when shooting
- **Projectile trails** - Visual trails following shots (2D sprite-based)
- **Charge-up effects** - Visual buildup before powerful attacks
- **Cast anticipation** - Brief windup animation before magic fires
- **Area of effect rings** - Expanding circles showing ability range/impact

### Visual Clarity (Bullet Hell Considerations)

- **Player vs Enemy differentiation** - Clear visual distinction between player and enemy projectiles
  - Color coding
  - Shape language
  - Glow/outline styles
- **Attack telegraphs** - Visual tells before attacks fire
  - Enemy wind-up animations
  - Target indicators
  - Warning flashes
- **Danger highlights** - _[TBD - slow-down or highlight critical attacks?]_

### Lighting & Visual Effects

- **Attack light emission** - All attacks emit light to illuminate environments
  - _[Dynamic lighting vs glow effect - TBD]_
  - _[Player magic color vs enemy magic color - TBD]_
- **Particle light emission** - Situational particle effects that also emit light
  - _[Shadow casting or additive glow - TBD]_
- **2D sprite sheet animations** - Magic attacks and projectiles use 2D sprite sheets
  - _[Style: hand-drawn/pixel art/fluid - TBD]_
  - _[Resolution/scale - TBD]_

### Environmental

- **Parallax layers** - Background moves at different speeds for depth
- **Grass/foliage sway** - Environmental elements react to player movement
- **Water ripples** - Splashes and ripples when moving through water
- **Fire flicker** - Dynamic lighting from flame sources (e.g., Sister Trio boss arena)
- **Surface-specific effects** - Different particle/sound responses per terrain type

### UI Feedback

- **Health bar shake** - When taking damage
- **Low health effects** - Visual/audio warning at low health
  - Screen desaturation
  - Vignette effect
  - Heartbeat audio
  - _[Intensity/timing - TBD]_
- **Button prompts bounce** - Interaction prompts have subtle pulse animation
- **Boss health bar slam** - Dramatic entrance animation when boss health bar appears

### Audio (Supporting Feel)

- **Impact sounds** - Meaty hit sounds with appropriate reverb
- **Layered combat audio** - Multiple sound layers for attacks (whoosh + impact + magic)
- **Dynamic mixing** - Audio responds to action intensity
- **Spatial audio** - Sound positioning for attacks and impacts

---

## Boss-Specific Feel

**Note**: See [[Bosses/BossOverview|Boss Design]] for complete boss mechanics

- **Mercy-kill slow-mo** - Time slows during mercy-kill sequence
  - _[Speed: 50%/25%/other - TBD]_
  - _[During approach, button press, or death animation - TBD]_
- **Lament transition** - Visual transition into Lament cutscene
  - _[Fade/blur/desaturate approach - TBD]_
  - _[Seamless vs cut transition - TBD]_
- **Boss entrance shake** - Arena shakes when boss enters or roars
- **Phase transition effects** - Visual pop when boss changes phases

---

## Companion-Specific Feel

**Note**: See [[Systems/CompanionSystem|Companion System]] (future doc) for complete companion mechanics

- **Healing particle flow** - Visual flow from companion to player during heal
- **Companion visual states** - Animations change based on companion's health/condition
  - _[Specific states/thresholds - TBD]_
- **Hurt reaction** - Companion visibly reacts when healing drains her
  - Animation
  - Particle effect
  - _[Sound cue - pained but no words - TBD]_
- **Player heal glow** - Brief effect when receiving heal
- **Companion pulse/glow** - Visual indicator of companion's current state

---

## Camera

### Normal Gameplay

- **Camera follow** - Camera moves with player (not locked off)
  - Smooth follow with slight lag (Hollow Knight-style)
  - _[Look-ahead in movement direction? - TBD]_
  - _[Vertical vs horizontal follow behavior - TBD]_

### Boss Arenas

- **Camera lock** - Camera may be locked off during boss fights (similar to Hollow Knight)
  - Fixed frame showing entire arena
  - _[Zoom level per boss arena - TBD]_
  - _[Transition between follow and lock - TBD]_

### Screen Effects

- **Effect management** - _[TBD - how to handle multiple simultaneous shake/punch effects]_

---

## Technical Considerations

### Performance

- **Optimization** - Budget irrelevant for now, optimize later
- **Effect stacking** - _[TBD - how do simultaneous effects interact?]_
- **Particle limits** - _[TBD - max particles on screen?]_

### Consistency

- **Tone balance** - Quick/responsive gameplay (Celeste) while maintaining dark, somber tone
- **Visual language** - Consistent particle and effect styles across all systems
- **Audio cohesion** - Music-driven narrative with sound effects supporting feel

---

## Design Questions & To Be Determined

**Combat Feel**:
- [ ] Time-stop duration for hit vs kill
- [ ] Screen shake intensity rules and stacking behavior
- [ ] Enemy hit reaction specifics (stun, knockback distance, i-frames)
- [ ] Attack telegraph timing and visual language

**Visual Effects**:
- [ ] Dynamic lighting vs glow approach for magic attacks
- [ ] Player magic color vs enemy magic color differentiation
- [ ] 2D sprite animation style and resolution
- [ ] Particle shadow casting or additive glow only

**Camera**:
- [ ] Camera follow lag amount and smoothing
- [ ] Look-ahead in movement direction (yes/no, distance)
- [ ] Vertical vs horizontal follow behavior differences
- [ ] Boss arena camera zoom levels
- [ ] Transition smoothness between follow and lock modes
- [ ] Screen effect management when multiple effects trigger

**Boss/Companion Feel**:
- [ ] Mercy-kill slow-mo specifics (speed, duration, scope)
- [ ] Lament cutscene transition approach
- [ ] Companion hurt sound design (emotional but no words)
- [ ] Healing time/player control during heal
- [ ] Companion visual state thresholds

**Bullet Hell Clarity**:
- [ ] Projectile differentiation system (color/shape/glow)
- [ ] Critical attack highlighting or slow-down
- [ ] Visual tell system for enemy attacks

---

## Cross-References

- [[Mechanics/PlayerMovement|Player Movement]] - Movement mechanics, coyote time, jump buffer
- [[Bosses/BossOverview|Boss Design]] - Mercy-kill mechanics, boss-specific feel
- [[Systems/CompanionSystem|Companion System]] - (Future) Complete companion mechanics
- [[Mechanics/Combat|Combat System]] - (Future) Combat mechanics and abilities
- [[Reference/NamingConventions|Naming Conventions]] - Code implementation standards

---

## Notes

- Game feel is iterative - implement, test, adjust
- Reference games: Celeste (movement feel), Cuphead (visual clarity), Hollow Knight (hit pause, camera)
- Balance responsiveness with weight/impact
- Music drives narrative; sound effects drive feel
- All effects should support the dark, somber tone while maintaining clarity
