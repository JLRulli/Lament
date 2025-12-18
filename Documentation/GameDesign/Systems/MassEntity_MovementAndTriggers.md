# Mass Entity Movement & Trigger Systems

## Overview

This document covers all movement attributes and the trigger system for behavior switching. Movement attributes define HOW entities move, while triggers define WHEN they switch between different movement behaviors.

**Prerequisites:**
- Read `MassEntity_CoreArchitecture.md` first
- Understanding of fragments and processors
- Familiarity with movement attributes from `EnemyAI.md`

**What You'll Learn:**
- All 20+ movement fragments
- Movement processor implementation patterns
- Complete trigger system (state machines)
- Full implementation examples (Floater, Follower, Trigger System)
- Advanced patterns (multi-state enemies, boss phases)

---

## Table of Contents

1. Movement System Overview
2. Movement Fragments Reference
3. Movement Processors
4. Full Implementation: Floater System
5. Full Implementation: Follower System
6. Trigger System Deep Dive
7. State Machine Patterns
8. Complete Entity Example: Shadow Stalker

---

## 1. Movement System Overview

### 1.1 Movement Architecture

```
Entity Movement Pipeline (Each Frame):

[UMassTriggerProcessor] ← Evaluate triggers first
    ↓
Check conditions (proximity, LOS, timer, health)
    ↓
Switch state if triggered (add/remove movement fragments)
    ↓
[Movement Processors] ← Execute active movement behaviors
    ↓
Update entity Transform based on active fragments
    ↓
Result: Entity moves according to current state
```

### 1.2 Movement Fragment Categories

Movement attributes are organized by complexity:

**Simple Movement** (Tier 1 compatible):
- Liner (straight line)
- Stationary (no movement)

**Physics-Free Movement** (Tier 2):
- Floater (sine wave bobbing)
- Waver (sine wave along path)
- Rotator (orbit around point)
- Swinger (pendulum motion)

**AI-Driven Movement** (Tier 2-3):
- Follower (chase target)
- Pacer (patrol with turn-around)
- Roamer (random direction changes)
- Mirror (copy/inverse player movement)

**Advanced Movement** (Tier 3):
- Jumper (physics-based jumping)
- Dasher (burst movement)
- Swooper (dive attack)
- Teleporter (instant repositioning)

**Geometry-Based** (All tiers):
- Walker (ground-only movement)
- Sticky (wall/ceiling adherence)
- Geobound (locked to geometry)
- Tethered (rope/chain constraint)

### 1.3 Combining Movement Attributes

Entities can have **multiple movement fragments**, but only one processor should be active at a time (controlled by triggers).

**Example Combinations:**
```cpp
// Floater + Follower (ghost that floats while chasing)
Entity has: FFloaterFragment + FFollowerFragment
State 0: FloaterProcessor active (idle bobbing)
State 1: FloaterProcessor + FollowerProcessor active (chase while bobbing)

// Walker + Dasher (enemy that walks and occasionally lunges)
Entity has: FWalkerFragment + FDasherFragment
State 0: WalkerProcessor active (normal patrol)
State 1: DasherProcessor active (dash towards player)
```

---

## 2. Movement Fragments Reference

### 2.1 FFloaterFragment

**Purpose:** Entity bobs up and down in a sine wave pattern.

**Declaration:**
```cpp
// FloaterFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "FloaterFragment.generated.h"

/**
 * Sine wave bobbing movement.
 * Entity hovers at specified height with smooth up/down motion.
 * Used by: Flying enemies, floating objects, hovering drones.
 */
USTRUCT()
struct LAMENT_API FFloaterFragment : public FMassFragment
{
    GENERATED_BODY()

    // Base height to float at (world Z or offset from ground)
    UPROPERTY()
    float FloatHeight = 100.0f;

    // Speed of bobbing (cycles per second)
    UPROPERTY()
    float BobSpeed = 2.0f;

    // How far to bob up/down from base height
    UPROPERTY()
    float BobAmplitude = 20.0f;

    // Time offset for staggered bobbing (set randomly on spawn)
    UPROPERTY()
    float TimeOffset = 0.0f;

    // Should height be relative to ground or absolute world Z?
    UPROPERTY()
    bool bRelativeToGround = false;

    // If relative to ground, use this trace distance
    UPROPERTY()
    float GroundTraceDistance = 200.0f;
};
```

**Processor:** `UMassFloaterProcessor` (Section 4)

---

### 2.2 FFollowerFragment

**Purpose:** Entity chases a target (usually the player).

**Declaration:**
```cpp
// FollowerFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "FollowerFragment.generated.h"

/**
 * Pursues a target entity (homing behavior).
 * Can use direct path or avoidance-based pathfinding.
 * Used by: Homing missiles, chasing enemies, tracking projectiles.
 */
USTRUCT()
struct LAMENT_API FFollowerFragment : public FMassFragment
{
    GENERATED_BODY()

    // Target to follow (usually player entity)
    UPROPERTY()
    FMassEntityHandle Target;

    // Movement speed when following
    UPROPERTY()
    float FollowSpeed = 300.0f;

    // Stop moving when this close to target
    UPROPERTY()
    float StoppingDistance = 50.0f;

    // Turn rate (degrees per second, 0 = instant turn)
    UPROPERTY()
    float TurnRate = 360.0f;

    // Use direct line to target or pathfinding?
    UPROPERTY()
    bool bUseDirectPath = true;

    // Acceleration (0 = instant speed, >0 = gradual)
    UPROPERTY()
    float Acceleration = 0.0f;

    // Current speed (for acceleration)
    UPROPERTY()
    float CurrentSpeed = 0.0f;

    // Prediction: lead target based on its velocity?
    UPROPERTY()
    bool bPredictTargetMovement = false;

    // Prediction time in seconds
    UPROPERTY()
    float PredictionTime = 0.5f;
};
```

