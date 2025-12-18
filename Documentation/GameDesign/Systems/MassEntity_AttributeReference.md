# Mass Entity Attribute Reference

## Overview

Quick reference guide for all fragments in the Mass Entity system. Use this as a lookup table when designing entities.

**Document Purpose:**
- Fast fragment lookup
- Complete attribute catalog
- Processor reference
- Default values and typical usage

**Related Documents:**
- `EnemyAI.md` - Design philosophy and attribute descriptions
- `MassEntity_CoreArchitecture.md` - System fundamentals
- `MassEntity_MovementAndTriggers.md` - Movement implementations
- `MassEntity_CombatSystems.md` - Combat implementations

---

## Fragment Quick Reference Table

| Fragment | Category | Tier | Processor | Description |
|----------|----------|------|-----------|-------------|
| **Core Fragments** | | | | |
| FTransformFragment | Core | All | All movement | Entity position/rotation/scale |
| FVelocityFragment | Core | All | SimpleMovement | Linear velocity-based movement |
| FHealthFragment | Core | 2-3 | Health | HP, damage, death |
| FProjectileDataFragment | Core | 1-2 | Lifetime | Damage, lifetime, despawn |
| FSimpleCollisionFragment | Core | All | Collision | Basic collision detection |
| FTriggerStateFragment | Core | 2-3 | Trigger | State machine and triggers |
| FNiagaraVFXFragment | Core | All | Niagara | VFX management |
| FPerceptionFragment | Core | 3 | Perception | Player detection, LOS |
| **Movement Fragments** | | | | |
| FFloaterFragment | Movement | 2-3 | Floater | Sine wave bobbing |
| FFollowerFragment | Movement | 2-3 | Follower | Chase target (homing) |
| FWaverFragment | Movement | 2-3 | Waver | Sine wave along path |
| FLinerFragment | Movement | 1-2 | Liner | Straight line movement |
| FDasherFragment | Movement | 2-3 | Dasher | Burst movement |
| FRotatorFragment | Movement | 2-3 | Rotator | Orbit around point |
| FPacerFragment | Movement | 2-3 | Pacer | Patrol with turn-around |
| FRoamerFragment | Movement | 2-3 | Roamer | Random wandering |
| FWalkerFragment | Movement | 3 | Walker | Ground-locked movement |
| FJumperFragment | Movement | 2-3 | Jumper | Physics-based jumping |
| FStickyFragment | Movement | 2-3 | Sticky | Wall/ceiling adherence |
| FSwingerFragment | Movement | 2-3 | Swinger | Pendulum swing |
| FSwooperFragment | Movement | 2-3 | Swooper | Dive attack |
| FTeleporterFragment | Movement | 2-3 | Teleporter | Instant repositioning |
| FPongerFragment | Movement | 2-3 | Ponger | Bounce off walls |
| FGeoBindFragment | Movement | All | GeoBind | Locked to geometry |
| FTetheredFragment | Movement | 2-3 | Tethered | Rope/chain constraint |
| FMirrorFragment | Movement | 2-3 | Mirror | Copy player movement |
| FRiserFragment | Movement | 2-3 | Riser | Rise from surfaces |
| FDuckerFragment | Movement | 2-3 | Ducker | Sink into surfaces |
| FFallerFragment | Movement | 2-3 | Faller | Fall from ceiling |
| **Quality Fragments** | | | | |
| FShielderFragment | Quality | 2-3 | Collision | Directional damage immunity |
| FInvulnerableFragment | Quality | 2-3 | Health | Complete immunity |
| FDeflectorFragment | Quality | 2-3 | Collision | Reflect projectiles |
| FSecretSpotFragment | Quality | 2-3 | Collision | Weak point vulnerability |
| FRegeneratorFragment | Quality | 2-3 | Health | Health regeneration |
| FRevivorFragment | Quality | 3 | Health | Resurrect after death |
| FSecretWeaknessFragment | Quality | 2-3 | Health | Type-specific vulnerability |
| FBumperFragment | Quality | 2-3 | Collision | Push entities away |
| FGeoMimicFragment | Quality | 2-3 | Movement | Can be stood on |
| FAlarmFragment | Quality | 3 | Trigger | Trigger other entities |
| FGeoIgnoreFragment | Quality | 2-3 | Movement | Pass through walls |
| FHardToHitFragment | Quality | 2-3 | Collision | Small/fast hitbox |
| FSegmentedFragment | Quality | 3 | Special | Multi-part entity |
| **Ability Fragments** | | | | |
| FEmitterFragment | Ability | 2-3 | Emitter | Spawn entities/projectiles |
| FSplitterFragment | Ability | 2-3 | Splitter | Divide on death |
| FExploderFragment | Ability | 2-3 | Exploder | Area damage explosion |
| FClonerFragment | Ability | 3 | Cloner | Duplicate self |
| FForcerFragment | Ability | 2-3 | Force | Apply pushback |
| FGrowerFragment | Ability | 2-3 | Grower | Increase size |
| FShrinkerFragment | Ability | 2-3 | Shrinker | Decrease size |
| FCarrierFragment | Ability | 3 | Carrier | Grab player/objects |
| FThrowerFragment | Ability | 2-3 | Thrower | Throw objects |
| FMorpherFragment | Ability | 3 | Morpher | Transform entity type |
| FSapperFragment | Ability | 2-3 | Sapper | Reduce player stats |
| FLatcherFragment | Ability | 3 | Latcher | Attach and drain |
| FHiderFragment | Ability | 2-3 | Hider | Conditional visibility |
| FSwitcherFragment | Ability | 2-3 | Trigger | Toggle attribute sets |
| FInteractorFragment | Ability | 3 | Interactor | Activate mechanisms |
| FChargerFragment | Ability | 2-3 | Charger | Wind-up attacks |

