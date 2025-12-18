# Enemy AI System

## Overview

The enemy AI system for Lament uses a modular, component-based approach where individual behavior attributes can be combined to create unique and varied enemies. This system is inspired by classic retro game design principles where simple, well-defined behaviors create memorable and challenging encounters.

## Design Philosophy

Rather than creating each enemy from scratch, we build enemies by combining reusable attributes. This approach:

- **Reduces development time** - Reuse tested components
- **Increases variety** - Mix and match to create unique combinations
- **Simplifies balancing** - Tune individual attributes across all enemies
- **Enables emergent complexity** - Simple attributes combine into sophisticated behaviors

## Core Attribute Categories

### 1. Movement Attributes

Movement defines how an enemy navigates the game space.

#### **Stationary**
- Does not move at all
- Example: Turrets, traps, environmental hazards

#### **Walker**
- Walks or runs along the ground
- Example: Basic melee enemies, patrolling guards

#### **Riser**
- Can increase its height from the ground or emerge from surfaces
- Example: Enemies that rise from pools, spike traps

#### **Ducker**
- Can reduce height or sink into surfaces
- Example: Enemies that hide when approached

#### **Faller**
- Falls from ceiling or high surfaces onto the ground
- Example: Drops of acid, ambush enemies

#### **Jumper**
- Can bounce or jump (vertical or forward)
- Example: Hopping enemies, leaping creatures

#### **Floater**
- Can float, fly, or levitate freely
- Example: Flying enemies, ghosts, drones

#### **Sticky**
- Adheres to walls and ceilings
- Example: Spiders, crawling horrors

#### **Waver**
- Floats in a sine wave pattern
- Example: Floating heads, serpentine flyers

#### **Rotator**
- Rotates around a fixed point (which may itself move)
- Example: Orbiting drones, spinning blades

#### **Swinger**
- Swings from a fixed point like a pendulum
- Example: Hanging traps, ceiling monsters

#### **Pacer**
- Changes direction based on triggers (edges, walls, timers)
- Example: Patrolling enemies

#### **Follower**
- Actively pursues the player
- Example: Tracking enemies, hunting beasts

#### **Roamer**
- Changes direction randomly
- Example: Wandering creatures

#### **Liner**
- Moves in straight lines to specific points
- Example: Charging enemies, projectiles

#### **Teleporter**
- Can instantly move between locations
- Example: Blinking enemies, phase shifters

#### **Dasher**
- Performs rapid bursts of movement
- Example: Lunging attackers

#### **Ponger**
- Bounces off surfaces at angles, ignoring physics
- Example: Ricocheting projectiles

#### **Geobound**
- Physically locked to level geometry
- Example: Wall-mounted turrets, floor spikes

#### **Tethered**
- Connected to geometry by chain or rope
- Example: Chained beasts

#### **Swooper**
- Descends rapidly, often returning to original position
- Example: Diving birds, drop attacks

#### **Mirror**
- Mirrors or inverses player movement
- Example: Shadow enemies, reflection creatures

---

### 2. Quality Attributes

These attributes define inherent properties and resistances.

#### **GeoIgnore**
- Passes through solid level geometry
- Example: Ghosts, energy beings

#### **Shielder**
- Immune to damage from specific directions/angles
- Example: Armored enemies, shield bearers

#### **Deflector**
- Reflects ranged attacks back
- Example: Mirror shields, energy barriers

#### **Secret Spot**
- Only vulnerable in specific location
- Example: Weak points, critical hit zones

#### **Invulnerable**
- Cannot be harmed or killed
- Example: Environmental hazards, certain boss phases

#### **Revivor**
- Returns to life after death
- Example: Undead, resurrecting enemies

#### **Regenerator**
- Recovers health over time
- Example: Healing enemies, regenerating bosses

#### **Secret Weakness**
- Vulnerable only to specific attack types
- Example: Fire-weak, magic-resistant

#### **Hard to Hit**
- Difficult to strike due to size or speed
- Example: Tiny fast enemies, erratic movers

#### **Segmented**
- Composed of multiple destructible parts
- Example: Snake enemies, multi-part bosses

#### **Bumper**
- Pushes player or objects away on contact
- Example: Charging bulls, repelling shields

#### **GeoMimic**
- Has properties of level geometry (can be stood on, etc.)
- Example: Living platforms, turtle shells

#### **Alarm**
- Triggers reactions in other enemies or systems
- Example: Alert guards, summoning totems

---

### 3. Ability Attributes

Active abilities enemies can perform.

#### **Grower**
- Can increase in size
- Example: Inflating enemies, size-shifting bosses

#### **Shrinker**
- Can decrease in size
- Example: Compressing enemies

#### **Forcer**
- Applies movement force to player
- Example: Wind blasts, pushback attacks

#### **Carrier**
- Can grab and carry player or objects
- Example: Grabbing enemies, enemy kidnappers

#### **Thrower**
- Hurls held objects/players
- Example: Boulder throwers

#### **Emitter**
- Spawns other enemies or projectiles infinitely
- Example: Spawners, shooters, summoners

#### **Splitter**
- Divides into multiple enemies upon death
- Example: Slimes, splitting creatures

#### **Cloner**
- Duplicates itself without dying
- Example: Multiplying enemies

#### **Morpher**
- Transforms into different enemy types
- Example: Shape-shifters, evolving enemies

#### **Sapper**
- Reduces player stats or abilities
- Example: Slow effects, ability drain