**Processor:** `UMassFollowerProcessor` (Section 5)

---

### 2.3 FWaverFragment

**Purpose:** Entity moves in sine wave pattern along a direction.

**Declaration:**
```cpp
// WaverFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "WaverFragment.generated.h"

/**
 * Sine wave movement perpendicular to forward direction.
 * Like Floater but moves laterally instead of vertically.
 * Used by: Weaving projectiles, serpentine enemies, oscillating flyers.
 */
USTRUCT()
struct LAMENT_API FWaverFragment : public FMassFragment
{
    GENERATED_BODY()

    // Frequency of wave (cycles per second)
    UPROPERTY()
    float WaveFrequency = 1.0f;

    // Amplitude of wave (distance from center)
    UPROPERTY()
    float WaveAmplitude = 50.0f;

    // Direction perpendicular to movement (usually Right vector)
    UPROPERTY()
    FVector WaveDirection = FVector::RightVector;

    // Phase offset (0-2π, for staggered waves)
    UPROPERTY()
    float PhaseOffset = 0.0f;

    // Base forward speed
    UPROPERTY()
    float ForwardSpeed = 200.0f;

    // Should wave direction rotate with entity?
    UPROPERTY()
    bool bRotateWithEntity = true;
};
```

**Processor:** `UMassWaverProcessor`

---

### 2.4 FLinerFragment

**Purpose:** Move in straight line to a target position.

**Declaration:**
```cpp
// LinerFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "LinerFragment.generated.h"

/**
 * Straight-line movement to destination.
 * Used by: Simple projectiles, charging attacks, straight shots.
 */
USTRUCT()
struct LAMENT_API FLinerFragment : public FMassFragment
{
    GENERATED_BODY()

    // Direction to move (normalized)
    UPROPERTY()
    FVector Direction = FVector::ForwardVector;

    // Movement speed
    UPROPERTY()
    float Speed = 400.0f;

    // Optional: Target position (if moving to specific point)
    UPROPERTY()
    FVector TargetPosition = FVector::ZeroVector;

    // Should stop at target position?
    UPROPERTY()
    bool bStopAtTarget = false;

    // Has reached target?
    UPROPERTY()
    bool bHasReachedTarget = false;
};
```

**Processor:** `UMassLinerProcessor`

**Note:** Very similar to simple velocity movement. Use this when you need trigger-based switching from Liner to other movement.

---

### 2.5 FDasherFragment

**Purpose:** Rapid burst movement in a direction.

**Declaration:**
```cpp
// DasherFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "DasherFragment.generated.h"

/**
 * Burst movement (dash/lunge).
 * Can be triggered by conditions (proximity, timer, etc).
 * Used by: Lunging enemies, dash attacks, quick repositioning.
 */
USTRUCT()
struct LAMENT_API FDasherFragment : public FMassFragment
{
    GENERATED_BODY()

    // Dash speed (usually much faster than normal movement)
    UPROPERTY()
    float DashSpeed = 800.0f;

    // Dash duration (seconds)
    UPROPERTY()
    float DashDuration = 0.3f;

    // Direction to dash (set when dash is triggered)
    UPROPERTY()
    FVector DashDirection = FVector::ZeroVector;

    // Is currently dashing?
    UPROPERTY()
    bool bIsDashing = false;

    // Time remaining in current dash
    UPROPERTY()
    float DashTimeRemaining = 0.0f;

    // Cooldown before next dash
    UPROPERTY()
    float DashCooldown = 2.0f;

    // Cooldown timer
    UPROPERTY()
    float CooldownRemaining = 0.0f;

    // Can dash be interrupted?
    UPROPERTY()
    bool bCanInterrupt = false;
};
```

**Processor:** `UMassDasherProcessor`

---

### 2.6 FRotatorFragment

**Purpose:** Orbit around a fixed point.

**Declaration:**
```cpp
// RotatorFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "RotatorFragment.generated.h"

/**
 * Circular orbit around a center point.
 * Center can be static or moving (attached to another entity).
 * Used by: Orbiting projectiles, circling enemies, rotating shields.
 */
USTRUCT()
struct LAMENT_API FRotatorFragment : public FMassFragment
{
    GENERATED_BODY()

    // Center point of rotation
    UPROPERTY()
    FVector CenterPoint = FVector::ZeroVector;

    // Optional: Entity to orbit around (overrides CenterPoint)
    UPROPERTY()
    FMassEntityHandle CenterEntity;

    // Orbit radius
    UPROPERTY()
    float OrbitRadius = 100.0f;

    // Rotation speed (degrees per second)
    UPROPERTY()
    float RotationSpeed = 90.0f;

    // Current angle (0-360)
    UPROPERTY()
    float CurrentAngle = 0.0f;

    // Rotation axis (usually Up vector)
    UPROPERTY()
    FVector RotationAxis = FVector::UpVector;

    // Should entity face forward along orbit path?
    UPROPERTY()
    bool bFaceMovementDirection = true;

    // Optional: Radius can change over time
    UPROPERTY()
    float RadiusChangeRate = 0.0f; // Units per second
};
```

**Processor:** `UMassRotatorProcessor`

---

### 2.7 FPacerFragment

**Purpose:** Patrol movement with turn-around at edges.