---

## Core Fragments (Required)

### FTransformFragment
```cpp
FTransform Transform;
```
**Tier:** All  
**Required By:** Almost all processors  
**Purpose:** Entity world position, rotation, scale

---

### FVelocityFragment
```cpp
FVector Velocity = FVector::ZeroVector;
FVector Acceleration = FVector::ZeroVector;
float MaxSpeed = 1000.0f;
float Friction = 0.0f;
```
**Tier:** All  
**Processor:** `UMassSimpleMovementProcessor`  
**Purpose:** Physics-free linear movement

---

### FHealthFragment
```cpp
float CurrentHealth = 100.0f;
float MaxHealth = 100.0f;
bool bIsDead = false;
TMap<FGameplayTag, float> DamageTypeMultipliers;
float InvulnerabilityTimeRemaining = 0.0f;
```
**Tier:** 2-3  
**Processor:** `UMassHealthProcessor`  
**Purpose:** Health tracking, damage, death

---

### FProjectileDataFragment
```cpp
float Damage = 10.0f;
float MaxLifetime = 5.0f;
float CurrentAge = 0.0f;
float MaxDistance = -1.0f;
FVector SpawnLocation = FVector::ZeroVector;
bool bDespawnOffScreen = true;
FGameplayTagContainer ProjectileTags;
bool bHasHit = false;
```
**Tier:** 1-2  
**Processor:** `UMassProjectileLifetimeProcessor`  
**Purpose:** Projectile properties and lifetime

---

### FSimpleCollisionFragment
```cpp
ECollisionShape ShapeType = ECollisionShape::Sphere;
FVector CollisionSize = FVector(10.0f);
TEnumAsByte<ECollisionChannel> CollisionChannel = ECC_WorldDynamic;
FGameplayTagContainer IgnoreTags;
bool bDestroyOnHit = true;
bool bPenetrating = false;
int32 MaxPenetrations = -1;
int32 CurrentPenetrations = 0;
```
**Tier:** All  
**Processor:** `UMassSimpleCollisionProcessor`  
**Purpose:** Collision detection and response

---

### FTriggerStateFragment
```cpp
int32 CurrentStateIndex = 0;
int32 PreviousStateIndex = -1;
const UTriggerRuleSet* RuleSet = nullptr;
float TimeInState = 0.0f;
TMap<FName, float> CustomData;
```
**Tier:** 2-3  
**Processor:** `UMassTriggerProcessor`  
**Purpose:** State machine and behavior switching

---

### FNiagaraVFXFragment
```cpp
UNiagaraSystem* TrailSystem = nullptr;
UNiagaraComponent* ActiveTrailComponent = nullptr;
UNiagaraSystem* SpawnVFX = nullptr;
UNiagaraSystem* DeathVFX = nullptr;
UNiagaraSystem* HitVFX = nullptr;
FLinearColor TrailColor = FLinearColor::White;
float VFXScale = 1.0f;
bool bVFXVisible = true;
```
**Tier:** All (optional)  
**Processor:** `UMassNiagaraProcessor`  
**Purpose:** VFX management

