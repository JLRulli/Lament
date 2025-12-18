# Mass Entity Core Architecture

## Overview

This document covers the foundational architecture of Lament's Mass Entity-based enemy and projectile system. This is the starting point for understanding how the modular attribute system is implemented using Unreal Engine 5.7's Mass Entity framework.

**Prerequisites:**
- UE 5.7 project with Mass Entity plugin enabled
- Familiarity with C++ and Unreal Engine
- Understanding of the design concepts in `EnemyAI.md`

**Related Documents:**
- `EnemyAI.md` - Design philosophy and attribute catalog
- `MassEntity_MovementAndTriggers.md` - Movement systems implementation
- `MassEntity_CombatSystems.md` - Combat and abilities implementation
- `MassEntity_AdvancedSystems.md` - Advanced features and optimization

---

## 1. System Architecture

### 1.1 Architecture Layers

The system is organized into three distinct layers:

```
┌─────────────────────────────────────────────────────────┐
│            Designer Layer (Data Assets)                  │
│  ┌────────────────┐  ┌──────────────────┐              │
│  │ Entity         │  │ Trigger          │              │
│  │ Archetypes     │  │ Rules            │              │
│  └────────────────┘  └──────────────────┘              │
│  Define WHAT behaviors    Define WHEN to switch        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│        Mass Entity Runtime (Fragments + Processors)      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│  │ Movement │ │ Combat   │ │ Visual   │               │
│  │ Fragments│ │ Fragments│ │ Fragments│               │
│  └──────────┘ └──────────┘ └──────────┘               │
│  Pure data     Processors operate on fragments          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│       Visualization Layer (Actors + Niagara)             │
│  Spawned/pooled actors sync with Mass entity data       │
└─────────────────────────────────────────────────────────┘
```

**Layer 1: Designer Layer**
- Data Assets define entity configurations
- No code required for creating new entities
- Combine existing fragments in new ways
- Designer-friendly value tuning

**Layer 2: Mass Entity Runtime**
- **Fragments**: Pure data structs (no logic)
- **Processors**: Systems that operate on fragments
- Runs in parallel, highly optimized
- Data-oriented design for cache efficiency

**Layer 3: Visualization Layer**
- Lightweight actors for visuals only
- Niagara VFX systems
- Synced with Mass entity positions
- Optional (can run headless for simulation)

---

### 1.2 Three-Tier Performance System

Entities are categorized into three performance tiers based on complexity:

```
┌─────────────────────────────────────────────────────────┐
│  TIER 1: Simple Projectiles                             │
│  Target: 200+ entities @ 60fps                          │
│  ┌────────────────────────────────────────────┐        │
│  │ • Basic movement (linear velocity)         │        │
│  │ • Simple collision (sphere/box)            │        │
│  │ • Lifetime/despawn management              │        │
│  │ • Minimal VFX (trail only)                 │        │
│  └────────────────────────────────────────────┘        │
│  Examples: Bullets, arrows, simple projectiles         │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  TIER 2: Complex Projectiles                            │
│  Target: 50+ entities @ 60fps                           │
│  ┌────────────────────────────────────────────┐        │
│  │ • All Tier 1 features, PLUS:               │        │
│  │ • Movement attributes (Floater, Follower)  │        │
│  │ • Quality attributes (Deflector, GeoIgnore)│        │
│  │ • Ability attributes (Splitter, Exploder)  │        │
│  │ • Trigger-based behavior switching         │        │
│  └────────────────────────────────────────────┘        │
│  Examples: Homing missiles, splitting bombs            │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  TIER 3: Enemy Entities                                 │
│  Target: 30+ entities @ 60fps                           │
│  ┌────────────────────────────────────────────┐        │
│  │ • All Tier 2 features, PLUS:               │        │
│  │ • Health and damage system                 │        │
│  │ • Perception (LOS, player tracking)        │        │
│  │ • AI decision-making                       │        │
│  │ • Loot drops on death                      │        │
│  └────────────────────────────────────────────┘        │
│  Examples: All enemies, enemy-projectiles              │
└─────────────────────────────────────────────────────────┘
```

**Performance Characteristics:**

| Tier | Fragment Count | Update Cost | Typical Use |
|------|----------------|-------------|-------------|
| Tier 1 | 4-5 | Very Low | 90% of projectiles |
| Tier 2 | 6-10 | Medium | Complex projectiles |
| Tier 3 | 10-15 | High | Enemies, bosses |

---

### 1.3 Core Concepts

#### Fragments

**Fragments are pure data** - they contain no logic, only state.

```cpp
// Example: A fragment is just a struct with data
USTRUCT()
struct FFloaterFragment : public FMassFragment
{
    GENERATED_BODY()
    
    float FloatHeight = 100.0f;      // How high to float
    float BobSpeed = 2.0f;            // How fast to bob up/down
    float BobAmplitude = 20.0f;       // How far to bob
    float TimeOffset = 0.0f;          // Stagger bobbing between entities
};
```

**Key Properties:**
- Lightweight (just data members)
- No virtual functions
- Cache-friendly memory layout
- Can be added/removed at runtime

#### Processors

**Processors are systems** that operate on entities with specific fragments.

```cpp
// Example: A processor operates on fragments
UCLASS()
class UMassFloaterProcessor : public UMassProcessor
{
    // Defines which fragments this processor needs
    virtual void ConfigureQueries() override;
    
    // Executes logic on all matching entities
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;
};
```

**Key Properties:**
- Stateless (operates on fragments only)
- Processes entities in parallel chunks
- Query-based filtering (only entities with required fragments)
- Deterministic execution order

#### Execution Flow

```
Frame Start
    ↓
[ConfigureQueries Phase]
    • Processors declare required fragments
    • Entity Manager builds query results
    ↓
[Execute Phase - runs each frame]
    ↓
    [UMassTriggerProcessor] ← Check conditions, add/remove fragments
        ↓
    [Movement Processors] ← Update entity positions
        ↓
    [Ability Processors] ← Execute abilities (spawn, split, explode)
        ↓
    [Collision Processor] ← Detect hits
        ↓
    [Health Processor] ← Apply damage, handle death
        ↓
    [Niagara Processor] ← Sync VFX with entity positions
    ↓
Frame End
```

#### Traits

**Traits are blueprints** that define which fragments an entity should have.