**Declaration:**
```cpp
// PacerFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "PacerFragment.generated.h"

/**
 * Patrol movement that reverses direction at edges/walls.
 * Used by: Patrolling enemies, platform-bound enemies.
 */
USTRUCT()
struct LAMENT_API FPacerFragment : public FMassFragment
{
    GENERATED_BODY()

    // Patrol speed
    UPROPERTY()
    float Speed = 150.0f;

    // Current movement direction (1 or -1)
    UPROPERTY()
    float DirectionMultiplier = 1.0f;

    // Distance to check for edges/walls
    UPROPERTY()
    float EdgeCheckDistance = 50.0f;

    // Should reverse at platform edges?
    UPROPERTY()
    bool bReverseAtEdges = true;

    // Should reverse when hitting walls?
    UPROPERTY()
    bool bReverseAtWalls = true;

    // Optional: Pause duration when reversing
    UPROPERTY()
    float ReversePauseDuration = 0.0f;

    // Pause timer
    UPROPERTY()
    float PauseTimeRemaining = 0.0f;
};
```

**Processor:** `UMassPacerProcessor`

---

### 2.8 FRoamerFragment

**Purpose:** Random direction changes.

**Declaration:**
```cpp
// RoamerFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "RoamerFragment.generated.h"

/**
 * Random wandering movement.
 * Changes direction at random intervals.
 * Used by: Wandering enemies, environmental creatures.
 */
USTRUCT()
struct LAMENT_API FRoamerFragment : public FMassFragment
{
    GENERATED_BODY()

    // Movement speed
    UPROPERTY()
    float Speed = 100.0f;

    // Current direction
    UPROPERTY()
    FVector CurrentDirection = FVector::ForwardVector;

    // Min/max time between direction changes
    UPROPERTY()
    float MinChangeInterval = 1.0f;

    UPROPERTY()
    float MaxChangeInterval = 3.0f;

    // Time until next direction change
    UPROPERTY()
    float TimeUntilChange = 0.0f;

    // Constrain movement to 2D plane?
    UPROPERTY()
    bool bMovementIn2D = true;

    // Optional: Avoid walls (raycast ahead)
    UPROPERTY()
    bool bAvoidObstacles = true;

    UPROPERTY()
    float ObstacleCheckDistance = 100.0f;
};
```

**Processor:** `UMassRoamerProcessor`

---

### 2.9 Additional Movement Fragments (Brief)

These fragments follow similar patterns. Full implementations in appendix.

**FWalkerFragment** - Ground-locked movement with gravity
**FJumperFragment** - Physics-based jumping
**FStickyFragment** - Adhere to walls/ceilings
**FSwingerFragment** - Pendulum swing from fixed point
**FSwooperFragment** - Dive attack, return to position
**FTeleporterFragment** - Instant position changes
**FPongerFragment** - Bounce off walls at angles
**FGeoBindFragment** - Locked to level geometry
**FTetheredFragment** - Rope/chain constraint
**FMirrorFragment** - Copy/inverse player movement
**FRiserFragment** - Rise from surfaces
**FDuckerFragment** - Lower/sink into surfaces
**FFallerFragment** - Fall from ceiling

**See `MassEntity_AttributeReference.md` for complete declarations.**

---

## 3. Movement Processors

### 3.1 Processor Pattern

All movement processors follow this pattern:

```cpp
// Pattern for movement processors
class UMass[Movement]Processor : public UMassProcessor
{
    // 1. Configure which fragments are required
    virtual void ConfigureQueries() override
    {
        EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadWrite);
        EntityQuery.AddRequirement<F[Movement]Fragment>(EMassFragmentAccess::ReadWrite);
        // Optional fragments as needed
    }

    // 2. Execute on all matching entities
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override
    {
        EntityQuery.ForEachEntityChunk(EntityManager, Context, 
            [](FMassExecutionContext& Context)
            {
                // Get fragment arrays for this chunk
                TArrayView<FTransformFragment> Transforms = Context.GetMutableFragmentView<FTransformFragment>();
                TArrayView<F[Movement]Fragment> Movement = Context.GetMutableFragmentView<F[Movement]Fragment>();
                
                const float DeltaTime = Context.GetDeltaTimeSeconds();
                
                // Process all entities in chunk
                for (int32 i = 0; i < Context.GetNumEntities(); ++i)
                {
                    // Update transform based on movement logic
                    UpdateMovement(Transforms[i], Movement[i], DeltaTime);
                }
            });
    }
};
```

### 3.2 Processor Execution Order

Movement processors should run **after triggers** but **before abilities/collision**:

```cpp
UMassMyMovementProcessor::UMassMyMovementProcessor()
{
    ExecutionOrder.ExecuteAfter.Add(TEXT("Triggers"));
    ExecutionOrder.ExecuteBefore.Add(TEXT("Abilities"));
}
```

### 3.3 Conditional Processing with Tags

To enable/disable processors per-entity, use tags:

```cpp
void UMassFloaterProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadWrite);
    EntityQuery.AddRequirement<FFloaterFragment>(EMassFragmentAccess::ReadWrite);
    
    // Only process entities with ActiveFloaterTag
    EntityQuery.AddTagRequirement<FActiveFloaterTag>(EMassFragmentPresence::All);
}
```

Triggers can add/remove tags to switch which processor runs.

---

## 4. Full Implementation: Floater System

Complete implementation of the Floater movement attribute.

### 4.1 Fragment (Already Shown in Section 2.1)

```cpp
// FloaterFragment.h - See Section 2.1 for full declaration
```

### 4.2 Processor Declaration

```cpp
// MassFloaterProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassFloaterProcessor.generated.h"

/**
 * Processes entities with FFloaterFragment.
 * Applies sine wave bobbing to entity Z position.
 * 
 * Execution Order: Default (after triggers, before collision)
 */
UCLASS()
class LAMENT_API UMassFloaterProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassFloaterProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    // Helper: Get ground height if relative to ground
    float GetGroundHeight(const FVector& Location, UWorld* World, float TraceDistance) const;
};
```

### 4.3 Processor Implementation