#### **Latcher**
- Attaches to player and drains over time
- Example: Parasites, leeches

#### **Hider**
- Conceals itself based on conditions
- Example: Ambush enemies, hiding creatures

#### **Switcher**
- Toggles between different attribute sets
- Example: Phase-shifting enemies, mode-changing bosses

#### **Exploder**
- Self-destructs causing area damage
- Example: Suicide bombers, living bombs

#### **Interactor**
- Can activate level mechanisms
- Example: Door-opening enemies, trap-triggering foes

#### **Charger**
- Pauses before switching behaviors
- Example: Wind-up attacks, charging strikes

---

## Trigger System

Triggers are conditions that cause enemies to switch between attributes or behaviors.

### Common Triggers

- **Player Proximity** - Distance to player reaches threshold
- **Line of Sight** - Player visibility changes
- **Hit by Player** - Takes damage
- **Hits Player** - Deals damage
- **Timer** - After X seconds
- **Sequential** - After completing another action
- **Random** - Probabilistic behavior selection
- **Health Threshold** - At certain HP percentages

### Example Usage

```
Enemy: Ghost Sentinel
- Default: Floater + Invulnerable
- [Trigger - Player Line of Sight: False]: Follower + Vulnerable
- [Trigger - Player Line of Sight: True]: Stationary + Invulnerable
```

---

## Enemy Design Variables

Fine-tune enemy difficulty and feel with these variables:

- **Movement Speed** - How fast the enemy moves
- **Jump Height** - Vertical leap distance
- **Dash Length** - Distance covered in dash
- **Attack Range** - Reach of attacks
- **Splash Radius** - Area effect size
- **Size** - Physical dimensions
- **Health** - Damage before death
- **Damage** - Harm dealt to player
- **Detection Range** - How far they sense player

---

## Enemy Design Process

### 1. Define Core Identity
What is the enemy's role and theme?
- Tank, Glass Cannon, Support, etc.
- Visual theme and lore

### 2. Select Primary Attributes
Choose 2-4 attributes that define the enemy's core behavior.

### 3. Add Triggers
Define when the enemy switches behaviors or reveals weaknesses.

### 4. Tune Variables
Adjust speed, damage, health, etc. for desired difficulty.

### 5. Test and Iterate
Play test in various scenarios and level contexts.

---

## Example Enemy Designs

### Shadow Stalker
**Concept**: Ghost that only moves when unseen

**Attributes**:
- Floater
- GeoIgnore
- Follower
- Invulnerable

**Triggers**:
- [Player Line of Sight: False]: Follower + Vulnerable
- [Player Line of Sight: True]: Stationary + Invulnerable

**Variables**:
- Movement Speed: Medium-Fast
- Health: Low
- Damage: High

---

### Plague Carrier
**Concept**: Slow enemy that explodes into smaller enemies

**Attributes**:
- Walker
- Pacer
- Exploder
- Splitter
- Sapper (reduces player speed on contact)

**Triggers**:
- [Health: 0]: Exploder + Splitter (spawns 3 fast mini-enemies)
- [Player Proximity: Close]: Dasher (attempts to reach player)

**Variables**:
- Movement Speed: Slow
- Dash Speed: Very Fast
- Health: Medium-High
- Damage: Medium
- Split Count: 3 enemies

---

### Crystal Sentinel
**Concept**: Stationary turret with rotating shield

**Attributes**:
- Stationary
- Rotator (shield rotates around it)
- Emitter (shoots projectiles)
- Shielder (shield blocks damage)
- Secret Spot (vulnerable core when shield is away)

**Triggers**:
- [Timer: Every 3 seconds]: Emitter fires burst of 3 projectiles
- [Hit by Player: When shield away]: Takes damage

**Variables**:
- Shield Rotation Speed: Medium
- Fire Rate: 3 seconds
- Projectile Speed: Fast
- Health: High
- Damage: Medium

---

### Ambush Leaper
**Concept**: Hides underground and leaps at player

**Attributes**:
- Hider
- Riser
- Ducker
- Jumper
- Dasher (in air)

**Triggers**:
- [Player Proximity: Medium]: Riser (emerges from ground)
- [Player Proximity: Close]: Jumper + Dasher (leaps toward player)
- [Lands on ground]: Ducker (hides again after 2 seconds)
- [Hit by Player]: Ducker (immediately hides)

**Variables**:
- Jump Height: High
- Jump Speed: Fast
- Hide/Rise Duration: 1 second
- Health: Low-Medium
- Damage: Medium-High

---

## Design Tips

1. **Start Simple** - Begin with 2-3 attributes, add complexity through triggers
2. **Consider Player Tools** - Design enemies that challenge different player abilities
3. **Create Counterplay** - Every enemy should have a weakness or strategy
4. **Mix Difficulty Levels** - Same attributes with different variables create easy/hard variants
5. **Test Combinations** - Certain enemy pairings create emergent challenges
6. **Visual Clarity** - Attributes should be communicated through appearance and animation
7. **Respect Player Learning** - Introduce complex enemies after simpler variants

---

## Random Enemy Generator

For quick prototyping, randomly select:
- 2-3 Movement/Quality/Ability attributes
- 1-2 Triggers
- Variable values

Test the combination to see if it creates interesting gameplay!

---

## Notes

- Not all attribute combinations will work well - iteration is key
- Some attributes conflict and require triggers to switch between them
- Projectiles can be designed as "enemies" using this system
- Environmental hazards can use these attributes as well
- Boss enemies typically use more attributes and complex trigger systems
