# Mass Entity Combat Systems

## Overview

This document covers all combat-related fragments and systems: damage, abilities, quality attributes, collision, and force application. These systems allow entities to interact with the player, environment, and each other.

**Prerequisites:**
- Read `MassEntity_CoreArchitecture.md`
- Read `MassEntity_MovementAndTriggers.md`
- Understanding of fragments, processors, and triggers

**What You'll Learn:**
- Quality attributes (defensive/resistance behaviors)
- Ability attributes (active combat abilities)
- Complete implementations (Emitter, Splitter, Exploder)
- Collision system
- Force application (pushback without Chaos physics)
- Complete entity examples (Homing Missile, Splitting Bomb, Plague Carrier)

---

## Table of Contents

1. Combat System Overview
2. Quality Fragments Reference
3. Ability Fragments Reference
4. Combat Processors
5. Full Implementation: Emitter System
6. Full Implementation: Exploder + Splitter System
7. Collision System
8. Force Application & Pushback
9. Complete Entity Examples

---

## 1. Combat System Overview

### 1.1 Combat Architecture

```
Combat Flow (Each Frame):

[UMassTriggerProcessor] ← Check triggers (health, hit events)
    ↓
[Movement Processors] ← Update positions
    ↓
[Ability Processors] ← Execute abilities (emit, clone, charge)
    ↓
[Collision Processor] ← Detect hits
    ↓
[Health Processor] ← Apply damage, check death
    ↓
[Splitter/Exploder] ← Death-triggered abilities
    ↓
[Force Processor] ← Apply pushback to hit targets
    ↓
[Niagara Processor] ← Spawn hit/death VFX
```

### 1.2 Quality vs Ability Attributes

**Quality Attributes** (Passive/Defensive):
- Define HOW entities respond to attacks
- Examples: Shielder, Invulnerable, Deflector, Regenerator
- Usually always active (or toggled by triggers)

**Ability Attributes** (Active/Offensive):
- Define WHAT entities can do
- Examples: Emitter, Splitter, Exploder, Grower
- Usually triggered by conditions (timer, health, hit)

### 1.3 Damage Flow

```
Projectile hits Enemy:
    ↓
1. Collision Processor detects hit
    ↓
2. Check Quality Attributes:
    - Shielder: Block if hit from protected angle?
    - Invulnerable: Ignore damage?
    - Deflector: Reflect projectile?
    - SecretSpot: Only vulnerable in specific location?
    ↓
3. If damage allowed:
    - Apply damage to FHealthFragment
    - Trigger hit events (OnHit triggers)
    - Spawn hit VFX
    ↓
4. Check death:
    - If health <= 0:
        - Set bIsDead = true
        - Trigger death abilities (Exploder, Splitter, etc.)
        - Spawn death VFX
        - Despawn entity
```

---

## 2. Quality Fragments Reference

### 2.1 FShielderFragment

**Purpose:** Block damage from specific directions/angles.

**Declaration:**
```cpp
// ShielderFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "ShielderFragment.generated.h"

/**
 * Directional damage immunity.
 * Blocks hits from specific angles (e.g., front-facing shield).
 * Used by: Shielded enemies, armored units, defensive bosses.
 */
USTRUCT()
struct LAMENT_API FShielderFragment : public FMassFragment
{
    GENERATED_BODY()

    // Shield direction (relative to entity forward)
    UPROPERTY()
    FVector ShieldDirection = FVector::ForwardVector;

    // Shield arc in degrees (180 = half-circle, 360 = all directions)
    UPROPERTY()
    float ShieldArc = 180.0f;

    // Does shield rotate with entity?
    UPROPERTY()
    bool bRotatesWithEntity = true;

    // Optional: Shield health (can be broken)
    UPROPERTY()
    float ShieldHealth = -1.0f; // -1 = infinite

    // Optional: Shield regeneration rate
    UPROPERTY()
    float ShieldRegenRate = 0.0f;
};
```

**Usage:** Collision processor checks hit angle against shield arc before applying damage.

---

### 2.2 FInvulnerableFragment

**Purpose:** Complete immunity to damage.

**Declaration:**
```cpp
// InvulnerableFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "InvulnerableFragment.generated.h"

/**
 * Complete damage immunity.
 * Presence of this fragment = cannot take damage.
 * Usually added/removed by triggers (phase-based invulnerability).
 */
USTRUCT()
struct LAMENT_API FInvulnerableFragment : public FMassFragment
{
    GENERATED_BODY()

    // Optional: Specific damage types to ignore (empty = all)
    UPROPERTY()
    TArray<FGameplayTag> IgnoredDamageTypes;

    // Visual feedback (flash, shader effect, etc.)
    UPROPERTY()
    bool bShowVisualFeedback = true;
};
```

**Usage:** Health processor skips damage if this fragment present.

---

### 2.3 FDeflectorFragment

**Purpose:** Reflect projectiles back.

**Declaration:**
```cpp
// DeflectorFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "GameplayTagContainer.h"
#include "DeflectorFragment.generated.h"

/**
 * Reflects projectiles that hit this entity.
 * Can reflect back to shooter or in mirror angle.
 */
USTRUCT()
struct LAMENT_API FDeflectorFragment : public FMassFragment
{
    GENERATED_BODY()

    // Which projectile types can be deflected?
    UPROPERTY()
    FGameplayTagContainer DeflectableTypes;

    // Reflection behavior
    UPROPERTY()
    EDeflectionType DeflectionType = EDeflectionType::Mirror;

    // Damage multiplier for deflected projectiles
    UPROPERTY()
    float DeflectedDamageMultiplier = 1.0f;

    // Speed multiplier for deflected projectiles
    UPROPERTY()
    float DeflectedSpeedMultiplier = 1.0f;
};

UENUM()
enum class EDeflectionType : uint8
{
    Mirror,         // Reflect at mirror angle
    BackToShooter,  // Send directly back to shooter
    Random          // Random direction
};
```