```cpp
// MassFloaterProcessor.cpp
#include "MassFloaterProcessor.h"
#include "MassCommonFragments.h"
#include "Engine/World.h"

UMassFloaterProcessor::UMassFloaterProcessor()
{
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Movement;
}

void UMassFloaterProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadWrite);
    EntityQuery.AddRequirement<FFloaterFragment>(EMassFragmentAccess::ReadWrite);
}

void UMassFloaterProcessor::Execute(FMassEntityManager& EntityManager, 
                                     FMassExecutionContext& Context)
{
    UWorld* World = Context.GetWorld();
    const float CurrentTime = World->GetTimeSeconds();
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [CurrentTime, World, this](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            
            TArrayView<FTransformFragment> Transforms = Context.GetMutableFragmentView<FTransformFragment>();
            TArrayView<FFloaterFragment> Floaters = Context.GetMutableFragmentView<FFloaterFragment>();
            
            for (int32 i = 0; i < NumEntities; ++i)
            {
                FTransformFragment& Transform = Transforms[i];
                FFloaterFragment& Floater = Floaters[i];
                
                FVector Location = Transform.GetLocation();
                
                // Calculate base height
                float BaseHeight = Floater.FloatHeight;
                if (Floater.bRelativeToGround)
                {
                    float GroundHeight = GetGroundHeight(Location, World, Floater.GroundTraceDistance);
                    BaseHeight = GroundHeight + Floater.FloatHeight;
                }
                
                // Calculate sine wave offset
                float Time = CurrentTime + Floater.TimeOffset;
                float BobOffset = FMath::Sin(Time * Floater.BobSpeed * TWO_PI) * Floater.BobAmplitude;
                
                // Update Z position
                Location.Z = BaseHeight + BobOffset;
                Transform.SetLocation(Location);
            }
        });
}

float UMassFloaterProcessor::GetGroundHeight(const FVector& Location, 
                                              UWorld* World, 
                                              float TraceDistance) const
{
    if (!World) return 0.0f;
    
    // Raycast down to find ground
    FVector TraceStart = Location;
    FVector TraceEnd = Location - FVector(0, 0, TraceDistance);
    
    FHitResult HitResult;
    FCollisionQueryParams QueryParams;
    QueryParams.bTraceComplex = false;
    
    bool bHit = World->LineTraceSingleByChannel(
        HitResult,
        TraceStart,
        TraceEnd,
        ECC_WorldStatic,
        QueryParams
    );
    
    if (bHit)
    {
        return HitResult.Location.Z;
    }
    
    // No ground found, return current Z
    return Location.Z;
}
```

### 4.4 Fragment Configuration

```cpp
// FloaterFragmentConfig.h
#pragma once
#include "MassEntityConfigAsset.h"
#include "FloaterFragmentConfig.generated.h"

/**
 * Designer-friendly configuration for FFloaterFragment.
 */
UCLASS()
class LAMENT_API UFloaterFragmentConfig : public UMassFragmentConfig
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, Category = "Floater", meta = (ClampMin = "0"))
    float FloatHeight = 100.0f;

    UPROPERTY(EditAnywhere, Category = "Floater", meta = (ClampMin = "0.1"))
    float BobSpeed = 2.0f;

    UPROPERTY(EditAnywhere, Category = "Floater", meta = (ClampMin = "0"))
    float BobAmplitude = 20.0f;

    UPROPERTY(EditAnywhere, Category = "Floater")
    bool bRelativeToGround = false;

    UPROPERTY(EditAnywhere, Category = "Floater", meta = (EditCondition = "bRelativeToGround"))
    float GroundTraceDistance = 200.0f;

    virtual void AddToEntity(FMassEntityManager& EntityManager,
                            FMassEntityHandle Entity) const override
    {
        FFloaterFragment& Fragment = EntityManager.AddFragmentToEntity<FFloaterFragment>(Entity);
        Fragment.FloatHeight = FloatHeight;
        Fragment.BobSpeed = BobSpeed;
        Fragment.BobAmplitude = BobAmplitude;
        Fragment.TimeOffset = FMath::FRand() * TWO_PI; // Random phase
        Fragment.bRelativeToGround = bRelativeToGround;
        Fragment.GroundTraceDistance = GroundTraceDistance;
    }
};
```

### 4.5 Usage Example

```cpp
// In entity archetype data asset
UPROPERTY(EditAnywhere, Category = "Movement")
UFloaterFragmentConfig* FloaterConfig;

// Result: Entity bobs up and down smoothly
```

---

## 5. Full Implementation: Follower System

Complete implementation of target-chasing behavior.

### 5.1 Fragment (Already Shown in Section 2.2)

### 5.2 Processor Declaration

```cpp
// MassFollowerProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassFollowerProcessor.generated.h"

/**
 * Processes entities with FFollowerFragment.
 * Moves entity towards target with optional acceleration and turn rate.
 * Can predict target movement for leading shots.
 * 
 * Execution Order: Default (after triggers)
 */
UCLASS()
class LAMENT_API UMassFollowerProcessor : public UMassProcessor
{
    GENERATED_BODY()

public:
    UMassFollowerProcessor();

protected:
    virtual void ConfigureQueries() override;
    virtual void Execute(FMassEntityManager& EntityManager, 
                        FMassExecutionContext& Context) override;

private:
    FMassEntityQuery EntityQuery;
    
    // Helper: Get target position (with prediction if enabled)
    FVector GetTargetPosition(const FFollowerFragment& Follower,
                             FMassEntityManager& EntityManager) const;
};
```

### 5.3 Processor Implementation