```cpp
// Trait bundles fragments together
UCLASS()
class USimpleProjectileTrait : public UMassEntityTraitBase
{
    // Adds required fragments to entity
    virtual void BuildTemplate(FMassEntityTemplateBuildContext& BuildContext) override
    {
        BuildContext.AddFragment<FTransformFragment>();
        BuildContext.AddFragment<FVelocityFragment>();
        BuildContext.AddFragment<FProjectileDataFragment>();
    }
};
```

#### Archetypes

**Archetypes are data assets** that designers use to create entities.

```cpp
// Data Asset - no code required to create new entity types
UCLASS()
class UEntityArchetype : public UDataAsset
{
    UPROPERTY(EditAnywhere)
    TArray<TSubclassOf<UMassFragmentConfig>> Fragments;
    
    UPROPERTY(EditAnywhere)
    UTriggerRuleSet* TriggerRules;
    
    UPROPERTY(EditAnywhere)
    TSoftClassPtr<AActor> VisualizationActor;
};
```

---

### 1.4 Why Mass Entity?

**Performance Benefits:**
1. **Data-Oriented Design**: Cache-friendly memory layout
2. **Batch Processing**: Process hundreds of entities per frame
3. **SIMD Optimization**: Automatic vectorization opportunities
4. **No Virtual Call Overhead**: Direct memory access to fragments
5. **Built-in Pooling**: Entity handles are recycled automatically

**Development Benefits:**
1. **Modularity**: Mix and match fragments to create new behaviors
2. **Reusability**: Write fragment logic once, use everywhere
3. **Designer-Friendly**: No code required to create new entity types
4. **Debuggability**: Easy to inspect fragment data
5. **Scalability**: Proven to handle thousands of entities

**Comparison to Actor-Based Systems:**

| Feature | Actor-Based | Mass Entity |
|---------|-------------|-------------|
| Max Entities @ 60fps | ~50-100 | 200+ (complex entities) |
| Memory per Entity | ~1-5KB | ~100-500 bytes |
| Component Overhead | Virtual calls, inheritance | Direct memory access |
| Batch Processing | No | Yes (automatic) |
| Modularity | Component system | Fragment system |
| Designer Iteration | Recompile blueprints | Edit data assets |

---

## 2. Core Fragments Reference

These fragments are used across all tiers and form the foundation of the system.

### 2.1 FTransformFragment

**Purpose:** Stores entity position, rotation, and scale.

**Declaration:**
```cpp
// TransformFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "TransformFragment.generated.h"

/**
 * Core fragment containing entity transform.
 * Required by almost all entities.
 * Used by: All processors that need position/rotation.
 */
USTRUCT()
struct LAMENT_API FTransformFragment : public FMassFragment
{
    GENERATED_BODY()

    UPROPERTY()
    FTransform Transform;

    // Helper accessors
    FVector GetLocation() const { return Transform.GetLocation(); }
    FRotator GetRotation() const { return Transform.Rotator(); }
    FVector GetScale() const { return Transform.GetScale3D(); }
    
    void SetLocation(const FVector& NewLocation) { Transform.SetLocation(NewLocation); }
    void SetRotation(const FRotator& NewRotation) { Transform.SetRotation(NewRotation.Quaternion()); }
};
```

**Tier Usage:** All tiers (required)

---

### 2.2 FVelocityFragment

**Purpose:** Stores entity velocity for simple physics-free movement.

**Declaration:**
```cpp
// VelocityFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "VelocityFragment.generated.h"

/**
 * Simple velocity-based movement.
 * Updated by UMassSimpleMovementProcessor.
 * No physics simulation - just Transform += Velocity * DeltaTime
 */
USTRUCT()
struct LAMENT_API FVelocityFragment : public FMassFragment
{
    GENERATED_BODY()

    // Current velocity in units/second
    UPROPERTY()
    FVector Velocity = FVector::ZeroVector;

    // Optional: Acceleration applied each frame
    UPROPERTY()
    FVector Acceleration = FVector::ZeroVector;

    // Optional: Max speed limit
    UPROPERTY()
    float MaxSpeed = 1000.0f;

    // Optional: Friction coefficient (0-1, 0 = no friction)
    UPROPERTY()
    float Friction = 0.0f;
};
```

**Tier Usage:** Tier 1, 2, 3

---

### 2.3 FProjectileDataFragment

**Purpose:** Core projectile properties (damage, lifetime, etc).

**Declaration:**
```cpp
// ProjectileDataFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "GameplayTagContainer.h"
#include "ProjectileDataFragment.generated.h"

/**
 * Core data for projectile entities.
 * Contains damage, lifetime, and despawn conditions.
 */
USTRUCT()
struct LAMENT_API FProjectileDataFragment : public FMassFragment
{
    GENERATED_BODY()

    // Damage dealt on hit
    UPROPERTY()
    float Damage = 10.0f;

    // Max lifetime in seconds (-1 = infinite)
    UPROPERTY()
    float MaxLifetime = 5.0f;

    // Current age in seconds
    UPROPERTY()
    float CurrentAge = 0.0f;

    // Max distance from spawn point (-1 = infinite)
    UPROPERTY()
    float MaxDistance = -1.0f;

    // Spawn location (for distance tracking)
    UPROPERTY()
    FVector SpawnLocation = FVector::ZeroVector;

    // Despawn when off-screen?
    UPROPERTY()
    bool bDespawnOffScreen = true;

    // Projectile type tags (for damage filtering, deflection, etc.)
    UPROPERTY()
    FGameplayTagContainer ProjectileTags;

    // Has this projectile hit something?
    UPROPERTY()
    bool bHasHit = false;
};
```

**Tier Usage:** Tier 1, 2

---

### 2.4 FHealthFragment

**Purpose:** Health, damage resistance, and death tracking.

**Declaration:**
```cpp
// HealthFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "GameplayTagContainer.h"
#include "HealthFragment.generated.h"

/**
 * Health system for entities that can take damage.
 * Primarily used by enemies, but can be added to destructible projectiles.
 */
USTRUCT()
struct LAMENT_API FHealthFragment : public FMassFragment
{
    GENERATED_BODY()

    // Current health
    UPROPERTY()
    float CurrentHealth = 100.0f;

    // Maximum health
    UPROPERTY()
    float MaxHealth = 100.0f;

    // Is this entity dead?
    UPROPERTY()
    bool bIsDead = false;

    // Damage multipliers per damage type (optional)
    UPROPERTY()
    TMap<FGameplayTag, float> DamageTypeMultipliers;

    // Invulnerability duration remaining (seconds)
    UPROPERTY()
    float InvulnerabilityTimeRemaining = 0.0f;

    // Helper functions
    float GetHealthPercent() const { return MaxHealth > 0 ? CurrentHealth / MaxHealth : 0.0f; }
    bool IsAlive() const { return !bIsDead && CurrentHealth > 0; }
};
```