**Usage:** Collision processor redirects projectile instead of destroying it.

---

### 2.4 FSecretSpotFragment

**Purpose:** Vulnerable only in specific location.

**Declaration:**
```cpp
// SecretSpotFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "SecretSpotFragment.generated.h"

/**
 * Only vulnerable when hit in specific spot (weak point).
 * Opposite of Shielder - everywhere is protected except one spot.
 */
USTRUCT()
struct LAMENT_API FSecretSpotFragment : public FMassFragment
{
    GENERATED_BODY()

    // Weak spot location (relative to entity)
    UPROPERTY()
    FVector WeakSpotOffset = FVector(0, 0, 100); // Top of entity

    // Weak spot radius
    UPROPERTY()
    float WeakSpotRadius = 20.0f;

    // Damage multiplier when hitting weak spot
    UPROPERTY()
    float WeakSpotDamageMultiplier = 3.0f;

    // Can weak spot move? (e.g., rotating boss core)
    UPROPERTY()
    bool bWeakSpotRotates = false;

    // Rotation speed if rotating
    UPROPERTY()
    float RotationSpeed = 0.0f;

    // Current rotation angle
    UPROPERTY()
    float CurrentAngle = 0.0f;
};
```

**Usage:** Collision processor only applies damage if hit location within weak spot radius.

---

### 2.5 FRegeneratorFragment

**Purpose:** Health regeneration over time.

**Declaration:**
```cpp
// RegeneratorFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "RegeneratorFragment.generated.h"

/**
 * Passive health regeneration.
 * Can have delays, limits, and conditional activation.
 */
USTRUCT()
struct LAMENT_API FRegeneratorFragment : public FMassFragment
{
    GENERATED_BODY()

    // HP recovered per second
    UPROPERTY()
    float RegenRate = 5.0f;

    // Delay after taking damage before regen starts
    UPROPERTY()
    float RegenDelay = 3.0f;

    // Time since last damage
    UPROPERTY()
    float TimeSinceLastDamage = 0.0f;

    // Max health to regenerate to (-1 = full health)
    UPROPERTY()
    float MaxRegenHealth = -1.0f;

    // Can regenerate while in combat?
    UPROPERTY()
    bool bRegenInCombat = false;
};
```

**Usage:** Health processor updates health each frame based on regen rate.

---

### 2.6 Additional Quality Fragments (Brief)

**FRevivorFragment** - Resurrect after death
**FSecretWeaknessFragment** - Vulnerable to specific damage types only
**FBumperFragment** - Push away entities on contact
**FGeoMimicFragment** - Can be stood on by player
**FAlarmFragment** - Trigger other entities when activated

**See `MassEntity_AttributeReference.md` for complete declarations.**

---

## 3. Ability Fragments Reference

### 3.1 FEmitterFragment

**Purpose:** Spawn other entities (projectiles, enemies).

**Declaration:**
```cpp
// EmitterFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "EmitterFragment.generated.h"

class UEntityArchetype;

/**
 * Spawns other entities at intervals.
 * Used by: Shooters, spawners, summoners, turrets.
 */
USTRUCT()
struct LAMENT_API FEmitterFragment : public FMassFragment
{
    GENERATED_BODY()

    // What to spawn
    UPROPERTY()
    TObjectPtr<const UEntityArchetype> EmittedArchetype = nullptr;

    // Emit interval (seconds)
    UPROPERTY()
    float EmitInterval = 1.0f;

    // Time since last emit
    UPROPERTY()
    float TimeSinceLastEmit = 0.0f;

    // Max emissions (-1 = infinite)
    UPROPERTY()
    int32 MaxEmissions = -1;

    // Emissions count
    UPROPERTY()
    int32 EmissionsRemaining = -1;

    // Spawn offset (relative to entity)
    UPROPERTY()
    FVector EmitOffset = FVector(50, 0, 0);

    // Emit direction (or target entity)
    UPROPERTY()
    FVector EmitDirection = FVector::ForwardVector;

    // Emit velocity
    UPROPERTY()
    float EmitSpeed = 400.0f;

    // Burst count (spawn multiple at once)
    UPROPERTY()
    int32 BurstCount = 1;

    // Spread angle for bursts
    UPROPERTY()
    float BurstSpreadAngle = 15.0f;

    // Auto-aim at player?
    UPROPERTY()
    bool bAimAtPlayer = true;
};
```

**Processor:** `UMassEmitterProcessor` (Section 5)

---

### 3.2 FSplitterFragment

**Purpose:** Split into multiple entities on death.

**Declaration:**
```cpp
// SplitterFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "SplitterFragment.generated.h"

/**
 * Divides into multiple smaller entities.
 * Triggered on death or manually.
 * Used by: Slimes, splitting bombs, dividing enemies.
 */
USTRUCT()
struct LAMENT_API FSplitterFragment : public FMassFragment
{
    GENERATED_BODY()

    // What to split into
    UPROPERTY()
    TObjectPtr<const UEntityArchetype> SplitArchetype = nullptr;

    // How many to spawn
    UPROPERTY()
    int32 SplitCount = 3;

    // Speed of split entities
    UPROPERTY()
    float SplitVelocity = 200.0f;

    // Split pattern
    UPROPERTY()
    ESplitPattern SplitPattern = ESplitPattern::Radial;

    // Trigger condition
    UPROPERTY()
    bool bSplitOnDeath = true;

    UPROPERTY()
    bool bSplitOnHit = false;

    // Has split occurred?
    UPROPERTY()
    bool bHasSplit = false;
};

UENUM()
enum class ESplitPattern : uint8
{
    Radial,        // Evenly spaced circle
    Random,        // Random directions
    Forward,       // All in forward cone
    Upward         // Upward burst
};
```