```cpp
// MassFollowerProcessor.cpp
#include "MassFollowerProcessor.h"
#include "MassCommonFragments.h"

UMassFollowerProcessor::UMassFollowerProcessor()
{
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::Movement;
}

void UMassFollowerProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadWrite);
    EntityQuery.AddRequirement<FFollowerFragment>(EMassFragmentAccess::ReadWrite);
}

void UMassFollowerProcessor::Execute(FMassEntityManager& EntityManager, 
                                      FMassExecutionContext& Context)
{
    const float DeltaTime = Context.GetDeltaTimeSeconds();
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [DeltaTime, &EntityManager, this](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            
            TArrayView<FTransformFragment> Transforms = Context.GetMutableFragmentView<FTransformFragment>();
            TArrayView<FFollowerFragment> Followers = Context.GetMutableFragmentView<FFollowerFragment>();
            
            for (int32 i = 0; i < NumEntities; ++i)
            {
                FTransformFragment& Transform = Transforms[i];
                FFollowerFragment& Follower = Followers[i];
                
                // Get target position
                FVector TargetPos = GetTargetPosition(Follower, EntityManager);
                FVector CurrentPos = Transform.GetLocation();
                
                // Calculate direction to target
                FVector ToTarget = TargetPos - CurrentPos;
                float DistanceToTarget = ToTarget.Size();
                
                // Check stopping distance
                if (DistanceToTarget <= Follower.StoppingDistance)
                {
                    continue; // Don't move, we're close enough
                }
                
                FVector DesiredDirection = ToTarget.GetSafeNormal();
                
                // Handle acceleration
                if (Follower.Acceleration > 0.0f)
                {
                    // Gradually accelerate to follow speed
                    Follower.CurrentSpeed = FMath::FInterpTo(
                        Follower.CurrentSpeed,
                        Follower.FollowSpeed,
                        DeltaTime,
                        Follower.Acceleration
                    );
                }
                else
                {
                    Follower.CurrentSpeed = Follower.FollowSpeed;
                }
                
                // Handle turn rate
                FVector CurrentDirection = Transform.GetRotation().Vector();
                FVector NewDirection = DesiredDirection;
                
                if (Follower.TurnRate > 0.0f)
                {
                    // Gradually rotate towards target
                    float MaxTurnRadians = FMath::DegreesToRadians(Follower.TurnRate) * DeltaTime;
                    NewDirection = FMath::VInterpNormalRotationTo(
                        CurrentDirection,
                        DesiredDirection,
                        DeltaTime,
                        Follower.TurnRate
                    );
                }
                
                // Update position
                FVector Movement = NewDirection * Follower.CurrentSpeed * DeltaTime;
                FVector NewLocation = CurrentPos + Movement;
                Transform.SetLocation(NewLocation);
                
                // Update rotation to face movement direction
                if (!NewDirection.IsNearlyZero())
                {
                    FRotator NewRotation = NewDirection.Rotation();
                    Transform.SetRotation(NewRotation);
                }
            }
        });
}

FVector UMassFollowerProcessor::GetTargetPosition(const FFollowerFragment& Follower,
                                                   FMassEntityManager& EntityManager) const
{
    if (!Follower.Target.IsValid())
        return FVector::ZeroVector;
    
    // Get target transform
    const FTransformFragment* TargetTransform = EntityManager.GetFragmentDataPtr<FTransformFragment>(Follower.Target);
    if (!TargetTransform)
        return FVector::ZeroVector;
    
    FVector TargetPos = TargetTransform->GetLocation();
    
    // Apply prediction if enabled
    if (Follower.bPredictTargetMovement)
    {
        // Get target velocity if available
        const FVelocityFragment* TargetVelocity = EntityManager.GetFragmentDataPtr<FVelocityFragment>(Follower.Target);
        if (TargetVelocity)
        {
            // Predict where target will be
            FVector PredictedOffset = TargetVelocity->Velocity * Follower.PredictionTime;
            TargetPos += PredictedOffset;
        }
    }
    
    return TargetPos;
}
```

### 5.4 Fragment Configuration

```cpp
// FollowerFragmentConfig.h
#pragma once
#include "MassEntityConfigAsset.h"
#include "FollowerFragmentConfig.generated.h"

UCLASS()
class LAMENT_API UFollowerFragmentConfig : public UMassFragmentConfig
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, Category = "Follower")
    float FollowSpeed = 300.0f;

    UPROPERTY(EditAnywhere, Category = "Follower")
    float StoppingDistance = 50.0f;

    UPROPERTY(EditAnywhere, Category = "Follower")
    float TurnRate = 360.0f;

    UPROPERTY(EditAnywhere, Category = "Follower")
    float Acceleration = 0.0f;

    UPROPERTY(EditAnywhere, Category = "Follower")
    bool bPredictTargetMovement = false;

    UPROPERTY(EditAnywhere, Category = "Follower", meta = (EditCondition = "bPredictTargetMovement"))
    float PredictionTime = 0.5f;

    virtual void AddToEntity(FMassEntityManager& EntityManager,
                            FMassEntityHandle Entity) const override
    {
        FFollowerFragment& Fragment = EntityManager.AddFragmentToEntity<FFollowerFragment>(Entity);
        Fragment.FollowSpeed = FollowSpeed;
        Fragment.StoppingDistance = StoppingDistance;
        Fragment.TurnRate = TurnRate;
        Fragment.Acceleration = Acceleration;
        Fragment.bPredictTargetMovement = bPredictTargetMovement;
        Fragment.PredictionTime = PredictionTime;
        
        // PRODUCTION NOTE: Set Target at spawn time
        // Fragment.Target = PlayerEntity;
    }
};
```

---

## 6. Trigger System Deep Dive

The trigger system allows entities to switch between different behaviors based on conditions.

### 6.1 Trigger System Architecture

```
Trigger Evaluation Flow (UMassTriggerProcessor):

For each entity with FTriggerStateFragment:
    1. Get current state from RuleSet
    2. Evaluate all triggers for current state
    3. If trigger condition met:
        a. Transition to new state
        b. Add/remove fragments per new state
        c. Add/remove processor tags
    4. Update time in state
```