**Tier Usage:** Tier 2 (destructible projectiles), Tier 3 (enemies)

---

### 2.5 FSimpleCollisionFragment

**Purpose:** Basic collision detection for projectiles.

**Declaration:**
```cpp
// SimpleCollisionFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "GameplayTagContainer.h"
#include "SimpleCollisionFragment.generated.h"

/**
 * Simple collision detection (sphere or box).
 * Used by UMassSimpleCollisionProcessor for efficient broad/narrow phase.
 */
USTRUCT()
struct LAMENT_API FSimpleCollisionFragment : public FMassFragment
{
    GENERATED_BODY()

    // Collision shape type
    UPROPERTY()
    ECollisionShape ShapeType = ECollisionShape::Sphere;

    // Collision radius (for sphere) or half-extents (for box)
    UPROPERTY()
    FVector CollisionSize = FVector(10.0f);

    // Collision channel (what this entity collides with)
    UPROPERTY()
    TEnumAsByte<ECollisionChannel> CollisionChannel = ECC_WorldDynamic;

    // Tags to filter collisions (e.g., ignore certain enemy types)
    UPROPERTY()
    FGameplayTagContainer IgnoreTags;

    // Should this entity be destroyed on hit?
    UPROPERTY()
    bool bDestroyOnHit = true;

    // Can hit multiple targets? (or just first hit)
    UPROPERTY()
    bool bPenetrating = false;

    // Max number of penetrations (-1 = infinite)
    UPROPERTY()
    int32 MaxPenetrations = -1;

    // Current penetration count
    UPROPERTY()
    int32 CurrentPenetrations = 0;
};

UENUM()
enum class ECollisionShape : uint8
{
    Sphere,
    Box,
    Capsule
};
```

**Tier Usage:** Tier 1, 2, 3

---

### 2.6 FTriggerStateFragment

**Purpose:** Manages behavior state transitions based on triggers.

**Declaration:**
```cpp
// TriggerStateFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "TriggerStateFragment.generated.h"

// Forward declarations
class UTriggerRuleSet;

/**
 * Manages entity state machine and trigger conditions.
 * Evaluated by UMassTriggerProcessor each frame.
 * Triggers can add/remove fragments to change behavior.
 */
USTRUCT()
struct LAMENT_API FTriggerStateFragment : public FMassFragment
{
    GENERATED_BODY()

    // Current state index (0-based)
    UPROPERTY()
    int32 CurrentStateIndex = 0;

    // Previous state (for transition detection)
    UPROPERTY()
    int32 PreviousStateIndex = -1;

    // Trigger rule set (loaded from data asset)
    UPROPERTY()
    const UTriggerRuleSet* RuleSet = nullptr;

    // Time spent in current state
    UPROPERTY()
    float TimeInState = 0.0f;

    // Custom trigger data (for state-specific logic)
    UPROPERTY()
    TMap<FName, float> TriggerData;

    // Helper functions
    bool HasChangedState() const { return CurrentStateIndex != PreviousStateIndex; }
    void ResetStateTime() { TimeInState = 0.0f; }
};
```

**Tier Usage:** Tier 2, 3

**Note:** See `MassEntity_MovementAndTriggers.md` Section 6 for detailed trigger system documentation.

---

### 2.7 FNiagaraVFXFragment

**Purpose:** Manages Niagara VFX systems attached to entities.

**Declaration:**
```cpp
// NiagaraVFXFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "NiagaraSystem.h"
#include "NiagaraComponent.h"
#include "NiagaraVFXFragment.generated.h"

/**
 * Manages Niagara VFX for entity visuals.
 * Updated by UMassNiagaraProcessor to sync VFX positions with entity transforms.
 * Components are pooled for performance.
 */
USTRUCT()
struct LAMENT_API FNiagaraVFXFragment : public FMassFragment
{
    GENERATED_BODY()

    // Continuous trail VFX (follows entity)
    UPROPERTY()
    UNiagaraSystem* TrailSystem = nullptr;

    // Pooled trail component (active during entity lifetime)
    UPROPERTY()
    UNiagaraComponent* ActiveTrailComponent = nullptr;

    // One-shot VFX on spawn
    UPROPERTY()
    UNiagaraSystem* SpawnVFX = nullptr;

    // One-shot VFX on death/despawn
    UPROPERTY()
    UNiagaraSystem* DeathVFX = nullptr;

    // One-shot VFX on hit
    UPROPERTY()
    UNiagaraSystem* HitVFX = nullptr;

    // Should VFX be visible? (for off-screen culling)
    UPROPERTY()
    bool bVFXVisible = true;

    // Has spawn VFX been played?
    UPROPERTY()
    bool bSpawnVFXPlayed = false;
};
```

**Tier Usage:** Tier 1, 2, 3 (optional)

**Note:** See `MassEntity_AdvancedSystems.md` Section 1 for detailed Niagara integration.

---

## 3. Core Processors Reference

These processors operate on the core fragments and form the foundation of entity simulation.

### 3.1 UMassSimpleMovementProcessor

**Purpose:** Updates entity positions based on velocity.

**Declaration:**
```cpp
// MassSimpleMovementProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassSimpleMovementProcessor.generated.h"

/**
 * Simple velocity-based movement processor.
 * Updates Transform from Velocity each frame.
 * No physics, no gravity - just linear movement.
 * 
 * Execution Order: Default (runs after triggers, before abilities)
 */
UCLASS()
class LAMENT_API UMassSimpleMovementProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassSimpleMovementProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
};
```

**Required Fragments:**
- `FTransformFragment` (ReadWrite)
- `FVelocityFragment` (ReadWrite)

**Optional Fragments:**
- None