**Processor:** `UMassSplitterProcessor` (Section 6)

---

### 3.3 FExploderFragment

**Purpose:** Explode dealing area damage.

**Declaration:**
```cpp
// ExploderFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "NiagaraSystem.h"
#include "ExploderFragment.generated.h"

/**
 * Area-of-effect explosion.
 * Can be triggered on death, contact, or manually.
 */
USTRUCT()
struct LAMENT_API FExploderFragment : public FMassFragment
{
    GENERATED_BODY()

    // Explosion radius
    UPROPERTY()
    float ExplosionRadius = 200.0f;

    // Explosion damage
    UPROPERTY()
    float ExplosionDamage = 50.0f;

    // Damage falloff (linear, squared, none)
    UPROPERTY()
    EDamageFalloff DamageFalloff = EDamageFalloff::Linear;

    // Trigger conditions
    UPROPERTY()
    bool bExplodeOnDeath = true;

    UPROPERTY()
    bool bExplodeOnContact = false;

    // Optional: Delay before explosion
    UPROPERTY()
    float ExplosionDelay = 0.0f;

    // Timer for delay
    UPROPERTY()
    float ExplosionDelayTimer = 0.0f;

    // Visual/audio
    UPROPERTY()
    TObjectPtr<UNiagaraSystem> ExplosionVFX = nullptr;

    UPROPERTY()
    TObjectPtr<USoundBase> ExplosionSound = nullptr;

    // Has exploded?
    UPROPERTY()
    bool bHasExploded = false;
};

UENUM()
enum class EDamageFalloff : uint8
{
    None,          // Full damage in radius
    Linear,        // Linear falloff to edge
    Squared        // Quadratic falloff
};
```

**Processor:** `UMassExploderProcessor` (Section 6)

---

### 3.4 FClonerFragment

**Purpose:** Duplicate self without dying.

**Declaration:**
```cpp
// ClonerFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "ClonerFragment.generated.h"

/**
 * Duplicates itself (splits without dying).
 * Used by: Multiplying enemies, cloning projectiles.
 */
USTRUCT()
struct LAMENT_API FClonerFragment : public FMassFragment
{
    GENERATED_BODY()

    // What to clone into (usually self archetype)
    UPROPERTY()
    TObjectPtr<const UEntityArchetype> CloneArchetype = nullptr;

    // How many clones to create
    UPROPERTY()
    int32 CloneCount = 1;

    // Clone interval
    UPROPERTY()
    float CloneInterval = 5.0f;

    // Time since last clone
    UPROPERTY()
    float TimeSinceLastClone = 0.0f;

    // Max total clones (-1 = infinite)
    UPROPERTY()
    int32 MaxTotalClones = -1;

    // Current clone count
    UPROPERTY()
    int32 CurrentCloneCount = 0;

    // Clone offset distance
    UPROPERTY()
    float CloneOffsetDistance = 50.0f;

    // Clone health (percentage of original, -1 = same)
    UPROPERTY()
    float CloneHealthMultiplier = 1.0f;
};
```

**Processor:** `UMassClonerProcessor`

---

### 3.5 FForcerFragment

**Purpose:** Apply force to player/entities.

**Declaration:**
```cpp
// ForcerFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "ForcerFragment.generated.h"

/**
 * Applies movement force to hit targets.
 * Used by: Wind blasts, pushback attacks, knockback.
 */
USTRUCT()
struct LAMENT_API FForcerFragment : public FMassFragment
{
    GENERATED_BODY()

    // Force magnitude
    UPROPERTY()
    float ForceMagnitude = 500.0f;

    // Force direction (relative to entity or absolute)
    UPROPERTY()
    FVector ForceDirection = FVector::ForwardVector;

    // Is direction relative to entity rotation?
    UPROPERTY()
    bool bRelativeDirection = true;

    // Apply continuously or on hit only?
    UPROPERTY()
    bool bApplyOnHitOnly = true;

    // Can affect other entities (not just player)?
    UPROPERTY()
    bool bAffectEntities = false;

    // Force application type
    UPROPERTY()
    EForceType ForceType = EForceType::Impulse;
};

UENUM()
enum class EForceType : uint8
{
    Impulse,       // Instant force
    Continuous,    // Applied each frame
    Velocity       // Set velocity directly
};
```

**Processor:** `UMassForceProcessor` (Section 8)

---

### 3.6 Additional Ability Fragments (Brief)

**FGrowerFragment** - Increase size over time
**FShrinkerFragment** - Decrease size over time
**FCarrierFragment** - Grab and carry player/objects
**FThrowerFragment** - Throw held objects
**FMorpherFragment** - Transform into different entity
**FSapperFragment** - Reduce player stats
**FLatcherFragment** - Attach to player and drain
**FHiderFragment** - Hide based on conditions
**FSwitcherFragment** - Toggle between attribute sets
**FInteractorFragment** - Activate level mechanisms
**FChargerFragment** - Wind-up before actions

**See `MassEntity_AttributeReference.md` for complete declarations.**

---

## 4. Combat Processors

### 4.1 UMassHealthProcessor

**Purpose:** Manage health, damage, and death.

**Declaration:**
```cpp
// MassHealthProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassHealthProcessor.generated.h"

/**
 * Handles health updates, damage application, and death.
 * Integrates with quality attributes (Invulnerable, Regenerator, etc.).
 * 
 * Execution Order: Late (after collision, before abilities)
 */
UCLASS()
class LAMENT_API UMassHealthProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassHealthProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    // Apply damage to entity
    void ApplyDamage(FMassEntityHandle Entity,
                    float Damage,
                    const FGameplayTag& DamageType,
                    FMassEntityManager& EntityManager) const;
    
    // Check if entity should block damage
    bool ShouldBlockDamage(FMassEntityHandle Entity,
                          const FVector& HitLocation,
                          const FVector& HitDirection,
                          FMassEntityManager& EntityManager) const;
};
```