---

### FPerceptionFragment
```cpp
FMassEntityHandle PlayerEntity;
bool bHasLineOfSight = false;
float DistanceToPlayer = 0.0f;
FVector LastKnownPlayerLocation = FVector::ZeroVector;
float DetectionRange = 1000.0f;
float UpdateInterval = 0.2f;
```
**Tier:** 3  
**Processor:** `UMassPerceptionProcessor`  
**Purpose:** Enemy AI perception

---

## Movement Fragments

### FFloaterFragment
```cpp
float FloatHeight = 100.0f;
float BobSpeed = 2.0f;
float BobAmplitude = 20.0f;
float TimeOffset = 0.0f;
bool bRelativeToGround = false;
```
**Processor:** `UMassFloaterProcessor`  
**Usage:** Flying enemies, hovering drones, floating objects  
**Example:** Ghost that bobs while chasing player

---

### FFollowerFragment
```cpp
FMassEntityHandle Target;
float FollowSpeed = 300.0f;
float StoppingDistance = 50.0f;
float TurnRate = 360.0f;
float Acceleration = 0.0f;
bool bPredictTargetMovement = false;
```
**Processor:** `UMassFollowerProcessor`  
**Usage:** Homing missiles, chasing enemies  
**Example:** Projectile that homes in on player

---

### FWaverFragment
```cpp
float WaveFrequency = 1.0f;
float WaveAmplitude = 50.0f;
FVector WaveDirection = FVector::RightVector;
float PhaseOffset = 0.0f;
float ForwardSpeed = 200.0f;
```
**Processor:** `UMassWaverProcessor`  
**Usage:** Weaving projectiles, serpentine enemies  
**Example:** Projectile that snakes left-right while moving forward

---

### FDasherFragment
```cpp
float DashSpeed = 800.0f;
float DashDuration = 0.3f;
FVector DashDirection = FVector::ZeroVector;
bool bIsDashing = false;
float DashCooldown = 2.0f;
```
**Processor:** `UMassDasherProcessor`  
**Usage:** Lunging enemies, dash attacks  
**Example:** Enemy that walks slowly, then lunges at player

---

### FRotatorFragment
```cpp
FVector CenterPoint = FVector::ZeroVector;
FMassEntityHandle CenterEntity;
float OrbitRadius = 100.0f;
float RotationSpeed = 90.0f;
float CurrentAngle = 0.0f;
FVector RotationAxis = FVector::UpVector;
```
**Processor:** `UMassRotatorProcessor`  
**Usage:** Orbiting projectiles, rotating shields  
**Example:** Bullets orbiting around boss

---

### FPacerFragment
```cpp
float Speed = 150.0f;
float DirectionMultiplier = 1.0f;
float EdgeCheckDistance = 50.0f;
bool bReverseAtEdges = true;
bool bReverseAtWalls = true;
```
**Processor:** `UMassPacerProcessor`  
**Usage:** Patrolling enemies, platform enemies  
**Example:** Enemy that walks back-and-forth on platform

---

### FRoamerFragment
```cpp
float Speed = 100.0f;
FVector CurrentDirection = FVector::ForwardVector;
float MinChangeInterval = 1.0f;
float MaxChangeInterval = 3.0f;
bool bMovementIn2D = true;
```
**Processor:** `UMassRoamerProcessor`  
**Usage:** Wandering enemies, ambient creatures  
**Example:** Enemy that randomly changes direction

---

## Quality Fragments

### FShielderFragment
```cpp
FVector ShieldDirection = FVector::ForwardVector;
float ShieldArc = 180.0f;
bool bRotatesWithEntity = true;
float ShieldHealth = -1.0f;
```
**Usage:** Shielded enemies, armored units  
**Blocks damage from specific angles**  
**Example:** Knight enemy with front-facing shield

---

### FInvulnerableFragment
```cpp
TArray<FGameplayTag> IgnoredDamageTypes;
bool bShowVisualFeedback = true;
```
**Usage:** Phase-based invulnerability, environmental hazards  
**Complete damage immunity**  
**Example:** Boss during invincible phase

---

### FDeflectorFragment
```cpp
FGameplayTagContainer DeflectableTypes;
EDeflectionType DeflectionType = EDeflectionType::Mirror;
float DeflectedDamageMultiplier = 1.0f;
```
**Usage:** Reflecting enemies, energy shields  
**Reflects projectiles back**  
**Example:** Enemy with reflecting shield