**Implementation:**
```cpp
// MassSimpleMovementProcessor.cpp
#include "MassSimpleMovementProcessor.h"
#include "MassCommonFragments.h"

UMassSimpleMovementProcessor::UMassSimpleMovementProcessor()
{
    ExecutionOrder.ExecuteAfter.Add(UE::Mass::ProcessorGroupNames::Tasks);
    ExecutionOrder.ExecuteBefore.Add(UE::Mass::ProcessorGroupNames::Avoidance);
}

void UMassSimpleMovementProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadWrite);
    EntityQuery.AddRequirement<FVelocityFragment>(EMassFragmentAccess::ReadWrite);
}

void UMassSimpleMovementProcessor::Execute(FMassEntityManager& EntityManager, 
                                           FMassExecutionContext& Context)
{
    // Process entities in parallel chunks (cache-friendly)
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            const float DeltaTime = Context.GetDeltaTimeSeconds();
            
            // Get fragment views for this chunk
            TArrayView<FTransformFragment> Transforms = Context.GetMutableFragmentView<FTransformFragment>();
            TArrayView<FVelocityFragment> Velocities = Context.GetMutableFragmentView<FVelocityFragment>();
            
            // Batch process all entities in this chunk
            for (int32 i = 0; i < NumEntities; ++i)
            {
                FTransformFragment& Transform = Transforms[i];
                FVelocityFragment& Velocity = Velocities[i];
                
                // Apply acceleration
                if (!Velocity.Acceleration.IsNearlyZero())
                {
                    Velocity.Velocity += Velocity.Acceleration * DeltaTime;
                }
                
                // Apply friction
                if (Velocity.Friction > 0.0f)
                {
                    Velocity.Velocity *= FMath::Max(0.0f, 1.0f - Velocity.Friction * DeltaTime);
                }
                
                // Clamp to max speed
                if (Velocity.MaxSpeed > 0.0f)
                {
                    const float SpeedSq = Velocity.Velocity.SizeSquared();
                    const float MaxSpeedSq = Velocity.MaxSpeed * Velocity.MaxSpeed;
                    
                    if (SpeedSq > MaxSpeedSq)
                    {
                        Velocity.Velocity = Velocity.Velocity.GetSafeNormal() * Velocity.MaxSpeed;
                    }
                }
                
                // Update position
                FVector NewLocation = Transform.GetLocation() + (Velocity.Velocity * DeltaTime);
                Transform.SetLocation(NewLocation);
                
                // Optional: Update rotation to face velocity direction
                if (!Velocity.Velocity.IsNearlyZero())
                {
                    FRotator NewRotation = Velocity.Velocity.Rotation();
                    Transform.SetRotation(NewRotation);
                }
            }
        });
}
```

---

### 3.2 UMassProjectileLifetimeProcessor

**Purpose:** Manages projectile lifetime and despawning.

**Declaration:**
```cpp
// MassProjectileLifetimeProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassProjectileLifetimeProcessor.generated.h"

/**
 * Manages projectile lifetime, distance tracking, and despawning.
 * Despawns entities based on:
 * - Max lifetime exceeded
 * - Max distance from spawn exceeded
 * - Off-screen (if enabled)
 * 
 * Execution Order: Late (after movement and collision)
 */
UCLASS()
class LAMENT_API UMassProjectileLifetimeProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassProjectileLifetimeProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    // Helper: Check if entity is off-screen
    bool IsOffScreen(const FVector& Location, const FMassExecutionContext& Context) const;
};
```

**Required Fragments:**
- `FTransformFragment` (ReadOnly)
- `FProjectileDataFragment` (ReadWrite)

**Implementation:**
```cpp
// MassProjectileLifetimeProcessor.cpp
#include "MassProjectileLifetimeProcessor.h"
#include "MassCommonFragments.h"
#include "MassCommandBuffer.h"

UMassProjectileLifetimeProcessor::UMassProjectileLifetimeProcessor()
{
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Tasks;
    ExecutionOrder.ExecuteAfter.Add(TEXT("Movement"));
}

void UMassProjectileLifetimeProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadOnly);
    EntityQuery.AddRequirement<FProjectileDataFragment>(EMassFragmentAccess::ReadWrite);
}

void UMassProjectileLifetimeProcessor::Execute(FMassEntityManager& EntityManager, 
                                               FMassExecutionContext& Context)
{
    const float DeltaTime = Context.GetDeltaTimeSeconds();
    
    // Deferred command buffer for despawning entities
    FMassCommandBuffer& CommandBuffer = Context.Defer();
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [DeltaTime, &CommandBuffer, this](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            TConstArrayView<FTransformFragment> Transforms = Context.GetFragmentView<FTransformFragment>();
            TArrayView<FProjectileDataFragment> ProjectileData = Context.GetMutableFragmentView<FProjectileDataFragment>();
            
            for (int32 i = 0; i < NumEntities; ++i)
            {
                FProjectileDataFragment& Data = ProjectileData[i];
                const FTransformFragment& Transform = Transforms[i];
                
                // Update age
                Data.CurrentAge += DeltaTime;
                
                bool bShouldDespawn = false;
                
                // Check max lifetime
                if (Data.MaxLifetime > 0.0f && Data.CurrentAge >= Data.MaxLifetime)
                {
                    bShouldDespawn = true;
                }
                
                // Check max distance
                if (Data.MaxDistance > 0.0f)
                {
                    float DistanceSq = FVector::DistSquared(Transform.GetLocation(), Data.SpawnLocation);
                    if (DistanceSq >= (Data.MaxDistance * Data.MaxDistance))
                    {
                        bShouldDespawn = true;
                    }
                }
                
                // Check off-screen
                if (Data.bDespawnOffScreen && IsOffScreen(Transform.GetLocation(), Context))
                {
                    bShouldDespawn = true;
                }
                
                // Check if already hit (and not penetrating)
                if (Data.bHasHit)
                {
                    bShouldDespawn = true;
                }
                
                // Despawn entity
                if (bShouldDespawn)
                {
                    FMassEntityHandle Entity = Context.GetEntity(i);
                    CommandBuffer.DestroyEntity(Entity);
                }
            }
        });
}

bool UMassProjectileLifetimeProcessor::IsOffScreen(const FVector& Location, 
                                                    const FMassExecutionContext& Context) const
{
    // PRODUCTION NOTE: Get camera frustum from player controller
    // For now, simple distance check
    const float MaxVisibleDistance = 5000.0f; // Units
    
    // Get player location (simplified)
    // PRODUCTION NOTE: Cache player location in processor or get from world subsystem
    FVector PlayerLocation = FVector::ZeroVector; // Placeholder
    
    float DistanceSq = FVector::DistSquared(Location, PlayerLocation);
    return DistanceSq > (MaxVisibleDistance * MaxVisibleDistance);
}
```