**Implementation (Simplified):**
```cpp
// MassHealthProcessor.cpp
#include "MassHealthProcessor.h"
#include "MassCommonFragments.h"

UMassHealthProcessor::UMassHealthProcessor()
{
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Tasks;
    ExecutionOrder.ExecuteAfter.Add(TEXT("Collision"));
}

void UMassHealthProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FHealthFragment>(EMassFragmentAccess::ReadWrite);
}

void UMassHealthProcessor::Execute(FMassEntityManager& EntityManager, 
                                    FMassExecutionContext& Context)
{
    const float DeltaTime = Context.GetDeltaTimeSeconds();
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [DeltaTime](FMassExecutionContext& Context)
        {
            TArrayView<FHealthFragment> HealthFragments = Context.GetMutableFragmentView<FHealthFragment>();
            
            for (int32 i = 0; i < Context.GetNumEntities(); ++i)
            {
                FHealthFragment& Health = HealthFragments[i];
                
                // Skip dead entities
                if (Health.bIsDead)
                    continue;
                
                // Update invulnerability timer
                if (Health.InvulnerabilityTimeRemaining > 0.0f)
                {
                    Health.InvulnerabilityTimeRemaining -= DeltaTime;
                }
                
                // Process regeneration (see FRegeneratorFragment)
                // PRODUCTION NOTE: Check for FRegeneratorFragment and apply regen
                
                // Check death
                if (Health.CurrentHealth <= 0.0f)
                {
                    Health.bIsDead = true;
                    Health.CurrentHealth = 0.0f;
                    
                    // Trigger death abilities (Exploder, Splitter)
                    // PRODUCTION NOTE: Add death trigger to FTriggerStateFragment
                }
            }
        });
}
```

---

## 5. Full Implementation: Emitter System

Spawning other entities at intervals (turrets, shooters, spawners).

### 5.1 Fragment (Section 3.1)

### 5.2 Processor Declaration

```cpp
// MassEmitterProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassEmitterProcessor.generated.h"

/**
 * Spawns entities from FEmitterFragment.
 * Handles intervals, burst fire, and auto-aiming.
 * 
 * Execution Order: Default (after movement)
 */
UCLASS()
class LAMENT_API UMassEmitterProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassEmitterProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    // Spawn single emitted entity
    void SpawnEmittedEntity(const FEmitterFragment& Emitter,
                           const FTransformFragment& EmitterTransform,
                           const FVector& EmitDirection,
                           UWorld* World) const;
    
    // Get aim direction (auto-aim if enabled)
    FVector GetEmitDirection(const FEmitterFragment& Emitter,
                            const FTransformFragment& EmitterTransform,
                            UWorld* World) const;
};
```

### 5.3 Processor Implementation

```cpp
// MassEmitterProcessor.cpp
#include "MassEmitterProcessor.h"
#include "MassCommonFragments.h"
#include "LamentEntitySpawner.h"

UMassEmitterProcessor::UMassEmitterProcessor()
{
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Tasks;
}

void UMassEmitterProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadOnly);
    EntityQuery.AddRequirement<FEmitterFragment>(EMassFragmentAccess::ReadWrite);
}

void UMassEmitterProcessor::Execute(FMassEntityManager& EntityManager, 
                                     FMassExecutionContext& Context)
{
    UWorld* World = Context.GetWorld();
    if (!World) return;
    
    ULamentEntitySpawner* Spawner = World->GetSubsystem<ULamentEntitySpawner>();
    if (!Spawner) return;
    
    const float DeltaTime = Context.GetDeltaTimeSeconds();
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [DeltaTime, World, Spawner, this](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            
            TConstArrayView<FTransformFragment> Transforms = Context.GetFragmentView<FTransformFragment>();
            TArrayView<FEmitterFragment> Emitters = Context.GetMutableFragmentView<FEmitterFragment>();
            
            for (int32 i = 0; i < NumEntities; ++i)
            {
                const FTransformFragment& Transform = Transforms[i];
                FEmitterFragment& Emitter = Emitters[i];
                
                // Skip if no archetype set
                if (!Emitter.EmittedArchetype)
                    continue;
                
                // Check emission limit
                if (Emitter.MaxEmissions > 0 && Emitter.EmissionsRemaining <= 0)
                    continue;
                
                // Update timer
                Emitter.TimeSinceLastEmit += DeltaTime;
                
                // Check if time to emit
                if (Emitter.TimeSinceLastEmit >= Emitter.EmitInterval)
                {
                    Emitter.TimeSinceLastEmit = 0.0f;
                    
                    // Get base emit direction
                    FVector BaseDirection = GetEmitDirection(Emitter, Transform, World);
                    
                    // Spawn burst
                    for (int32 BurstIndex = 0; BurstIndex < Emitter.BurstCount; ++BurstIndex)
                    {
                        FVector EmitDirection = BaseDirection;
                        
                        // Apply burst spread
                        if (Emitter.BurstCount > 1)
                        {
                            float SpreadAngle = Emitter.BurstSpreadAngle;
                            float AngleStep = (SpreadAngle * 2.0f) / (Emitter.BurstCount - 1);
                            float CurrentAngle = -SpreadAngle + (AngleStep * BurstIndex);
                            
                            FRotator SpreadRotation(CurrentAngle, 0, 0);
                            EmitDirection = SpreadRotation.RotateVector(BaseDirection);
                        }
                        
                        // Spawn entity
                        SpawnEmittedEntity(Emitter, Transform, EmitDirection, World);
                    }
                    
                    // Update emission count
                    if (Emitter.MaxEmissions > 0)
                    {
                        Emitter.EmissionsRemaining--;
                    }
                }
            }
        });
}

void UMassEmitterProcessor::SpawnEmittedEntity(const FEmitterFragment& Emitter,
                                                const FTransformFragment& EmitterTransform,
                                                const FVector& EmitDirection,
                                                UWorld* World) const
{
    ULamentEntitySpawner* Spawner = World->GetSubsystem<ULamentEntitySpawner>();
    if (!Spawner) return;
    
    // Calculate spawn transform
    FVector SpawnLocation = EmitterTransform.GetLocation() + 
                           EmitterTransform.Transform.TransformVector(Emitter.EmitOffset);
    
    FRotator SpawnRotation = EmitDirection.Rotation();
    FTransform SpawnTransform(SpawnRotation, SpawnLocation);
    
    // Calculate velocity
    FVector EmitVelocity = EmitDirection.GetSafeNormal() * Emitter.EmitSpeed;
    
    // Spawn
    FMassEntityHandle NewEntity = Spawner->SpawnEntity(
        Emitter.EmittedArchetype,
        SpawnTransform,
        EmitVelocity
    );
}

FVector UMassEmitterProcessor::GetEmitDirection(const FEmitterFragment& Emitter,
                                                 const FTransformFragment& EmitterTransform,
                                                 UWorld* World) const
{
    if (Emitter.bAimAtPlayer)
    {
        // PRODUCTION NOTE: Get player location from world subsystem
        FVector PlayerLocation = FVector::ZeroVector; // Placeholder
        FVector ToPlayer = PlayerLocation - EmitterTransform.GetLocation();
        return ToPlayer.GetSafeNormal();
    }
    else
    {
        // Use configured emit direction
        return EmitterTransform.Transform.TransformVector(Emitter.EmitDirection);
    }
}
```