---

### FRegeneratorFragment
```cpp
float RegenRate = 5.0f;
float RegenDelay = 3.0f;
float TimeSinceLastDamage = 0.0f;
float MaxRegenHealth = -1.0f;
```
**Usage:** Regenerating enemies, healing bosses  
**Passive health recovery**  
**Example:** Boss that heals when not taking damage

---

### FSecretSpotFragment
```cpp
FVector WeakSpotOffset = FVector(0, 0, 100);
float WeakSpotRadius = 20.0f;
float WeakSpotDamageMultiplier = 3.0f;
bool bWeakSpotRotates = false;
```
**Usage:** Weak point bosses, critical hit enemies  
**Only vulnerable in specific spot**  
**Example:** Boss with glowing weak spot on back

---

## Ability Fragments

### FEmitterFragment
```cpp
const UEntityArchetype* EmittedArchetype = nullptr;
float EmitInterval = 1.0f;
int32 MaxEmissions = -1;
FVector EmitOffset = FVector(50, 0, 0);
float EmitSpeed = 400.0f;
int32 BurstCount = 1;
bool bAimAtPlayer = true;
```
**Processor:** `UMassEmitterProcessor`  
**Usage:** Turrets, spawners, shooters  
**Spawns other entities at intervals**  
**Example:** Turret that fires 3 bullets every 2 seconds

---

### FSplitterFragment
```cpp
const UEntityArchetype* SplitArchetype = nullptr;
int32 SplitCount = 3;
float SplitVelocity = 200.0f;
ESplitPattern SplitPattern = ESplitPattern::Radial;
bool bSplitOnDeath = true;
```
**Processor:** `UMassSplitterProcessor`  
**Usage:** Splitting enemies, fragmenting projectiles  
**Divides into multiple entities**  
**Example:** Slime that splits into 3 smaller slimes on death

---

### FExploderFragment
```cpp
float ExplosionRadius = 200.0f;
float ExplosionDamage = 50.0f;
EDamageFalloff DamageFalloff = EDamageFalloff::Linear;
bool bExplodeOnDeath = true;
UNiagaraSystem* ExplosionVFX = nullptr;
```
**Processor:** `UMassExploderProcessor`  
**Usage:** Suicide bombers, explosive projectiles  
**Area damage explosion**  
**Example:** Bomb that explodes on contact

---

### FClonerFragment
```cpp
const UEntityArchetype* CloneArchetype = nullptr;
int32 CloneCount = 1;
float CloneInterval = 5.0f;
int32 MaxTotalClones = -1;
float CloneHealthMultiplier = 1.0f;
```
**Processor:** `UMassClonerProcessor`  
**Usage:** Multiplying enemies, cloning projectiles  
**Duplicates self without dying**  
**Example:** Enemy that creates copy every 5 seconds

---

### FForcerFragment
```cpp
float ForceMagnitude = 500.0f;
FVector ForceDirection = FVector::ForwardVector;
bool bRelativeDirection = true;
bool bApplyOnHitOnly = true;
EForceType ForceType = EForceType::Impulse;
```
**Processor:** `UMassForceProcessor`  
**Usage:** Knockback attacks, wind zones  
**Applies movement force**  
**Example:** Explosion that pushes player back

---

## Processor Quick Reference

### Execution Order

```
PreMovement:
  - UMassPerceptionProcessor (updates enemy awareness)
  - UMassTriggerProcessor (evaluates conditions, switches states)

Movement:
  - UMassSimpleMovementProcessor (velocity-based)
  - UMassFloaterProcessor, UMassFollowerProcessor, etc. (attribute-based)

Tasks:
  - UMassEmitterProcessor (spawns entities)
  - UMassClonerProcessor (duplicates entities)
  - UMassCollisionProcessor (detects hits)

Late Tasks:
  - UMassHealthProcessor (applies damage, checks death)
  - UMassExploderProcessor (explodes entities)
  - UMassSplitterProcessor (splits entities)
  - UMassForceProcessor (applies pushback)

PostMovement:
  - UMassProjectileLifetimeProcessor (despawns old entities)
  - UMassNiagaraProcessor (syncs VFX)
```

### Processor Dependencies