### 6.2 FTriggerStateFragment (Expanded)

```cpp
// TriggerStateFragment.h
#pragma once
#include "MassEntityTypes.h"
#include "GameplayTagContainer.h"
#include "TriggerStateFragment.generated.h"

class UTriggerRuleSet;

/**
 * Manages entity state machine.
 * Evaluated by UMassTriggerProcessor each frame.
 */
USTRUCT()
struct LAMENT_API FTriggerStateFragment : public FMassFragment
{
    GENERATED_BODY()

    // Current state index
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

    // Custom data for state-specific logic
    UPROPERTY()
    TMap<FName, float> CustomData;

    // Helpers
    bool HasChangedState() const { return CurrentStateIndex != PreviousStateIndex; }
    void ResetStateTime() { TimeInState = 0.0f; PreviousStateIndex = CurrentStateIndex; }
};
```

### 6.3 Trigger Rule Set

```cpp
// TriggerRuleSet.h
#pragma once
#include "Engine/DataAsset.h"
#include "GameplayTagContainer.h"
#include "TriggerRuleSet.generated.h"

/**
 * Trigger types supported by the system.
 */
UENUM(BlueprintType)
enum class ETriggerType : uint8
{
    None,
    Timer,                  // Time in state > threshold
    PlayerProximity,        // Distance to player
    LineOfSight,           // Can see player
    HealthThreshold,       // Health % reaches value
    Random,                // Random chance each frame
    OnHit,                 // When damaged
    OnDeath,               // When health reaches 0
    Sequential,            // After completing action
    Custom                 // Custom condition (per-entity)
};

/**
 * Single trigger condition.
 */
USTRUCT(BlueprintType)
struct FTriggerCondition
{
    GENERATED_BODY()

    // Type of trigger
    UPROPERTY(EditAnywhere)
    ETriggerType TriggerType = ETriggerType::None;

    // Threshold value (meaning depends on trigger type)
    // Timer: seconds
    // Proximity: units
    // Health: percentage (0-1)
    // Random: probability (0-1)
    UPROPERTY(EditAnywhere)
    float Threshold = 0.0f;

    // State to transition to if condition met
    UPROPERTY(EditAnywhere)
    int32 TargetStateIndex = 0;

    // Optional: Invert condition (NOT)
    UPROPERTY(EditAnywhere)
    bool bInvertCondition = false;
};

/**
 * Single behavior state.
 */
USTRUCT(BlueprintType)
struct FBehaviorState
{
    GENERATED_BODY()

    // State name (for debugging)
    UPROPERTY(EditAnywhere)
    FString StateName = TEXT("Unnamed State");

    // Fragments to add when entering this state
    UPROPERTY(EditAnywhere)
    TArray<FGameplayTag> FragmentsToAdd;

    // Fragments to remove when entering this state
    UPROPERTY(EditAnywhere)
    TArray<FGameplayTag> FragmentsToRemove;

    // Processor tags to enable
    UPROPERTY(EditAnywhere)
    TArray<FGameplayTag> ProcessorTagsToAdd;

    // Processor tags to disable
    UPROPERTY(EditAnywhere)
    TArray<FGameplayTag> ProcessorTagsToRemove;

    // Triggers to evaluate while in this state
    UPROPERTY(EditAnywhere)
    TArray<FTriggerCondition> Triggers;
};

/**
 * Data asset defining entity state machine.
 */
UCLASS()
class LAMENT_API UTriggerRuleSet : public UDataAsset
{
    GENERATED_BODY()

public:
    // All states for this entity
    UPROPERTY(EditAnywhere, Category = "States")
    TArray<FBehaviorState> States;

    // Initial state index
    UPROPERTY(EditAnywhere, Category = "States")
    int32 InitialStateIndex = 0;

    // Helper: Get state by index
    const FBehaviorState* GetState(int32 StateIndex) const
    {
        if (States.IsValidIndex(StateIndex))
            return &States[StateIndex];
        return nullptr;
    }
};
```

### 6.4 UMassTriggerProcessor Implementation

```cpp
// MassTriggerProcessor.h
#pragma once
#include "MassProcessor.h"
#include "MassTriggerProcessor.generated.h"

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
    
    // Trigger evaluation
    bool EvaluateTrigger(const FMassEntityHandle Entity,
                        const FTriggerCondition& Condition,
                        const FTriggerStateFragment& StateFragment,
                        FMassEntityManager& EntityManager,
                        FMassExecutionContext& Context) const;
    
    // State transitions
    void TransitionToState(FMassEntityHandle Entity,
                          int32 NewStateIndex,
                          FTriggerStateFragment& StateFragment,
                          FMassEntityManager& EntityManager,
                          FMassExecutionContext& Context) const;
    
    // Helper: Get player entity
    FMassEntityHandle GetPlayerEntity(UWorld* World) const;
};
```