### 5.4 Usage Example

```cpp
// Crystal Sentinel - Stationary turret that fires projectiles

Fragments:
  - EmitterConfig:
      EmittedArchetype: DA_SimpleBullet
      EmitInterval: 3.0
      BurstCount: 3
      BurstSpreadAngle: 15.0
      bAimAtPlayer: true
      EmitSpeed: 600

Result: Every 3 seconds, fires 3 bullets in a spread pattern at player
```

---

## 6. Full Implementation: Exploder + Splitter System

Combined death abilities: explode AND spawn smaller enemies.

### 6.1 Fragments (Sections 3.2, 3.3)

### 6.2 Processor Declarations

```cpp
// MassExploderProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassExploderProcessor.generated.h"

UCLASS()
class LAMENT_API UMassExploderProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassExploderProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    void TriggerExplosion(FMassEntityHandle Entity,
                         FExploderFragment& Exploder,
                         const FTransformFragment& Transform,
                         UWorld* World) const;
    
    void ApplyExplosionDamage(const FVector& ExplosionCenter,
                             float Radius,
                             float Damage,
                             EDamageFalloff Falloff,
                             UWorld* World) const;
};

// MassSplitterProcessor.h
UCLASS()
class LAMENT_API UMassSplitterProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassSplitterProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    void TriggerSplit(const FSplitterFragment& Splitter,
                     const FTransformFragment& Transform,
                     UWorld* World) const;
};
```

### 6.3 Exploder Implementation