| Processor | Depends On | Required Fragments |
|-----------|------------|-------------------|
| SimpleMovement | None | Transform, Velocity |
| Floater | None | Transform, Floater |
| Follower | None | Transform, Follower |
| Trigger | None | TriggerState |
| Emitter | Trigger | Transform, Emitter |
| Collision | Movement | Transform, Collision |
| Health | Collision | Health |
| Exploder | Health | Transform, Exploder |
| Splitter | Health | Transform, Splitter |
| Force | Collision | Transform, Forcer |
| Niagara | All | Transform, NiagaraVFX |

---

## Common Entity Recipes

### Simple Bullet
```
Tier: 1
Fragments: Transform, Velocity, ProjectileData, SimpleCollision, NiagaraVFX
Processors: SimpleMovement, Lifetime, Collision
Use Case: Basic projectile
```

### Homing Missile
```
Tier: 2
Fragments: Transform, Liner, Follower, Exploder, TriggerState, NiagaraVFX
States: 
  0: Liner (0.5s) → 1
  1: Follower + Exploder on hit
Use Case: Smart projectile
```

### Splitting Bomb
```
Tier: 2
Fragments: Transform, Waver, Exploder, Splitter, Forcer, TriggerState
States:
  0: Waver (2s OR hit) → Explode + Split + Force
Use Case: Chain reaction projectile
```

### Patrol Enemy
```
Tier: 3
Fragments: Transform, Pacer, Dasher, Health, Perception, TriggerState
States:
  0: Pacer (patrol)
  1: Dasher (player close) → lunge
Use Case: Basic ground enemy
```

### Flying Chaser
```
Tier: 3
Fragments: Transform, Floater, Follower, Health, Perception, TriggerState
States:
  0: Floater (idle bob)
  1: Floater + Follower (chase while bobbing)
Use Case: Airborne enemy
```

### Boss Enemy
```
Tier: 3
Fragments: Transform, Roamer, Emitter, Exploder, Splitter, Health, TriggerState
States:
  0: Phase 1 (HP > 66%) - Roamer + Emitter(slow)
  1: Phase 2 (HP > 33%) - Roamer + Emitter(fast) + Exploder
  2: Phase 3 (HP > 0%) - Roamer + Emitter(fast) + Exploder + Splitter
Use Case: Multi-phase boss
```

---

## Fragment Size Reference

| Fragment | Approximate Size | Notes |
|----------|------------------|-------|
| FTransformFragment | ~60 bytes | FTransform overhead |
| FVelocityFragment | ~40 bytes | 3 FVectors + float |
| FHealthFragment | ~60 bytes | Floats + TMap |
| FProjectileDataFragment | ~80 bytes | Multiple properties |
| FSimpleCollisionFragment | ~60 bytes | Vector + enums |
| FTriggerStateFragment | ~50 bytes | Ints + pointer + TMap |
| FNiagaraVFXFragment | ~80 bytes | Multiple pointers |
| Movement Fragments | ~40-60 bytes | Typically 5-10 floats |
| Quality Fragments | ~30-50 bytes | Few properties |
| Ability Fragments | ~60-100 bytes | Complex data |

**Total Tier 1 Entity:** ~300-400 bytes  
**Total Tier 2 Entity:** ~500-700 bytes  
**Total Tier 3 Entity:** ~800-1200 bytes

---

## Performance Guidelines

| Tier | Target Count | Update Cost | Use For |
|------|--------------|-------------|---------|
| Tier 1 | 200-300 | 0.01ms/100 | Simple projectiles |
| Tier 2 | 50-100 | 0.05ms/50 | Complex projectiles |
| Tier 3 | 30-50 | 0.1ms/30 | Enemies, bosses |

**Optimization Tips:**
- Prefer Tier 1 for common entities
- Use Tier 2 for special projectiles
- Reserve Tier 3 for enemies only
- Stagger expensive updates (perception every 0.2s)
- Pool VFX components
- Cull off-screen entities

---

## Summary

This reference provides:
- ✅ Complete fragment catalog (40+ fragments)
- ✅ Quick lookup table
- ✅ Default values and usage
- ✅ Processor dependencies
- ✅ Common entity recipes
- ✅ Performance guidelines

**For Detailed Implementation:**
- See `MassEntity_CoreArchitecture.md` for fundamentals
- See `MassEntity_MovementAndTriggers.md` for movement details
- See `MassEntity_CombatSystems.md` for combat details
- See `MassEntity_AdvancedSystems.md` for production features
- See `MassEntity_Templates.md` for copy-paste code

---

**Document Version:** 1.0  
**Last Updated:** December 2024  
**UE Version:** 5.7+