```cpp
// MassTriggerProcessor.cpp
#include "MassTriggerProcessor.h"
#include "MassCommonFragments.h"
#include "MassCommandBuffer.h"

UMassTriggerProcessor::UMassTriggerProcessor()
{
    // Run early, before movement processors
    ExecutionOrder.ExecuteInGroup = UE::Mass::ProcessorGroupNames::PreMovement;
}

void UMassTriggerProcessor::ConfigureQueries()
{
    EntityQuery.AddRequirement<FTriggerStateFragment>(EMassFragmentAccess::ReadWrite);
    EntityQuery.AddRequirement<FTransformFragment>(EMassFragmentAccess::ReadOnly);
}

void UMassTriggerProcessor::Execute(FMassEntityManager& EntityManager, 
                                     FMassExecutionContext& Context)
{
    const float DeltaTime = Context.GetDeltaTimeSeconds();
    UWorld* World = Context.GetWorld();
    FMassEntityHandle PlayerEntity = GetPlayerEntity(World);
    
    // Deferred commands for fragment add/remove
    FMassCommandBuffer& CommandBuffer = Context.Defer();
    
    EntityQuery.ForEachEntityChunk(EntityManager, Context, 
        [DeltaTime, &EntityManager, &CommandBuffer, PlayerEntity, this](FMassExecutionContext& Context)
        {
            const int32 NumEntities = Context.GetNumEntities();
            
            TArrayView<FTriggerStateFragment> StateFragments = Context.GetMutableFragmentView<FTriggerStateFragment>();
            TConstArrayView<FTransformFragment> Transforms = Context.GetFragmentView<FTransformFragment>();
            
            for (int32 i = 0; i < NumEntities; ++i)
            {
                FTriggerStateFragment& StateFragment = StateFragments[i];
                FMassEntityHandle Entity = Context.GetEntity(i);
                
                // Skip if no rule set
                if (!StateFragment.RuleSet)
                    continue;
                
                // Update time in state
                StateFragment.TimeInState += DeltaTime;
                
                // Get current state
                const FBehaviorState* CurrentState = StateFragment.RuleSet->GetState(StateFragment.CurrentStateIndex);
                if (!CurrentState)
                    continue;
                
                // Evaluate triggers
                for (const FTriggerCondition& Trigger : CurrentState->Triggers)
                {
                    bool bConditionMet = EvaluateTrigger(Entity, Trigger, StateFragment, EntityManager, Context);
                    
                    // Invert if requested
                    if (Trigger.bInvertCondition)
                        bConditionMet = !bConditionMet;
                    
                    // Transition if triggered
                    if (bConditionMet)
                    {
                        TransitionToState(Entity, Trigger.TargetStateIndex, StateFragment, EntityManager, Context);
                        break; // Only one trigger per frame
                    }
                }
            }
        });
}

bool UMassTriggerProcessor::EvaluateTrigger(const FMassEntityHandle Entity,
                                             const FTriggerCondition& Condition,
                                             const FTriggerStateFragment& StateFragment,
                                             FMassEntityManager& EntityManager,
                                             FMassExecutionContext& Context) const
{
    switch (Condition.TriggerType)
    {
        case ETriggerType::Timer:
        {
            return StateFragment.TimeInState >= Condition.Threshold;
        }
        
        case ETriggerType::PlayerProximity:
        {
            // Get entity and player positions
            const FTransformFragment* EntityTransform = EntityManager.GetFragmentDataPtr<FTransformFragment>(Entity);
            FMassEntityHandle PlayerEntity = GetPlayerEntity(Context.GetWorld());
            const FTransformFragment* PlayerTransform = EntityManager.GetFragmentDataPtr<FTransformFragment>(PlayerEntity);
            
            if (EntityTransform && PlayerTransform)
            {
                float DistanceSq = FVector::DistSquared(
                    EntityTransform->GetLocation(),
                    PlayerTransform->GetLocation()
                );
                float ThresholdSq = Condition.Threshold * Condition.Threshold;
                return DistanceSq <= ThresholdSq;
            }
            return false;
        }
        
        case ETriggerType::LineOfSight:
        {
            // PRODUCTION NOTE: Check perception fragment for LOS data
            // For now, simplified implementation
            const FPerceptionFragment* Perception = EntityManager.GetFragmentDataPtr<FPerceptionFragment>(Entity);
            if (Perception)
            {
                return Perception->bHasLineOfSight;
            }
            return false;
        }
        
        case ETriggerType::HealthThreshold:
        {
            const FHealthFragment* Health = EntityManager.GetFragmentDataPtr<FHealthFragment>(Entity);
            if (Health)
            {
                float HealthPercent = Health->GetHealthPercent();
                return HealthPercent <= Condition.Threshold;
            }
            return false;
        }
        
        case ETriggerType::Random:
        {
            // Random chance each frame
            return FMath::FRand() < Condition.Threshold;
        }
        
        case ETriggerType::OnDeath:
        {
            const FHealthFragment* Health = EntityManager.GetFragmentDataPtr<FHealthFragment>(Entity);
            if (Health)
            {
                return Health->bIsDead;
            }
            return false;
        }
        
        default:
            return false;
    }
}

void UMassTriggerProcessor::TransitionToState(FMassEntityHandle Entity,
                                               int32 NewStateIndex,
                                               FTriggerStateFragment& StateFragment,
                                               FMassEntityManager& EntityManager,
                                               FMassExecutionContext& Context) const
{
    if (NewStateIndex == StateFragment.CurrentStateIndex)
        return; // Already in target state
    
    const FBehaviorState* NewState = StateFragment.RuleSet->GetState(NewStateIndex);
    if (!NewState)
        return;
    
    // Update state
    StateFragment.PreviousStateIndex = StateFragment.CurrentStateIndex;
    StateFragment.CurrentStateIndex = NewStateIndex;
    StateFragment.ResetStateTime();
    
    // PRODUCTION NOTE: Add/remove fragments based on NewState
    // This requires mapping FGameplayTags to fragment types
    // Deferred to prevent modification during iteration
    
    FMassCommandBuffer& CommandBuffer = Context.Defer();
    
    // Example: Add/remove processor tags
    for (const FGameplayTag& Tag : NewState->ProcessorTagsToAdd)
    {
        CommandBuffer.AddTag(Entity, Tag);
    }
    for (const FGameplayTag& Tag : NewState->ProcessorTagsToRemove)
    {
        CommandBuffer.RemoveTag(Entity, Tag);
    }
}

FMassEntityHandle UMassTriggerProcessor::GetPlayerEntity(UWorld* World) const
{
    // PRODUCTION NOTE: Cache player entity handle in processor or world subsystem
    // For now, return invalid handle
    return FMassEntityHandle();
}
```