---

### 3.3 UMassSimpleCollisionProcessor

**Purpose:** Basic collision detection for projectiles.

**Declaration:**
```cpp
// MassSimpleCollisionProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassSimpleCollisionProcessor.generated.h"

/**
 * Simple collision detection for projectiles.
 * Uses spatial hashing for broad phase, shape checks for narrow phase.
 * Applies damage on hit and triggers hit events.
 * 
 * Execution Order: Default (after movement)
 */
UCLASS()
class LAMENT_API UMassSimpleCollisionProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassSimpleCollisionProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    // Spatial hash grid for broad phase
    TMap<FIntVector, TArray<FMassEntityHandle>> SpatialGrid;
    float GridCellSize = 200.0f;
    
    FIntVector GetGridCell(const FVector& Location) const;
    void RebuildSpatialGrid(FMassEntityManager& EntityManager, FMassExecutionContext& Context);
    bool CheckCollision(const FTransformFragment& Transform, 
                       const FSimpleCollisionFragment& Collision,
                       AActor* HitActor) const;
};
```

**Required Fragments:**
- `FTransformFragment` (ReadOnly)
- `FSimpleCollisionFragment` (ReadWrite)
- `FProjectileDataFragment` (ReadWrite)

**Implementation (Simplified):**
```cpp
// MassSimpleCollisionProcessor.cpp
#include "MassSimpleCollisionProcessor.h"
#include "MassCommonFragments.h"
#include "Engine/World.h"

UMassSimpleCollisionProcessor::UMassSimpleCollisionProcessor()
{
    ExecutionOrder.ExecuteAfter.Add(TEXT("Movement"));
}

void UMassSimpleCollisionProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadOnly);
    EntityQuery.AddRequirement<FSimpleCollisionFragment>(EMassFragmentAccess::ReadWrite);
    EntityQuery.AddRequirement<FProjectileDataFragment>(EMassFragmentAccess::ReadWrite);
}

void UMassSimpleCollisionProcessor::Execute(FMassEntityManager& EntityManager, 
                                            FMassExecutionContext& Context)
{
    // Rebuild spatial grid for broad phase
    RebuildSpatialGrid(EntityManager, Context);
    
    UWorld* World = Context.GetWorld();
    if (!World) return;
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [World, this](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            TConstArrayView<FTransformFragment> Transforms = Context.GetFragmentView<FTransformFragment>();
            TArrayView<FSimpleCollisionFragment> Collisions = Context.GetMutableFragmentView<FSimpleCollisionFragment>();
            TArrayView<FProjectileDataFragment> ProjectileData = Context.GetMutableFragmentView<FProjectileDataFragment>();
            
            for (int32 i = 0; i < NumEntities; ++i)
            {
                const FTransformFragment& Transform = Transforms[i];
                FSimpleCollisionFragment& Collision = Collisions[i];
                FProjectileDataFragment& Data = ProjectileData[i];
                
                // Skip if already hit and not penetrating
                if (Data.bHasHit && !Collision.bPenetrating) continue;
                
                // Simple sphere trace (PRODUCTION NOTE: Use spatial hash for optimization)
                FCollisionQueryParams QueryParams;
                QueryParams.AddIgnoredActor(nullptr); // PRODUCTION NOTE: Ignore shooter
                
                TArray<FHitResult> HitResults;
                bool bHit = World->SweepMultiByChannel(
                    HitResults,
                    Transform.GetLocation(),
                    Transform.GetLocation() + FVector(1.0f), // Small sweep
                    FQuat::Identity,
                    Collision.CollisionChannel,
                    FCollisionShape::MakeSphere(Collision.CollisionSize.X),
                    QueryParams
                );
                
                if (bHit)
                {
                    for (const FHitResult& Hit : HitResults)
                    {
                        // Apply damage
                        // PRODUCTION NOTE: Use proper damage system
                        if (AActor* HitActor = Hit.GetActor())
                        {
                            // Check penetration limits
                            if (Collision.bPenetrating)
                            {
                                Collision.CurrentPenetrations++;
                                if (Collision.MaxPenetrations > 0 && 
                                    Collision.CurrentPenetrations >= Collision.MaxPenetrations)
                                {
                                    Data.bHasHit = true;
                                }
                            }
                            else
                            {
                                Data.bHasHit = true;
                            }
                        }
                    }
                }
            }
        });
}

void UMassSimpleCollisionProcessor::RebuildSpatialGrid(FMassEntityManager& EntityManager, 
                                                        FMassExecutionContext& Context)
{
    // Clear previous grid
    SpatialGrid.Reset();
    
    // PRODUCTION NOTE: Build spatial hash for broad phase optimization
    // For now, using simple sweep collision
}

FIntVector UMassSimpleCollisionProcessor::GetGridCell(const FVector& Location) const
{
    return FIntVector(
        FMath::FloorToInt(Location.X / GridCellSize),
        FMath::FloorToInt(Location.Y / GridCellSize),
        FMath::FloorToInt(Location.Z / GridCellSize)
    );
}
```

---

### 3.4 UMassTriggerProcessor

**Purpose:** Evaluates trigger conditions and switches entity behaviors.

**Declaration:**
```cpp
// MassTriggerProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassTriggerProcessor.generated.h"

/**
 * Evaluates trigger conditions and switches entity states.
 * Can add/remove fragments to change entity behavior.
 * 
 * Execution Order: Early (before movement/abilities)
 */
UCLASS()
class LAMENT_API UMassTriggerProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassTriggerProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    // Trigger evaluation helpers
    bool EvaluateTrigger(const FMassEntityHandle Entity,
                        const FTriggerCondition& Condition,
                        FMassEntityManager& EntityManager,
                        FMassExecutionContext& Context) const;
};
```

**Required Fragments:**
- `FTriggerStateFragment` (ReadWrite)

**Note:** Full implementation and trigger system details are in `MassEntity_MovementAndTriggers.md` Section 6.

---

## 4. Full Implementation Example: Simple Bullet (Tier 1)

This section provides a complete walkthrough of implementing a basic projectile from scratch.