```cpp
// MassExploderProcessor.cpp
#include "MassExploderProcessor.h"
#include "MassCommonFragments.h"
#include "NiagaraFunctionLibrary.h"
#include "Kismet/GameplayStatics.h"

UMassExploderProcessor::UMassExploderProcessor()
{
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Tasks;
    ExecutionOrder.ExecuteAfter.Add(TEXT("Health"));
}

void UMassExploderProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadOnly);
    EntityQuery.AddRequirement<FExploderFragment>(EMassFragmentAccess::ReadWrite);
    
    // Optional: Check for death
    EntityQuery.AddRequirement<FHealthFragment>(EMassFragmentAccess::ReadOnly);
}

void UMassExploderProcessor::Execute(FMassEntityManager& EntityManager, 
                                      FMassExecutionContext& Context)
{
    UWorld* World = Context.GetWorld();
    if (!World) return;
    
    const float DeltaTime = Context.GetDeltaTimeSeconds();
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [DeltaTime, World, this](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            
            TConstArrayView<FTransformFragment> Transforms = Context.GetFragmentView<FTransformFragment>();
            TArrayView<FExploderFragment> Exploders = Context.GetMutableFragmentView<FExploderFragment>();
            TConstArrayView<FHealthFragment> HealthFragments = Context.GetFragmentView<FHealthFragment>();
            
            for (int32 i = 0; i < NumEntities; ++i)
            {
                const FTransformFragment& Transform = Transforms[i];
                FExploderFragment& Exploder = Exploders[i];
                const FHealthFragment& Health = HealthFragments[i];
                
                // Skip if already exploded
                if (Exploder.bHasExploded)
                    continue;
                
                bool bShouldExplode = false;
                
                // Check death trigger
                if (Exploder.bExplodeOnDeath && Health.bIsDead)
                {
                    bShouldExplode = true;
                }
                
                // Check contact trigger (handled by collision processor)
                // PRODUCTION NOTE: Collision processor sets flag
                
                // Handle explosion delay
                if (Exploder.ExplosionDelay > 0.0f && bShouldExplode)
                {
                    Exploder.ExplosionDelayTimer += DeltaTime;
                    if (Exploder.ExplosionDelayTimer >= Exploder.ExplosionDelay)
                    {
                        bShouldExplode = true;
                    }
                    else
                    {
                        bShouldExplode = false; // Wait for timer
                    }
                }
                
                // Trigger explosion
                if (bShouldExplode)
                {
                    FMassEntityHandle Entity = Context.GetEntity(i);
                    TriggerExplosion(Entity, Exploder, Transform, World);
                }
            }
        });
}

void UMassExploderProcessor::TriggerExplosion(FMassEntityHandle Entity,
                                               FExploderFragment& Exploder,
                                               const FTransformFragment& Transform,
                                               UWorld* World) const
{
    Exploder.bHasExploded = true;
    
    FVector ExplosionCenter = Transform.GetLocation();
    
    // Spawn VFX
    if (Exploder.ExplosionVFX)
    {
        UNiagaraFunctionLibrary::SpawnSystemAtLocation(
            World,
            Exploder.ExplosionVFX,
            ExplosionCenter
        );
    }
    
    // Play sound
    if (Exploder.ExplosionSound)
    {
        UGameplayStatics::PlaySoundAtLocation(
            World,
            Exploder.ExplosionSound,
            ExplosionCenter
        );
    }
    
    // Apply damage
    ApplyExplosionDamage(
        ExplosionCenter,
        Exploder.ExplosionRadius,
        Exploder.ExplosionDamage,
        Exploder.DamageFalloff,
        World
    );
}

void UMassExploderProcessor::ApplyExplosionDamage(const FVector& ExplosionCenter,
                                                   float Radius,
                                                   float Damage,
                                                   EDamageFalloff Falloff,
                                                   UWorld* World) const
{
    // PRODUCTION NOTE: Use overlap sphere to find affected entities
    TArray<FOverlapResult> Overlaps;
    FCollisionQueryParams QueryParams;
    
    World->OverlapMultiByChannel(
        Overlaps,
        ExplosionCenter,
        FQuat::Identity,
        ECC_Pawn,
        FCollisionShape::MakeSphere(Radius),
        QueryParams
    );
    
    for (const FOverlapResult& Overlap : Overlaps)
    {
        AActor* HitActor = Overlap.GetActor();
        if (!HitActor) continue;
        
        // Calculate damage based on distance
        float Distance = FVector::Dist(ExplosionCenter, HitActor->GetActorLocation());
        float DamageMultiplier = 1.0f;
        
        switch (Falloff)
        {
            case EDamageFalloff::None:
                DamageMultiplier = 1.0f;
                break;
            case EDamageFalloff::Linear:
                DamageMultiplier = 1.0f - (Distance / Radius);
                break;
            case EDamageFalloff::Squared:
                DamageMultiplier = FMath::Square(1.0f - (Distance / Radius));
                break;
        }
        
        float FinalDamage = Damage * DamageMultiplier;
        
        // Apply damage (use Unreal's damage system)
        UGameplayStatics::ApplyDamage(
            HitActor,
            FinalDamage,
            nullptr,
            nullptr,
            UDamageType::StaticClass()
        );
    }
}
```

### 6.4 Splitter Implementation

```cpp
// MassSplitterProcessor.cpp
#include "MassSplitterProcessor.h"
#include "MassCommonFragments.h"
#include "LamentEntitySpawner.h"

UMassSplitterProcessor::UMassSplitterProcessor()
{
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Tasks;
    ExecutionOrder.ExecuteAfter.Add(TEXT("Exploder")); // Split after explosion
}

void UMassSplitterProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadOnly);
    EntityQuery.AddRequirement<FSplitterFragment>(EMassFragmentAccess::ReadWrite);
    EntityQuery.AddRequirement<FHealthFragment>(EMassFragmentAccess::ReadOnly);
}

void UMassSplitterProcessor::Execute(FMassEntityManager& EntityManager, 
                                      FMassExecutionContext& Context)
{
    UWorld* World = Context.GetWorld();
    if (!World) return;
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [World, this](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            
            TConstArrayView<FTransformFragment> Transforms = Context.GetFragmentView<FTransformFragment>();
            TArrayView<FSplitterFragment> Splitters = Context.GetMutableFragmentView<FSplitterFragment>();
            TConstArrayView<FHealthFragment> HealthFragments = Context.GetFragmentView<FHealthFragment>();
            
            for (int32 i = 0; i < NumEntities; ++i)
            {
                const FTransformFragment& Transform = Transforms[i];
                FSplitterFragment& Splitter = Splitters[i];
                const FHealthFragment& Health = HealthFragments[i];
                
                // Skip if already split
                if (Splitter.bHasSplit)
                    continue;
                
                bool bShouldSplit = false;
                
                // Check triggers
                if (Splitter.bSplitOnDeath && Health.bIsDead)
                {
                    bShouldSplit = true;
                }
                
                if (Splitter.bSplitOnHit)
                {
                    // PRODUCTION NOTE: Check hit event from collision
                }
                
                if (bShouldSplit)
                {
                    TriggerSplit(Splitter, Transform, World);
                    Splitter.bHasSplit = true;
                }
            }
        });
}

void UMassSplitterProcessor::TriggerSplit(const FSplitterFragment& Splitter,
                                          const FTransformFragment& Transform,
                                          UWorld* World) const
{
    ULamentEntitySpawner* Spawner = World->GetSubsystem<ULamentEntitySpawner>();
    if (!Spawner || !Splitter.SplitArchetype) return;
    
    FVector SplitCenter = Transform.GetLocation();
    
    for (int32 i = 0; i < Splitter.SplitCount; ++i)
    {
        FVector SplitDirection;
        
        switch (Splitter.SplitPattern)
        {
            case ESplitPattern::Radial:
            {
                // Evenly spaced circle
                float Angle = (360.0f / Splitter.SplitCount) * i;
                FRotator Rotation(0, Angle, 0);
                SplitDirection = Rotation.RotateVector(FVector::ForwardVector);
                break;
            }
            
            case ESplitPattern::Random:
            {
                SplitDirection = FMath::VRand();
                SplitDirection.Z = FMath::Abs(SplitDirection.Z); // Bias upward
                break;
            }
            
            case ESplitPattern::Forward:
            {
                FRotator BaseRotation = Transform.GetRotation();
                float SpreadAngle = 45.0f;
                FRotator Spread(
                    FMath::FRandRange(-SpreadAngle, SpreadAngle),
                    FMath::FRandRange(-SpreadAngle, SpreadAngle),
                    0
                );
                SplitDirection = (BaseRotation + Spread).Vector();
                break;
            }
            
            case ESplitPattern::Upward:
            {
                SplitDirection = FVector::UpVector;
                SplitDirection += FVector(
                    FMath::FRandRange(-0.5f, 0.5f),
                    FMath::FRandRange(-0.5f, 0.5f),
                    0
                );
                SplitDirection.Normalize();
                break;
            }
        }
        
        FVector SplitVelocity = SplitDirection * Splitter.SplitVelocity;
        FTransform SpawnTransform(SplitDirection.Rotation(), SplitCenter);
        
        Spawner->SpawnEntity(
            Splitter.SplitArchetype,
            SpawnTransform,
            SplitVelocity
        );
    }
}
```