### 6.5 Using Triggers in Data Assets

**Example: Shadow Stalker Trigger Setup**

```cpp
// In UTriggerRuleSet data asset (Content/DataAssets/Enemies/DA_ShadowStalkerTriggers)

States:
  [0] "Observed" (Invulnerable, Stationary):
    ProcessorTagsToAdd: [ActiveFloaterTag, InvulnerableTag]
    ProcessorTagsToRemove: [ActiveFollowerTag]
    Triggers:
      - Type: LineOfSight
        Threshold: 0 (false)
        TargetState: 1
        bInvert: true (trigger when NOT in LOS)
  
  [1] "Stalking" (Vulnerable, Following):
    ProcessorTagsToAdd: [ActiveFollowerTag, ActiveFloaterTag]
    ProcessorTagsToRemove: [InvulnerableTag]
    Triggers:
      - Type: LineOfSight
        Threshold: 1 (true)
        TargetState: 0
        bInvert: false (trigger when in LOS)
```

---

## 7. State Machine Patterns

Common trigger patterns for different entity behaviors.

### 7.1 Simple Two-State (Idle → Chase)

```
State 0: Idle
  Trigger: PlayerProximity < 500 → State 1

State 1: Chase
  Trigger: PlayerProximity > 800 → State 0
```

### 7.2 Three-State (Patrol → Chase → Attack)

```
State 0: Patrol (Pacer)
  Trigger: PlayerProximity < 400 → State 1

State 1: Chase (Follower)
  Trigger: PlayerProximity < 100 → State 2
  Trigger: PlayerProximity > 600 → State 0

State 2: Attack (Stationary + Emitter)
  Trigger: Timer > 3.0 → State 1
```

### 7.3 Boss Phase Transitions

```
State 0: Phase 1 (Normal behavior)
  Trigger: Health < 0.66 → State 1

State 1: Phase 2 (Faster, more aggressive)
  Trigger: Health < 0.33 → State 2

State 2: Phase 3 (Enraged, new attacks)
  Trigger: OnDeath → State 3

State 3: Death (Explode, spawn minions)
```

---

## 8. Complete Entity Example: Shadow Stalker

Full implementation of a complex enemy with triggers.

### 8.1 Design Spec

**Concept:** Ghost that only moves when unseen

**Attributes:**
- Floater (always bobbing)
- GeoIgnore (passes through walls)
- Follower (when not observed)
- Invulnerable (when observed)

**Triggers:**
- Player looks at it → Stationary + Invulnerable
- Player looks away → Follower + Vulnerable

### 8.2 Fragment Setup

Entity has these fragments:
- `FTransformFragment`
- `FFloaterFragment` (always active)
- `FFollowerFragment` (conditionally active)
- `FGeoIgnoreFragment` (always active)
- `FInvulnerableFragment` (conditionally present)
- `FHealthFragment`
- `FPerceptionFragment` (for LOS tracking)
- `FTriggerStateFragment`

### 8.3 Archetype Configuration

```cpp
// ShadowStalkerArchetype Data Asset

Fragments:
  - FloaterConfig:
      FloatHeight: 150
      BobSpeed: 1.5
      BobAmplitude: 30
  
  - FollowerConfig:
      FollowSpeed: 250
      TurnRate: 180
      StoppingDistance: 100
  
  - HealthConfig:
      MaxHealth: 30
  
  - TriggerStateConfig:
      RuleSet: DA_ShadowStalkerTriggers

TriggerRuleSet (DA_ShadowStalkerTriggers):
  States:
    [0] "Observed":
      ProcessorTagsToAdd: [InvulnerableTag]
      ProcessorTagsToRemove: [ActiveFollowerTag]
      Triggers:
        - LineOfSight: false → State 1
    
    [1] "Stalking":
      ProcessorTagsToAdd: [ActiveFollowerTag]
      ProcessorTagsToRemove: [InvulnerableTag]
      Triggers:
        - LineOfSight: true → State 0
```

### 8.4 Behavior

1. **Player looks at Shadow Stalker:**
   - Trigger evaluates: LineOfSight == true
   - Transitions to State 0 ("Observed")
   - Adds InvulnerableTag (cannot take damage)
   - Removes ActiveFollowerTag (stops chasing)
   - Only FloaterProcessor runs (bobs in place)

2. **Player looks away:**
   - Trigger evaluates: LineOfSight == false
   - Transitions to State 1 ("Stalking")
   - Removes InvulnerableTag (can take damage)
   - Adds ActiveFollowerTag (starts chasing)
   - FloaterProcessor + FollowerProcessor run (chases while bobbing)

3. **Player shoots while not looking:**
   - Entity takes damage (vulnerable)
   - Health decreases
   - If killed, death trigger fires (can spawn loot, VFX, etc.)

---

## Summary

**What You've Learned:**
- 20+ movement fragments (Floater, Follower, Waver, Dasher, etc.)
- Movement processor implementation pattern
- Complete Floater system (fragment + processor + config)
- Complete Follower system (with target prediction)
- Trigger system architecture (state machines, condition evaluation)
- Trigger rule sets and behavior states
- Common state machine patterns
- Complete entity example (Shadow Stalker with LOS-based behavior)

**Next Steps:**
- Read `MassEntity_CombatSystems.md` for abilities (Emitter, Splitter, Exploder)
- Read `MassEntity_AdvancedSystems.md` for VFX, optimization, and production features
- See `MassEntity_AttributeReference.md` for complete fragment catalog

**Key Takeaways:**
- Multiple movement fragments can coexist on one entity
- Triggers enable/disable processors via tags
- State machines are data-driven (no code required for new behaviors)
- Combine movement + triggers = emergent complexity

---

**Document Version:** 1.0  
**Last Updated:** December 2024  
**UE Version:** 5.7+