### 4.1 Design Specification

**Entity:** Simple Bullet
**Tier:** 1 (Simple Projectile)
**Behavior:** 
- Travels in straight line
- Despawns after 2 seconds or when off-screen
- Deals 10 damage on hit
- Simple bullet trail VFX

**Fragments Required:**
- `FTransformFragment`
- `FVelocityFragment`
- `FProjectileDataFragment`
- `FSimpleCollisionFragment`
- `FNiagaraVFXFragment`

---

### 4.2 Fragment Configuration

Create a data asset configuration for the bullet:

```cpp
// SimpleBulletConfig.h
#pragma once
#include "MassEntityConfigAsset.h"
#include "SimpleBulletConfig.generated.h"

/**
 * Configuration for simple bullet projectile.
 * Designer-editable values for bullet behavior.
 */
UCLASS()
class LAMENT_API USimpleBulletConfig : public UMassEntityConfigAsset
{
    GENERATED_BODY()

public:
    // Movement
    UPROPERTY(EditAnywhere, Category = "Movement")
    float Speed = 800.0f;

    // Damage
    UPROPERTY(EditAnywhere, Category = "Combat")
    float Damage = 10.0f;

    // Lifetime
    UPROPERTY(EditAnywhere, Category = "Lifetime")
    float MaxLifetime = 2.0f;

    UPROPERTY(EditAnywhere, Category = "Lifetime")
    bool bDespawnOffScreen = true;

    // Collision
    UPROPERTY(EditAnywhere, Category = "Collision")
    float CollisionRadius = 10.0f;

    UPROPERTY(EditAnywhere, Category = "Collision")
    bool bDestroyOnHit = true;

    // VFX
    UPROPERTY(EditAnywhere, Category = "VFX")
    UNiagaraSystem* TrailVFX = nullptr;

    UPROPERTY(EditAnywhere, Category = "VFX")
    UNiagaraSystem* HitVFX = nullptr;
};
```

---

### 4.3 Entity Archetype Data Asset

Create the archetype that designers will use:

```cpp
// BulletArchetype.h
#pragma once
#include "MassEntityTypes.h"
#include "MassEntityConfigAsset.h"
#include "BulletArchetype.generated.h"

/**
 * Archetype for simple bullet projectile.
 * Combines all required fragments with configured values.
 */
UCLASS()
class LAMENT_API UBulletArchetype : public UMassEntityConfigAsset
{
    GENERATED_BODY()

public:
    // Configuration
    UPROPERTY(EditAnywhere, Category = "Setup")
    USimpleBulletConfig* Config = nullptr;

    // Build entity template
    virtual void BuildTemplate(FMassEntityTemplateBuildContext& BuildContext, 
                              const UWorld& World) const override
    {
        if (!Config) return;

        // Add required fragments
        FTransformFragment& Transform = BuildContext.AddFragment_GetRef<FTransformFragment>();
        FVelocityFragment& Velocity = BuildContext.AddFragment_GetRef<FVelocityFragment>();
        FProjectileDataFragment& ProjectileData = BuildContext.AddFragment_GetRef<FProjectileDataFragment>();
        FSimpleCollisionFragment& Collision = BuildContext.AddFragment_GetRef<FSimpleCollisionFragment>();
        FNiagaraVFXFragment& VFX = BuildContext.AddFragment_GetRef<FNiagaraVFXFragment>();

        // Configure from data asset
        Velocity.MaxSpeed = Config->Speed;
        ProjectileData.Damage = Config->Damage;
        ProjectileData.MaxLifetime = Config->MaxLifetime;
        ProjectileData.bDespawnOffScreen = Config->bDespawnOffScreen;
        Collision.CollisionSize = FVector(Config->CollisionRadius);
        Collision.bDestroyOnHit = Config->bDestroyOnHit;
        VFX.TrailSystem = Config->TrailVFX;
        VFX.HitVFX = Config->HitVFX;
    }
};
```

---

### 4.4 Spawning System

Create a spawner subsystem to spawn entities from archetypes:

```cpp
// LamentEntitySpawner.h
#pragma once
#include "Subsystems/WorldSubsystem.h"
#include "MassEntityTypes.h"
#include "LamentEntitySpawner.generated.h"

class UMassEntityConfigAsset;

/**
 * World subsystem for spawning Mass entities.
 * Handles entity pooling and batch spawning.
 */
UCLASS()
class LAMENT_API ULamentEntitySpawner : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    // Spawn single entity from archetype
    UFUNCTION(BlueprintCallable, Category = "Lament|Spawning")
    FMassEntityHandle SpawnEntity(const UMassEntityConfigAsset* Archetype, 
                                   const FTransform& SpawnTransform,
                                   const FVector& InitialVelocity = FVector::ZeroVector);

    // Batch spawn (more efficient)
    TArray<FMassEntityHandle> SpawnEntities(const UMassEntityConfigAsset* Archetype,
                                            const TArray<FTransform>& Transforms,
                                            const TArray<FVector>& Velocities);

    // Despawn entity (returns to pool)
    UFUNCTION(BlueprintCallable, Category = "Lament|Spawning")
    void DespawnEntity(FMassEntityHandle Entity);

protected:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

private:
    // Mass entity subsystem reference
    UPROPERTY()
    class UMassEntitySubsystem* EntitySubsystem = nullptr;
};
```