### 6.5 Combined Usage: Plague Carrier

```cpp
// Plague Carrier - Explodes AND splits into mini enemies on death

Fragments:
  - HealthConfig:
      MaxHealth: 60
  
  - ExploderConfig:
      ExplosionRadius: 150
      ExplosionDamage: 20
      bExplodeOnDeath: true
      ExplosionVFX: NS_PlagueExplosion
  
  - SplitterConfig:
      SplitArchetype: DA_MiniPlagueCarrier
      SplitCount: 3
      SplitVelocity: 300
      SplitPattern: Radial
      bSplitOnDeath: true

Result: When killed, explodes (damages player) AND spawns 3 smaller enemies
```

---

## 7. Collision System

*(Brief overview - see Core Architecture for UMassSimpleCollisionProcessor)*

### 7.1 Collision with Quality Attributes

```cpp
// Enhanced collision check integrating quality attributes

bool UMassSimpleCollisionProcessor::ProcessCollision(
    FMassEntityHandle ProjectileEntity,
    FMassEntityHandle HitEntity,
    const FVector& HitLocation,
    const FVector& HitDirection,
    FMassEntityManager& EntityManager) const
{
    // 1. Check Invulnerable
    if (EntityManager.HasFragment<FInvulnerableFragment>(HitEntity))
    {
        return false; // No damage
    }
    
    // 2. Check Shielder
    if (const FShielderFragment* Shield = EntityManager.GetFragmentDataPtr<FShielderFragment>(HitEntity))
    {
        // Calculate hit angle
        FVector ShieldDir = Shield->ShieldDirection;
        if (Shield->bRotatesWithEntity)
        {
            const FTransformFragment* Transform = EntityManager.GetFragmentDataPtr<FTransformFragment>(HitEntity);
            ShieldDir = Transform->Transform.TransformVector(Shield->ShieldDirection);
        }
        
        float HitAngle = FMath::RadiansToDegrees(FMath::Acos(FVector::DotProduct(-HitDirection, ShieldDir)));
        
        if (HitAngle <= Shield->ShieldArc / 2.0f)
        {
            return false; // Blocked by shield
        }
    }
    
    // 3. Check SecretSpot
    if (const FSecretSpotFragment* SecretSpot = EntityManager.GetFragmentDataPtr<FSecretSpotFragment>(HitEntity))
    {
        const FTransformFragment* Transform = EntityManager.GetFragmentDataPtr<FTransformFragment>(HitEntity);
        FVector WeakSpotWorld = Transform->GetLocation() + 
                               Transform->Transform.TransformVector(SecretSpot->WeakSpotOffset);
        
        float DistanceToWeakSpot = FVector::Dist(HitLocation, WeakSpotWorld);
        
        if (DistanceToWeakSpot > SecretSpot->WeakSpotRadius)
        {
            return false; // Didn't hit weak spot
        }
        // Apply damage multiplier
        Damage *= SecretSpot->WeakSpotDamageMultiplier;
    }
    
    // 4. Check Deflector
    if (const FDeflectorFragment* Deflector = EntityManager.GetFragmentDataPtr<FDeflectorFragment>(HitEntity))
    {
        // Deflect projectile instead of destroying
        DeflectProjectile(ProjectileEntity, HitDirection, Deflector, EntityManager);
        return false; // No damage to entity
    }
    
    // 5. Apply damage
    ApplyDamageToEntity(HitEntity, Damage, EntityManager);
    return true;
}
```

---

## 8. Force Application & Pushback

Lightweight force system without Chaos physics.

### 8.1 FForceApplicationFragment (Section 3.5)

### 8.2 UMassForceProcessor

```cpp
// MassForceProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassForceProcessor.generated.h"

UCLASS()
class LAMENT_API UMassForceProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassForceProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    void ApplyForceToCharacter(ACharacter* Character,
                              const FVector& Force,
                              EForceType ForceType) const;
};
```