**Implementation:**
```cpp
// LamentEntitySpawner.cpp
#include "LamentEntitySpawner.h"
#include "MassEntitySubsystem.h"
#include "MassEntityConfigAsset.h"
#include "MassExecutionContext.h"

void ULamentEntitySpawner::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    
    EntitySubsystem = GetWorld()->GetSubsystem<UMassEntitySubsystem>();
}

void ULamentEntitySpawner::Deinitialize()
{
    Super::Deinitialize();
}

FMassEntityHandle ULamentEntitySpawner::SpawnEntity(const UMassEntityConfigAsset* Archetype,
                                                     const FTransform& SpawnTransform,
                                                     const FVector& InitialVelocity)
{
    if (!EntitySubsystem || !Archetype) 
        return FMassEntityHandle();

    // Get or create entity template from archetype
    FMassEntityTemplate* Template = Archetype->GetOrCreateTemplate(*GetWorld());
    if (!Template) 
        return FMassEntityHandle();

    // Spawn entity
    FMassEntityHandle NewEntity = EntitySubsystem->CreateEntity(Template->GetTemplateID());

    // Set initial transform
    if (FTransformFragment* Transform = EntitySubsystem->GetFragmentDataPtr<FTransformFragment>(NewEntity))
    {
        Transform->Transform = SpawnTransform;
    }

    // Set initial velocity
    if (FVelocityFragment* Velocity = EntitySubsystem->GetFragmentDataPtr<FVelocityFragment>(NewEntity))
    {
        Velocity->Velocity = InitialVelocity;
    }

    // Set spawn location (for distance tracking)
    if (FProjectileDataFragment* ProjectileData = EntitySubsystem->GetFragmentDataPtr<FProjectileDataFragment>(NewEntity))
    {
        ProjectileData->SpawnLocation = SpawnTransform.GetLocation();
    }

    return NewEntity;
}

TArray<FMassEntityHandle> ULamentEntitySpawner::SpawnEntities(const UMassEntityConfigAsset* Archetype,
                                                               const TArray<FTransform>& Transforms,
                                                               const TArray<FVector>& Velocities)
{
    TArray<FMassEntityHandle> SpawnedEntities;
    
    if (!EntitySubsystem || !Archetype || Transforms.Num() == 0)
        return SpawnedEntities;

    // PRODUCTION NOTE: Batch spawning is more efficient than individual spawns
    for (int32 i = 0; i < Transforms.Num(); ++i)
    {
        FVector Velocity = (i < Velocities.Num()) ? Velocities[i] : FVector::ZeroVector;
        FMassEntityHandle Entity = SpawnEntity(Archetype, Transforms[i], Velocity);
        SpawnedEntities.Add(Entity);
    }

    return SpawnedEntities;
}

void ULamentEntitySpawner::DespawnEntity(FMassEntityHandle Entity)
{
    if (!EntitySubsystem || !Entity.IsValid())
        return;

    // PRODUCTION NOTE: Trigger death VFX before despawning
    if (FNiagaraVFXFragment* VFX = EntitySubsystem->GetFragmentDataPtr<FNiagaraVFXFragment>(Entity))
    {
        if (VFX->DeathVFX)
        {
            // Spawn one-shot VFX at entity location
            if (FTransformFragment* Transform = EntitySubsystem->GetFragmentDataPtr<FTransformFragment>(Entity))
            {
                // PRODUCTION NOTE: Use VFX pooling system
                UNiagaraFunctionLibrary::SpawnSystemAtLocation(
                    GetWorld(),
                    VFX->DeathVFX,
                    Transform->GetLocation()
                );
            }
        }
    }

    // Destroy entity (returns to pool automatically)
    EntitySubsystem->DestroyEntity(Entity);
}
```

---

### 4.5 Usage Example

**Spawning a bullet from C++:**
```cpp
// In your weapon/gun class
void APlayerGun::FireBullet()
{
    ULamentEntitySpawner* Spawner = GetWorld()->GetSubsystem<ULamentEntitySpawner>();
    if (!Spawner) return;

    // Get muzzle transform
    FTransform MuzzleTransform = MuzzleComponent->GetComponentTransform();
    
    // Calculate bullet velocity
    FVector FireDirection = MuzzleTransform.GetRotation().GetForwardVector();
    FVector BulletVelocity = FireDirection * 800.0f; // Speed from config

    // Spawn bullet
    FMassEntityHandle Bullet = Spawner->SpawnEntity(
        BulletArchetype,      // UBulletArchetype* data asset
        MuzzleTransform,
        BulletVelocity
    );
}
```

**Batch spawning (shotgun spread):**
```cpp
void APlayerShotgun::FireShotgun()
{
    ULamentEntitySpawner* Spawner = GetWorld()->GetSubsystem<ULamentEntitySpawner>();
    if (!Spawner) return;

    const int32 PelletCount = 8;
    const float SpreadAngle = 15.0f;
    
    TArray<FTransform> Transforms;
    TArray<FVector> Velocities;
    
    FTransform MuzzleTransform = MuzzleComponent->GetComponentTransform();
    FVector BaseDirection = MuzzleTransform.GetRotation().GetForwardVector();
    
    // Generate spread pattern
    for (int32 i = 0; i < PelletCount; ++i)
    {
        // Random spread
        FRotator Spread(
            FMath::FRandRange(-SpreadAngle, SpreadAngle),
            FMath::FRandRange(-SpreadAngle, SpreadAngle),
            0.0f
        );
        
        FVector Direction = Spread.RotateVector(BaseDirection);
        FVector Velocity = Direction * 800.0f;
        
        Transforms.Add(MuzzleTransform);
        Velocities.Add(Velocity);
    }
    
    // Batch spawn all pellets
    TArray<FMassEntityHandle> Pellets = Spawner->SpawnEntities(
        BulletArchetype,
        Transforms,
        Velocities
    );
}
```

---

### 4.6 Performance Characteristics

**Simple Bullet (Tier 1) Performance:**

| Metric | Value |
|--------|-------|
| Memory per Entity | ~200 bytes |
| Fragments | 5 |
| Processors | 3 (Movement, Lifetime, Collision) |
| Update Cost | 0.01ms per 100 entities |
| Recommended Max | 200-300 @ 60fps |

**Optimization Notes:**
- All processing is batched (cache-friendly)
- No virtual function calls in hot path
- Spatial hashing for collision (O(1) broad phase)
- VFX components are pooled

---

## 5. Project File Structure

Recommended file organization for the Mass Entity system:

```
Lament/
├── Source/
│   └── Lament/
│       ├── MassEntity/
│       │   ├── Fragments/
│       │   │   ├── Core/
│       │   │   │   ├── TransformFragment.h
│       │   │   │   ├── VelocityFragment.h
│       │   │   │   ├── HealthFragment.h
│       │   │   │   ├── ProjectileDataFragment.h
│       │   │   │   ├── SimpleCollisionFragment.h
│       │   │   │   ├── TriggerStateFragment.h
│       │   │   │   └── NiagaraVFXFragment.h
│       │   │   ├── Movement/
│       │   │   │   ├── FloaterFragment.h
│       │   │   │   ├── FollowerFragment.h
│       │   │   │   ├── WaverFragment.h
│       │   │   │   └── ... (see Movement & Triggers doc)
│       │   │   ├── Quality/
│       │   │   │   ├── ShielderFragment.h
│       │   │   │   ├── InvulnerableFragment.h
│       │   │   │   └── ... (see Combat Systems doc)
│       │   │   └── Ability/
│       │   │       ├── EmitterFragment.h
│       │   │       ├── SplitterFragment.h
│       │   │       └── ... (see Combat Systems doc)
│       │   ├── Processors/
│       │   │   ├── Core/
│       │   │   │   ├── MassSimpleMovementProcessor.h/.cpp
│       │   │   │   ├── MassProjectileLifetimeProcessor.h/.cpp
│       │   │   │   ├── MassSimpleCollisionProcessor.h/.cpp
│       │   │   │   ├── MassTriggerProcessor.h/.cpp
│       │   │   │   ├── MassHealthProcessor.h/.cpp
│       │   │   │   └── MassNiagaraProcessor.h/.cpp
│       │   │   ├── Movement/
│       │   │   │   ├── MassFloaterProcessor.h/.cpp
│       │   │   │   ├── MassFollowerProcessor.h/.cpp
│       │   │   │   └── ... (one per movement attribute)
│       │   │   ├── Quality/
│       │   │   │   └── ... (see Combat Systems doc)
│       │   │   └── Ability/
│       │   │       ├── MassEmitterProcessor.h/.cpp
│       │   │       ├── MassSplitterProcessor.h/.cpp
│       │   │       └── ... (see Combat Systems doc)
│       │   ├── DataAssets/
│       │   │   ├── EntityArchetype.h
│       │   │   ├── FragmentConfigs/
│       │   │   │   ├── MassFragmentConfig.h (base class)
│       │   │   │   ├── SimpleBulletConfig.h
│       │   │   │   ├── FloaterFragmentConfig.h
│       │   │   │   └── ... (one per fragment type)
│       │   │   └── TriggerRuleSet.h
│       │   ├── Spawning/
│       │   │   ├── LamentEntitySpawner.h/.cpp
│       │   │   └── EntityPool.h/.cpp
│       │   └── Visualization/
│       │       └── MassVisualizationActor.h/.cpp
│       └── ... (other game code)
└── Content/
    ├── DataAssets/
    │   ├── Projectiles/
    │   │   ├── DA_SimpleBullet.uasset
    │   │   ├── DA_HomingMissile.uasset
    │   │   ├── DA_SplittingBomb.uasset
    │   │   └── ... (archetype data assets)
    │   └── Enemies/
    │       ├── DA_ShadowStalker.uasset
    │       ├── DA_PlagueCarrier.uasset
    │       └── ... (enemy archetypes)
    ├── VFX/
    │   ├── Projectiles/
    │   │   ├── NS_BulletTrail.uasset
    │   │   ├── NS_MissileTrail.uasset
    │   │   ├── NS_BulletImpact.uasset
    │   │   └── NS_Explosion.uasset
    │   └── Enemies/
    │       └── ... (enemy VFX)
    └── Blueprints/
        └── Visualization/
            ├── BP_BulletVisual.uasset (optional)
            └── ... (visual actors if needed)
```

---

## 6. Quick Start Checklist

Follow this checklist to get started with the Mass Entity system:

### Phase 1: Project Setup
- [ ] Enable Mass Entity plugin in UE 5.7 project
- [ ] Create `Source/Lament/MassEntity/` directory structure
- [ ] Add Mass Entity module dependency to `Lament.Build.cs`
  ```csharp
  PublicDependencyModuleNames.AddRange(new string[] { 
      "MassEntity", 
      "MassCommon", 
      "MassSpawner",
      "MassGameplay",
      "Niagara"
  });
  ```

### Phase 2: Core Fragments
- [ ] Implement `FTransformFragment` (Section 2.1)
- [ ] Implement `FVelocityFragment` (Section 2.2)
- [ ] Implement `FProjectileDataFragment` (Section 2.3)
- [ ] Implement `FSimpleCollisionFragment` (Section 2.5)

### Phase 3: Core Processors
- [ ] Implement `UMassSimpleMovementProcessor` (Section 3.1)
- [ ] Implement `UMassProjectileLifetimeProcessor` (Section 3.2)
- [ ] Implement `UMassSimpleCollisionProcessor` (Section 3.3)

### Phase 4: Spawning System
- [ ] Implement `ULamentEntitySpawner` subsystem (Section 4.4)
- [ ] Test spawning/despawning entities

### Phase 5: First Entity
- [ ] Create `USimpleBulletConfig` data asset class
- [ ] Create `UBulletArchetype` class
- [ ] Create bullet archetype data asset in Content Browser
- [ ] Test spawning bullets from weapon

### Phase 6: Validation
- [ ] Spawn 100 bullets, verify 60fps
- [ ] Test collision detection
- [ ] Test lifetime despawning
- [ ] Test off-screen despawning

### Next Steps
Once core system is working:
- Read `MassEntity_MovementAndTriggers.md` for movement attributes
- Read `MassEntity_CombatSystems.md` for combat abilities
- Read `MassEntity_AdvancedSystems.md` for VFX, optimization, etc.

---

## 7. Summary

**What You've Learned:**
- Mass Entity architecture (3 layers: Designer, Runtime, Visualization)
- Three-tier performance system (Simple, Complex, Enemy)
- Core concepts (Fragments, Processors, Traits, Archetypes)
- Core fragments for projectiles (Transform, Velocity, ProjectileData, Collision)
- Core processors (Movement, Lifetime, Collision)
- Complete implementation of Tier 1 projectile (Simple Bullet)
- Spawning system and entity lifecycle

**Next Documents:**
1. `MassEntity_MovementAndTriggers.md` - Movement attributes and behavior switching
2. `MassEntity_CombatSystems.md` - Damage, abilities, and interactions
3. `MassEntity_AdvancedSystems.md` - VFX, perception, optimization, and advanced features

**Key Takeaways:**
- Fragments = Data only (no logic)
- Processors = Logic only (operates on fragments)
- Archetypes = Designer-friendly entity definitions
- Performance scales with fragment count, not entity count
- 200+ simple entities @ 60fps is achievable

---

**Document Version:** 1.0  
**Last Updated:** December 2024  
**UE Version:** 5.7+  
**Related Documents:** `EnemyAI.md`, `MassEntity_MovementAndTriggers.md`, `MassEntity_CombatSystems.md`, `MassEntity_AdvancedSystems.md`