```cpp
// MassForceProcessor.cpp
#include "MassForceProcessor.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"

UMassForceProcessor::UMassForceProcessor()
{
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Tasks;
    ExecutionOrder.ExecuteAfter.Add(TEXT("Collision"));
}

void UMassForceProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadOnly);
    EntityQuery.AddRequirement<FForcerFragment>(EMassFragmentAccess::ReadWrite);
}

void UMassForceProcessor::Execute(FMassEntityManager& EntityManager, 
                                   FMassExecutionContext& Context)
{
    // PRODUCTION NOTE: Get list of characters hit this frame from collision processor
    // For now, simplified implementation
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [this](FMassExecutionContext& Context)
        {
            TConstArrayView<FTransformFragment> Transforms = Context.GetFragmentView<FTransformFragment>();
            TArrayView<FForcerFragment> Forcers = Context.GetMutableFragmentView<FForcerFragment>();
            
            for (int32 i = 0; i < Context.GetNumEntities(); ++i)
            {
                const FTransformFragment& Transform = Transforms[i];
                const FForcerFragment& Forcer = Forcers[i];
                
                // Calculate force vector
                FVector ForceDirection = Forcer.ForceDirection;
                if (Forcer.bRelativeDirection)
                {
                    ForceDirection = Transform.Transform.TransformVector(ForceDirection);
                }
                ForceDirection.Normalize();
                
                FVector ForceVector = ForceDirection * Forcer.ForceMagnitude;
                
                // Apply to hit characters
                // PRODUCTION NOTE: Get from collision data
            }
        });
}

void UMassForceProcessor::ApplyForceToCharacter(ACharacter* Character,
                                                 const FVector& Force,
                                                 EForceType ForceType) const
{
    if (!Character) return;
    
    UCharacterMovementComponent* Movement = Character->GetCharacterMovement();
    if (!Movement) return;
    
    switch (ForceType)
    {
        case EForceType::Impulse:
            // Instant impulse (knockback)
            Character->LaunchCharacter(Force, true, true);
            break;
        
        case EForceType::Continuous:
            // Applied each frame (wind, conveyor)
            Movement->AddForce(Force);
            break;
        
        case EForceType::Velocity:
            // Set velocity directly
            Movement->Velocity = Force;
            break;
    }
}
```

### 8.3 Usage Examples

**Knockback on hit:**
```cpp
FForcerFragment:
  ForceMagnitude: 500
  ForceDirection: Forward
  bRelativeDirection: true
  bApplyOnHitOnly: true
  ForceType: Impulse
```

**Wind zone (continuous push):**
```cpp
FForcerFragment:
  ForceMagnitude: 200
  ForceDirection: (1, 0, 0)
  bRelativeDirection: false
  bApplyOnHitOnly: false
  ForceType: Continuous
```

---

## 9. Complete Entity Examples

### 9.1 Homing Missile (Tier 2)

**Design:**
- Starts moving straight
- After 0.5s, homes in on player
- Explodes on impact

**Fragments:**
```cpp
- FTransformFragment
- FVelocityFragment (initial straight movement)
- FLinerFragment (state 0)
- FFollowerFragment (state 1)
- FExploderFragment
- FProjectileDataFragment
- FTriggerStateFragment
- FNiagaraVFXFragment
```

**Trigger Setup:**
```
State 0 "Launch":
  ProcessorTags: [ActiveLinerTag]
  Triggers:
    - Timer > 0.5 → State 1

State 1 "Homing":
  ProcessorTags: [ActiveFollowerTag]
  Triggers:
    - OnHit → Explode
```

**Configuration:**
```cpp
LinerConfig:
  Direction: Forward
  Speed: 400

FollowerConfig:
  FollowSpeed: 600
  TurnRate: 270
  bPredictTargetMovement: true

ExploderConfig:
  ExplosionRadius: 150
  ExplosionDamage: 30
  bExplodeOnContact: true
  ExplosionVFX: NS_MissileExplosion
```

---

### 9.2 Splitting Bomb (Tier 2)

**Design:**
- Floats in wave pattern
- After 2s OR on hit, explodes
- Spawns 5 bullets in radial pattern
- Pushes player back

**Fragments:**
```cpp
- FWaverFragment
- FExploderFragment
- FSplitterFragment
- FForcerFragment
- FTriggerStateFragment
```

**Configuration:**
```cpp
WaverConfig:
  WaveFrequency: 2.0
  WaveAmplitude: 30
  ForwardSpeed: 200

ExploderConfig:
  ExplosionRadius: 100
  ExplosionDamage: 20
  bExplodeOnDeath: true

SplitterConfig:
  SplitArchetype: DA_SimpleBullet
  SplitCount: 5
  SplitPattern: Radial
  SplitVelocity: 400
  bSplitOnDeath: true

ForcerConfig:
  ForceMagnitude: 800
  ForceDirection: (0, 0, 0) // Radial from explosion
  ForceType: Impulse
```

**Trigger:**
```
State 0 "Active":
  Triggers:
    - Timer > 2.0 → Explode & Split
    - OnHit → Explode & Split
```

---

### 9.3 Plague Carrier (Tier 3)

**(See Section 6.5 for detailed implementation)**

---

## Summary

**What You've Learned:**
- Quality attributes (Shielder, Invulnerable, Deflector, Regenerator, etc.)
- Ability attributes (Emitter, Splitter, Exploder, Cloner, Forcer, etc.)
- Complete Emitter system (turrets, shooters, spawners)
- Complete Exploder + Splitter system (chain reactions)
- Collision integration with quality attributes
- Force application without Chaos physics (lightweight knockback)
- 3 complete entity examples (Homing Missile, Splitting Bomb, Plague Carrier)

**Next Steps:**
- Read `MassEntity_AdvancedSystems.md` for Niagara VFX, perception, optimization
- Read `MassEntity_AttributeReference.md` for complete fragment catalog
- Read `MassEntity_Templates.md` for copy-paste ready code

**Key Takeaways:**
- Quality = Defensive/Passive, Ability = Offensive/Active
- Combine Exploder + Splitter for complex death behaviors
- Force application uses Character Movement Component (no physics overhead)
- Collision system integrates all quality attributes for rich interactions

---

**Document Version:** 1.0  
**Last Updated:** December 2024  
**UE Version:** 5.7+
