# 3D Art Pipeline Testing Plan - Summer Forest Scene

**Project:** Lament  
**Purpose:** Comprehensive testing of 3D art pipeline with forest assets  
**Timeline:** ~4 weeks  
**Asset Packs:**
- Summer Forest Pack: https://www.fab.com/listings/842f8137-94b0-4a0c-9a11-e918a0d1158d
- Ultra Dynamic Sky: https://www.fab.com/listings/84fda27a-c79f-49c9-8458-82401fb37cfb

**Related Documentation:**
- [[Materials3D]] - Master material system architecture
- [[Pipeline3D]] - 3D asset workflow
- [[Lighting]] - Lighting approach testing framework
- [[PostProcessing]] - Film effects and post-processing
- [[ColorPalettes]] - Color palette definitions

---

## Performance Targets

- **Switch 2:** 30 FPS
- **PS5/Xbox Series X:** 60 FPS
- **PC:** 60+ FPS

---

## Testing Scope

**Testing:**
- ✅ 3D environment assets (trees, rocks, foliage)
- ✅ Master material system with solid color albedo
- ✅ Three lighting approaches (Naturalistic, Cel-Shaded, Hybrid)
- ✅ Post-processing effects (grain, vignette, LUT, bloom)
- ✅ Sky and weather system integration
- ✅ Material assignment automation (C++)

**Skipping for Now:**
- ❌ 2D sprite assets (separate testing phase)
- ❌ Edge mutation materials (experimental - test later)
- ❌ Runtime palette swapping (implement if needed later)

---

# Phase 1: Initial Setup & Preparation

## Step 1.1: Project Setup

**Create Test Level:**
1. Content Browser → Levels
2. Create new level: `ArtTest_SummerForest`
3. Save in `/Content/Levels/ArtTests/`

**Create Folder Structure:**
```
/Content/
├── ArtTests/
│   └── ForestScene/
├── Materials/
│   ├── Master/
│   ├── Instances/
│   ├── PostProcess/
│   └── MPC_ColorPalettes (Material Parameter Collection)
├── Blueprints/
│   └── Utilities/
├── PostProcess/
└── Levels/
    └── ArtTests/
```

**Setup Commands:**
```
In Content Browser:
1. Create folder structure above
2. Enable "Show Engine Content" in View Options
3. Enable "Show Plugin Content" in View Options
```

---

## Step 1.2: Asset Acquisition & Import

### **Download Assets:**
1. Summer Forest Pack from FAB
2. Ultra Dynamic Sky from FAB

### **Import Summer Forest Pack:**

1. Content Browser → Right-click → Import to Game
2. Select all FBX files from Summer Forest Pack
3. **Import Settings:**
   ```
   Mesh:
   - Skeletal Mesh: False (Static Mesh)
   - Import Materials: True (we'll replace, but useful for reference)
   - Import Textures: True (reference only)
   
   Transform:
   - Import Uniform Scale: 1.0 (or adjust if needed)
   
   Mesh:
   - Auto Generate Collision: True
   - Generate Lightmap UVs: True
   
   Normals:
   - Import Normals: True (keep for lighting depth)
   - Import Tangents: True
   ```

4. Import to `/Content/ArtTests/ForestScene/Meshes/`

### **Import/Install Ultra Dynamic Sky:**

1. Follow plugin installation instructions
2. Verify installation in Plugins window
3. Test in empty level to ensure it works

### **Validate Imports:**

**Check:**
- [ ] All meshes imported without errors (check Output Log)
- [ ] Meshes visible in viewport at correct scale
- [ ] No missing textures warnings
- [ ] Collision generated correctly (test with collision view)
- [ ] Normal maps present (if included in pack)

**Document:**
- Total triangle count range (lowest/highest poly assets)
- Number of material slots per asset type
- Texture resolutions (baseline before simplification)

**✓ CHECKPOINT: Import Validation**
- All assets visible and correctly scaled?
- No import errors or corruption?
- Sky system functional?

---

# Phase 2: Master Material Creation

## Implementation Approach

**Architecture:**
- **Master Material** (`M_Master_3D`) - Full-featured material with all parameters
- **Material Instances** - Per-asset type instances with specific colors
- **Post-Process Material** (`PP_CelShading`) - For cel-shading lighting approach
- **Material Parameter Collection** (`MPC_ColorPalettes`) - Palette color storage
- **C++ Utility** - Automated material assignment

---

## Step 2.1: Create Master Material (`M_Master_3D`)

### **Create Material:**
1. Content Browser → `/Content/Materials/Master/`
2. Right-click → Material → Name: `M_Master_3D`
3. Double-click to open Material Editor

### **Material Properties:**
In Details panel (select main material node):
- **Material Domain:** Surface
- **Blend Mode:** Opaque
- **Shading Model:** Default Lit
- **Two Sided:** Unchecked (control per instance as needed)

### **Create Parameters:**

#### **Color & Palette Group**
```
Right-click in graph → Scalar/Vector Parameter:

1. Vector Parameter: "BaseColor"
   - Default: (0.5, 0.5, 0.5, 1.0)
   - Group: "Color and Palette"
   - Description: "Primary solid color for this asset"

2. Scalar Parameter: "PaletteID"
   - Default: 0
   - Group: "Color and Palette"
   - Description: "Which palette set to use (future: runtime swapping)"

3. Static Switch Parameter: "UsePaletteSystem"
   - Default: False
   - Group: "Color and Palette"
   - Description: "Enable palette lookup from MPC (future feature)"
```

#### **Albedo Source Group**
```
4. Static Switch Parameter: "UseAlbedoTexture"
   - Default: False
   - Group: "Albedo Source"
   - Description: "Use texture instead of solid color"

5. Texture Object Parameter: "AlbedoTexture"
   - Default: None
   - Sampler Type: Color
   - Group: "Albedo Source"
   - Description: "Albedo texture map (when UseAlbedoTexture = true)"

6. Static Switch Parameter: "TexturePaletteTint"
   - Default: False
   - Group: "Albedo Source"
   - Description: "Apply palette color as tint to texture"

7. Scalar Parameter: "TextureTintStrength"
   - Default: 0.5
   - Slider Min: 0.0
   - Slider Max: 1.0
   - Group: "Albedo Source"
   - Description: "How much palette affects texture (0=none, 1=full)"
```

#### **Lighting Response Group**
```
8. Scalar Parameter: "Roughness"
   - Default: 0.7
   - Slider Min: 0.0
   - Slider Max: 1.0
   - Group: "Lighting Response"
   - Description: "Surface roughness (0=smooth, 1=rough)"

9. Scalar Parameter: "Metallic"
   - Default: 0.0
   - Slider Min: 0.0
   - Slider Max: 1.0
   - Group: "Lighting Response"
   - Description: "Metallic property (typically 0 for matte)"

10. Scalar Parameter: "Specular"
    - Default: 0.5
    - Slider Min: 0.0
    - Slider Max: 1.0
    - Group: "Lighting Response"
    - Description: "Specular highlight strength"
```

#### **Normal Map Group**
```
11. Static Switch Parameter: "UseNormalMap"
    - Default: True (recommended even with solid colors)
    - Group: "Normal Mapping"
    - Description: "Use normal map for lighting detail"

12. Texture Object Parameter: "NormalMap"
    - Default: None
    - Sampler Type: Normal
    - Group: "Normal Mapping"
    - Description: "Normal map texture"
```

#### **Advanced Group**
```
13. Vector Parameter: "EmissiveColor"
    - Default: (0, 0, 0, 1)
    - Group: "Advanced"
    - Description: "Glow color for special effects"

14. Scalar Parameter: "EmissiveIntensity"
    - Default: 0.0
    - Group: "Advanced"
    - Description: "Glow strength"

15. Scalar Parameter: "Opacity"
    - Default: 1.0
    - Slider Min: 0.0
    - Slider Max: 1.0
    - Group: "Advanced"
    - Description: "Transparency (for special cases)"
```

---

### **Build Material Graph:**

#### **Base Color Logic:**

**Node Setup:**
```
SECTION A: TEXTURE vs SOLID COLOR
================================

1. Create "Static Switch" node
   Name: "UseAlbedoTexture_Switch"
   
2. Connect "UseAlbedoTexture" parameter → Switch input

3. FALSE Branch (Solid Color):
   ├─ Create another "Static Switch" node
   │  Name: "UsePaletteSystem_Switch"
   │  Connect "UsePaletteSystem" parameter → Switch
   │
   ├─ FALSE Branch: Connect "BaseColor" parameter
   │  (Manual color control - recommended for testing)
   │
   └─ TRUE Branch: [Future: MPC lookup]
      For now: Connect "BaseColor" parameter
      (We'll add MPC integration later if needed)

4. TRUE Branch (Texture):
   ├─ Create "Texture Coordinate" node → UVs
   │
   ├─ Create "Texture Sample" node
   │  Connect "AlbedoTexture" parameter → Texture pin
   │  Connect Texture Coordinate → UVs pin
   │
   ├─ Create "Static Switch" node
   │  Name: "TexturePaletteTint_Switch"
   │  Connect "TexturePaletteTint" parameter → Switch
   │
   ├─ FALSE Branch (No Tint):
   │  Connect Texture Sample RGB
   │
   └─ TRUE Branch (Palette Tint):
      ├─ Create "Multiply" node
      │  A: Texture Sample RGB
      │  B: "BaseColor" parameter
      │
      ├─ Create "Lerp" node
      │  A: Texture Sample RGB (original)
      │  B: Multiply result (tinted)
      │  Alpha: "TextureTintStrength" parameter
      │
      └─ Connect Lerp output

5. Final Color Output:
   Connect UseAlbedoTexture_Switch result → [Goes to Base Color pin]
```

**Visual Flow Diagram:**
```
                        ┌─ FALSE → BaseColor (manual)
UsePaletteSystem ───────┤
                        └─ TRUE → BaseColor (future: MPC)
                                    │
                                    ▼
                        ┌─ FALSE → Color from above
UseAlbedoTexture ───────┤
                        └─ TRUE → TextureSample ───┬─ FALSE → RGB
                                                    │
                                  TexturePaletteTint┤
                                                    └─ TRUE → Lerp(
                                                                RGB,
                                                                RGB * BaseColor,
                                                                TintStrength
                                                              )
                                    │
                                    ▼
                              BASE COLOR OUTPUT
```

---

#### **Normal Map Logic:**

```
1. Create "Static Switch" node
   Name: "UseNormalMap_Switch"
   Connect "UseNormalMap" parameter → Switch

2. FALSE Branch:
   Leave disconnected (uses vertex normals)

3. TRUE Branch:
   ├─ Create "Texture Coordinate" node
   ├─ Create "Texture Sample" node
   │  Texture: "NormalMap" parameter
   │  UVs: Texture Coordinate
   │  Sampler Type: Normal (set in texture parameter)
   └─ Connect RGB → Normal output pin

4. Connect Switch result → Normal pin on material output
```

---

#### **Material Outputs:**

```
Connect to Final Material Node:

Base Color:
└─ UseAlbedoTexture_Switch final output

Metallic:
└─ "Metallic" parameter

Specular:
└─ "Specular" parameter

Roughness:
└─ "Roughness" parameter

Normal:
└─ UseNormalMap_Switch output (or leave empty)

Emissive Color:
└─ Create "Multiply" node:
   ├─ "EmissiveColor" parameter
   └─ "EmissiveIntensity" parameter

Opacity:
└─ "Opacity" parameter (only if Blend Mode = Translucent)
```

---

### **Compile and Test:**

1. Click **"Apply"** button
2. Wait for shader compilation (check progress bar)
3. Check **Output Log** for errors
4. Review **Stats** panel:
   - Shader Instructions should be moderate (~100-300 for this material)
   - Texture Samplers: 2-3 (albedo + normal)
5. Click **"Save"**

**✓ CHECKPOINT: Master Material Validation**
- [ ] Compiles without errors
- [ ] All parameters visible in material editor
- [ ] Shader complexity acceptable
- [ ] Ready to create instances

---

## Step 2.2: Create Material Parameter Collection

### **Create MPC:**

1. Content Browser → `/Content/Materials/`
2. Right-click → Miscellaneous → **Material Parameter Collection**
3. Name: `MPC_ColorPalettes`
4. Double-click to open

### **Add Summer Forest Palette Colors:**

Click **"+"** to add Vector Parameters:

```
Palette 0 - Summer Forest (Analogous Green):
============================================

1. Name: "Palette0_Foliage"
   Default Value: X=0.416, Y=0.541, Z=0.353, W=1.0
   // #6A8A5A - Primary foliage color

2. Name: "Palette0_Ground"
   Default Value: X=0.541, Y=0.478, Z=0.314, W=1.0
   // #8A7A50 - Ground/dirt color

3. Name: "Palette0_Shadow"
   Default Value: X=0.227, Y=0.271, Z=0.188, W=1.0
   // #3A4530 - Deep shadow color

4. Name: "Palette0_Highlight"
   Default Value: X=0.690, Y=0.784, Z=0.627, W=1.0
   // #B0C8A0 - Highlight/accent color

5. Name: "Palette0_TreeBark"
   Default Value: X=0.416, Y=0.353, Z=0.282, W=1.0
   // #6A5A48 - Tree bark brown

6. Name: "Palette0_Rock"
   Default Value: X=0.353, Y=0.353, Z=0.314, W=1.0
   // #5A5A50 - Rock gray-green
```

**Conversion Formula (Hex to Linear RGB):**
```
For hex color #RRGGBB:
- R_Linear = (RR in decimal) / 255
- G_Linear = (GG in decimal) / 255
- B_Linear = (BB in decimal) / 255
- W = 1.0 (alpha)

Example: #6A8A5A
- R = 0x6A = 106 → 106/255 = 0.416
- G = 0x8A = 138 → 138/255 = 0.541
- B = 0x5A = 90  → 90/255 = 0.353
```

### **Reserve Future Palettes:**

Add placeholder parameters (leave at default gray):
```
Palette1_Color1 through Palette1_Color6
Palette2_Color1 through Palette2_Color6
etc.
```

**Purpose:**
- MPC stores all palette colors in one place
- Easy reference when setting Material Instance colors
- Future: Can enable runtime palette swapping via Blueprint/C++

**Note:** For testing, we won't connect MPC to master material yet. We'll manually set `BaseColor` in each Material Instance using these color values as reference.

---

## Step 2.3: Create Material Instances

### **Create Base Instance:**

1. Right-click `M_Master_3D` → **Create Material Instance**
2. Name: `MI_Environment`
3. Save in `/Content/Materials/Instances/`
4. Double-click to open

### **Configure Base Instance:**

Check boxes to override these parameters:
```
Color and Palette:
- BaseColor: (0.5, 0.5, 0.5) - neutral gray (will override in child instances)
- UsePaletteSystem: FALSE

Albedo Source:
- UseAlbedoTexture: FALSE
- TexturePaletteTint: FALSE

Lighting Response:
- Roughness: 0.7 (matte default)
- Metallic: 0.0 (non-metallic)
- Specular: 0.5 (moderate)

Normal Mapping:
- UseNormalMap: FALSE (enable per instance if needed)

Advanced:
- EmissiveIntensity: 0.0 (no glow)
```

Click **"Save"**

---

### **Create Specific Asset Instances:**

Create Material Instances **from** `MI_Environment` (right-click → Create Material Instance):

#### **1. Tree Foliage Material**
```
Name: MI_Environment_Tree_Foliage
Parent: MI_Environment
Location: /Content/Materials/Instances/

Override Parameters:
- BaseColor: (0.416, 0.541, 0.353) // #6A8A5A
- Roughness: 0.8 (very matte leaves)
- UseNormalMap: TRUE (if foliage has normal maps)
```

#### **2. Tree Bark Material**
```
Name: MI_Environment_Tree_Bark
Parent: MI_Environment

Override Parameters:
- BaseColor: (0.416, 0.353, 0.282) // #6A5A48
- Roughness: 0.7 (matte bark)
- UseNormalMap: TRUE
```

#### **3. Rock Material**
```
Name: MI_Environment_Rock
Parent: MI_Environment

Override Parameters:
- BaseColor: (0.353, 0.353, 0.314) // #5A5A50
- Roughness: 0.6 (slightly less matte)
- UseNormalMap: TRUE
```

#### **4. Ground Material**
```
Name: MI_Environment_Ground
Parent: MI_Environment

Override Parameters:
- BaseColor: (0.541, 0.478, 0.314) // #8A7A50
- Roughness: 0.75 (fairly matte)
- UseNormalMap: TRUE (if terrain has normals)
```

#### **5. Grass/Foliage Material**
```
Name: MI_Environment_Grass
Parent: MI_Environment

Override Parameters:
- BaseColor: (0.690, 0.784, 0.627) // #B0C8A0 (highlight color)
- Roughness: 0.85 (very matte)
- UseNormalMap: TRUE
- Two-Sided: TRUE (may need to enable in material properties)
```

---

### **Test Material Instances:**

1. Create test scene with basic shapes (cubes, spheres)
2. Apply each material instance to a different shape
3. Add basic directional light
4. Verify:
   - [ ] Colors display correctly
   - [ ] Roughness affects shininess
   - [ ] Normal maps work (if enabled)
   - [ ] Can adjust parameters and see changes

**✓ CHECKPOINT: Material Instances Ready**
- [ ] All instances created and saved
- [ ] Colors match palette
- [ ] Parameters override correctly
- [ ] Test meshes display materials properly

---

## Step 2.4: Create Post-Process Material for Cel-Shading

This will be used for **Lighting Approach B** testing.

### **Create Post-Process Material:**

1. Content Browser → `/Content/Materials/PostProcess/`
2. Right-click → Material → Name: `PP_CelShading`
3. Double-click to open

### **Material Properties:**

In Details panel:
- **Material Domain:** Post Process
- **Blendable Location:** Before Tonemapping
- **Shading Model:** Unlit

### **Create Parameters:**

```
1. Scalar Parameter: "CelSteps"
   - Default: 3
   - Slider Min: 2
   - Slider Max: 8
   - Group: "Cel-Shading"
   - Description: "Number of color bands (2=two-tone, 3=tri-tone, etc.)"

2. Scalar Parameter: "Intensity"
   - Default: 1.0
   - Slider Min: 0.0
   - Slider Max: 1.0
   - Group: "Cel-Shading"
   - Description: "Blend between original and cel-shaded (0=off, 1=full)"

3. Vector Parameter: "OutlineColor"
   - Default: (0, 0, 0, 1) - Black
   - Group: "Cel-Shading"
   - Description: "Color for edge outlines"

4. Scalar Parameter: "OutlineThickness"
   - Default: 1.0
   - Slider Min: 0.0
   - Slider Max: 5.0
   - Group: "Cel-Shading"
   - Description: "Thickness of outlines (0=none)"
```

### **Build Post-Process Graph:**

#### **Section 1: Posterization (Color Quantization)**

```
1. Create "SceneTexture:PostProcessInput0" node
   (Gets current scene color)

2. Create "Custom" node for posterization:
   Name: "Posterize"
   
   Code:
   ```hlsl
   // Posterize - Quantize colors into discrete steps
   // Inputs: Color (float3), Steps (float)
   // Output: float3
   
   float3 posterized;
   posterized.r = floor(Color.r * Steps) / Steps;
   posterized.g = floor(Color.g * Steps) / Steps;
   posterized.b = floor(Color.b * Steps) / Steps;
   return posterized;
   ```
   
   Inputs:
   - Color (Vector3): Connect PostProcessInput0 RGB
   - Steps (Float1): Connect "CelSteps" parameter

3. Output: Posterized color (quantized)
```

#### **Section 2: Edge Detection (Optional - Start Simple)**

```
For initial testing, skip edge detection.
Can add later if cel-shading approach is chosen.

Future implementation:
- Sample Scene Depth at current pixel
- Sample at offset pixels (neighbors)
- Compare depth differences
- If difference > threshold → draw outline
```

#### **Section 3: Final Blend**

```
1. Create "Lerp" node
   A: PostProcessInput0 RGB (original scene)
   B: Posterized color (from Custom node)
   Alpha: "Intensity" parameter

2. Connect Lerp result → Emissive Color output pin
```

**Simplified Graph Flow:**
```
SceneTexture:PostProcessInput0 (original)
            │
            ├─────────────────┐
            │                 │
            ▼                 │
    Custom Posterize          │
    (Color, CelSteps)         │
            │                 │
            ▼                 │
         Lerp ◄───────────────┘
      (Original, Posterized, Intensity)
            │
            ▼
      Emissive Color
```

### **Compile and Save:**

1. Click **"Apply"**
2. Check for errors in Output Log
3. Click **"Save"**

**Note:** We'll add this to a Post-Process Volume during Phase 5 (Lighting Testing)

**✓ CHECKPOINT: Post-Process Material Ready**
- [ ] Material compiles without errors
- [ ] Posterization effect works (test by adding to post-process volume)
- [ ] Intensity parameter blends effect on/off
- [ ] Ready for lighting approach testing

---

# Phase 3: C++ Material Assignment Utility

## Step 3.1: Create C++ Files

### **File Structure:**
```
/Source/Lament/
├── Public/
│   └── EditorUtilities/
│       └── MaterialAssignmentUtility.h
└── Private/
    └── EditorUtilities/
        └── MaterialAssignmentUtility.cpp
```

### **Update Build Configuration:**

**Lament.Build.cs:**
```csharp
// Lament.Build.cs
using UnrealBuildTool;

public class Lament : ModuleRules
{
    public Lament(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[] { 
            "Core", 
            "CoreUObject", 
            "Engine", 
            "InputCore" 
        });

        PrivateDependencyModuleNames.AddRange(new string[] { });

        // For editor-only utilities
        if (Target.bBuildEditor)
        {
            PrivateDependencyModuleNames.AddRange(new string[] { 
                "UnrealEd",
                "Blutility"
            });
        }
    }
}
```

---

### **MaterialAssignmentUtility.h:**

```cpp
// MaterialAssignmentUtility.h
#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Engine/StaticMeshActor.h"
#include "Materials/MaterialInstance.h"
#include "Materials/MaterialInstanceConstant.h"
#include "MaterialAssignmentUtility.generated.h"

/**
 * Editor utility for automatically assigning materials to static mesh actors
 * based on their names and types.
 */
UCLASS()
class LAMENT_API UMaterialAssignmentUtility : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    /**
     * Automatically assigns materials to static mesh actors based on asset name matching.
     * 
     * @param TargetActors - Array of actors to process
     * @param MaterialMapping - Map of search strings to material instances
     *                          Example: "Tree" -> MI_Environment_Tree_Foliage
     * @param bLogAssignments - Whether to log assignments to console
     * @return Number of materials assigned
     */
    UFUNCTION(BlueprintCallable, Category = "Material Assignment", meta = (WorldContext = "WorldContextObject"))
    static int32 AutoAssignMaterialsToActors(
        UObject* WorldContextObject,
        const TArray<AActor*>& TargetActors,
        const TMap<FString, UMaterialInstance*>& MaterialMapping,
        bool bLogAssignments = true
    );

    /**
     * Assigns materials to all static mesh actors in the current level.
     * 
     * @param WorldContextObject - World context
     * @param MaterialMapping - Map of search strings to material instances
     * @param bLogAssignments - Whether to log assignments to console
     * @return Number of materials assigned
     */
    UFUNCTION(BlueprintCallable, Category = "Material Assignment", meta = (WorldContext = "WorldContextObject"))
    static int32 AutoAssignMaterialsInLevel(
        UObject* WorldContextObject,
        const TMap<FString, UMaterialInstance*>& MaterialMapping,
        bool bLogAssignments = true
    );

    /**
     * Batch sets a vector parameter on multiple material instances.
     * 
     * @param MaterialInstances - Array of material instances to modify
     * @param ParameterName - Name of the parameter to set
     * @param Value - Value to set
     */
    UFUNCTION(BlueprintCallable, Category = "Material Assignment")
    static void BatchSetVectorParameter(
        const TArray<UMaterialInstanceDynamic*>& MaterialInstances,
        FName ParameterName,
        FLinearColor Value
    );

    /**
     * Batch sets a scalar parameter on multiple material instances.
     * 
     * @param MaterialInstances - Array of material instances to modify
     * @param ParameterName - Name of the parameter to set
     * @param Value - Value to set
     */
    UFUNCTION(BlueprintCallable, Category = "Material Assignment")
    static void BatchSetScalarParameter(
        const TArray<UMaterialInstanceDynamic*>& MaterialInstances,
        FName ParameterName,
        float Value
    );

    /**
     * Creates material instance dynamic copies from material instance constants.
     * Useful for runtime parameter modification.
     * 
     * @param SourceMaterial - Material instance constant to copy
     * @param Outer - Outer object (usually the actor or component)
     * @return Newly created material instance dynamic
     */
    UFUNCTION(BlueprintCallable, Category = "Material Assignment")
    static UMaterialInstanceDynamic* CreateDynamicMaterialInstance(
        UMaterialInstance* SourceMaterial,
        UObject* Outer
    );

private:
    /**
     * Helper: Finds the best matching material for a given asset name.
     * 
     * @param AssetName - Name of the asset (e.g., "SM_Oak_Tree_01")
     * @param MaterialMapping - Map of search strings to materials
     * @return Matched material instance, or nullptr if no match found
     */
    static UMaterialInstance* FindMatchingMaterial(
        const FString& AssetName,
        const TMap<FString, UMaterialInstance*>& MaterialMapping
    );

    /**
     * Helper: Assigns material to a static mesh component, handling all material slots.
     * 
     * @param MeshComponent - Component to assign material to
     * @param Material - Material to assign
     * @param bAllSlots - If true, assigns to all material slots; if false, only slot 0
     * @return Number of slots assigned
     */
    static int32 AssignMaterialToComponent(
        UStaticMeshComponent* MeshComponent,
        UMaterialInstance* Material,
        bool bAllSlots = true
    );
};
```

---

### **MaterialAssignmentUtility.cpp:**

```cpp
// MaterialAssignmentUtility.cpp
#include "EditorUtilities/MaterialAssignmentUtility.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInstanceDynamic.h"

int32 UMaterialAssignmentUtility::AutoAssignMaterialsToActors(
    UObject* WorldContextObject,
    const TArray<AActor*>& TargetActors,
    const TMap<FString, UMaterialInstance*>& MaterialMapping,
    bool bLogAssignments)
{
    if (!WorldContextObject || TargetActors.Num() == 0 || MaterialMapping.Num() == 0)
    {
        UE_LOG(LogTemp, Warning, TEXT("AutoAssignMaterialsToActors: Invalid input parameters"));
        return 0;
    }

    int32 AssignmentCount = 0;

    for (AActor* Actor : TargetActors)
    {
        if (!Actor) continue;

        // Get all static mesh components from the actor
        TArray<UStaticMeshComponent*> MeshComponents;
        Actor->GetComponents<UStaticMeshComponent>(MeshComponents);

        for (UStaticMeshComponent* MeshComp : MeshComponents)
        {
            if (!MeshComp || !MeshComp->GetStaticMesh()) continue;

            // Get the mesh name
            FString MeshName = MeshComp->GetStaticMesh()->GetName();
            
            // Find matching material
            UMaterialInstance* MatchedMaterial = FindMatchingMaterial(MeshName, MaterialMapping);
            
            if (MatchedMaterial)
            {
                int32 SlotsAssigned = AssignMaterialToComponent(MeshComp, MatchedMaterial, true);
                AssignmentCount += SlotsAssigned;

                if (bLogAssignments)
                {
                    UE_LOG(LogTemp, Log, TEXT("Assigned '%s' to '%s' (%d slots)"),
                        *MatchedMaterial->GetName(),
                        *Actor->GetName(),
                        SlotsAssigned);
                }
            }
            else if (bLogAssignments)
            {
                UE_LOG(LogTemp, Warning, TEXT("No matching material found for '%s'"), *MeshName);
            }
        }
    }

    if (bLogAssignments)
    {
        UE_LOG(LogTemp, Log, TEXT("Material assignment complete: %d materials assigned"), AssignmentCount);
    }

    return AssignmentCount;
}

int32 UMaterialAssignmentUtility::AutoAssignMaterialsInLevel(
    UObject* WorldContextObject,
    const TMap<FString, UMaterialInstance*>& MaterialMapping,
    bool bLogAssignments)
{
    UWorld* World = GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::LogAndReturnNull);
    if (!World)
    {
        UE_LOG(LogTemp, Error, TEXT("AutoAssignMaterialsInLevel: Invalid world context"));
        return 0;
    }

    // Gather all static mesh actors in the level
    TArray<AActor*> AllActors;
    for (TActorIterator<AStaticMeshActor> ActorItr(World); ActorItr; ++ActorItr)
    {
        AllActors.Add(*ActorItr);
    }

    if (bLogAssignments)
    {
        UE_LOG(LogTemp, Log, TEXT("Found %d static mesh actors in level"), AllActors.Num());
    }

    return AutoAssignMaterialsToActors(WorldContextObject, AllActors, MaterialMapping, bLogAssignments);
}

void UMaterialAssignmentUtility::BatchSetVectorParameter(
    const TArray<UMaterialInstanceDynamic*>& MaterialInstances,
    FName ParameterName,
    FLinearColor Value)
{
    for (UMaterialInstanceDynamic* MatInstance : MaterialInstances)
    {
        if (MatInstance)
        {
            MatInstance->SetVectorParameterValue(ParameterName, Value);
        }
    }

    UE_LOG(LogTemp, Log, TEXT("Set vector parameter '%s' on %d material instances"),
        *ParameterName.ToString(),
        MaterialInstances.Num());
}

void UMaterialAssignmentUtility::BatchSetScalarParameter(
    const TArray<UMaterialInstanceDynamic*>& MaterialInstances,
    FName ParameterName,
    float Value)
{
    for (UMaterialInstanceDynamic* MatInstance : MaterialInstances)
    {
        if (MatInstance)
        {
            MatInstance->SetScalarParameterValue(ParameterName, Value);
        }
    }

    UE_LOG(LogTemp, Log, TEXT("Set scalar parameter '%s' on %d material instances"),
        *ParameterName.ToString(),
        MaterialInstances.Num());
}

UMaterialInstanceDynamic* UMaterialAssignmentUtility::CreateDynamicMaterialInstance(
    UMaterialInstance* SourceMaterial,
    UObject* Outer)
{
    if (!SourceMaterial)
    {
        UE_LOG(LogTemp, Warning, TEXT("CreateDynamicMaterialInstance: Source material is null"));
        return nullptr;
    }

    UMaterialInstanceDynamic* DynamicMaterial = UMaterialInstanceDynamic::Create(SourceMaterial, Outer);
    
    if (!DynamicMaterial)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed to create dynamic material instance from '%s'"),
            *SourceMaterial->GetName());
    }

    return DynamicMaterial;
}

UMaterialInstance* UMaterialAssignmentUtility::FindMatchingMaterial(
    const FString& AssetName,
    const TMap<FString, UMaterialInstance*>& MaterialMapping)
{
    // Try to find the best match based on keywords in asset name
    // Priority: More specific matches first (longer keywords)
    
    TArray<FString> Keys;
    MaterialMapping.GetKeys(Keys);
    
    // Sort by key length (descending) to prioritize specific matches
    Keys.Sort([](const FString& A, const FString& B) {
        return A.Len() > B.Len();
    });

    for (const FString& Key : Keys)
    {
        if (AssetName.Contains(Key, ESearchCase::IgnoreCase))
        {
            return MaterialMapping[Key];
        }
    }

    return nullptr;
}

int32 UMaterialAssignmentUtility::AssignMaterialToComponent(
    UStaticMeshComponent* MeshComponent,
    UMaterialInstance* Material,
    bool bAllSlots)
{
    if (!MeshComponent || !Material) return 0;

    int32 NumMaterials = MeshComponent->GetNumMaterials();
    int32 AssignedCount = 0;

    if (bAllSlots)
    {
        // Assign to all material slots
        for (int32 i = 0; i < NumMaterials; ++i)
        {
            MeshComponent->SetMaterial(i, Material);
            AssignedCount++;
        }
    }
    else
    {
        // Assign only to slot 0
        MeshComponent->SetMaterial(0, Material);
        AssignedCount = 1;
    }

    return AssignedCount;
}
```

---

## Step 3.2: Compile C++ Code

1. Close Unreal Editor
2. Right-click `Lament.uproject` → Generate Visual Studio project files
3. Open `Lament.sln` in Visual Studio
4. Build Solution (Build → Build Solution or Ctrl+Shift+B)
5. Check for compilation errors
6. Launch Unreal Editor from Visual Studio (Debug → Start Debugging or F5)

**✓ Checkpoint: C++ Compilation**
- [ ] Code compiles without errors
- [ ] Editor launches successfully
- [ ] Functions visible in Blueprint (search for "Auto Assign Materials")

---

## Step 3.3: Create Blueprint Helper (Optional UI)

For easier access to C++ functions:

1. Content Browser → `/Content/Blueprints/Utilities/`
2. Right-click → Editor Utilities → Editor Utility Widget
3. Name: `EUW_MaterialAssigner`
4. Open the widget

### **Design UI:**

Add widgets:
```
Vertical Box
├─ Text Block: "Material Assignment Utility"
├─ Horizontal Box
│  ├─ Text: "Tree Material:"
│  └─ Object Field (Material Instance): TreeMaterial
├─ Horizontal Box
│  ├─ Text: "Rock Material:"
│  └─ Object Field (Material Instance): RockMaterial
├─ Horizontal Box
│  ├─ Text: "Grass Material:"
│  └─ Object Field (Material Instance): GrassMaterial
├─ Horizontal Box
│  ├─ Text: "Ground Material:"
│  └─ Object Field (Material Instance): GroundMaterial
└─ Button: "Assign Materials to Level"
   └─ On Clicked Event
```

### **Wire Button Event:**

In Graph:
```
On Button Clicked
│
├─ Make Map (String → Material Instance)
│  ├─ Add: "Tree" → TreeMaterial variable
│  ├─ Add: "Oak" → TreeMaterial variable
│  ├─ Add: "Pine" → TreeMaterial variable
│  ├─ Add: "Bark" → TreeMaterial variable
│  ├─ Add: "Foliage" → TreeMaterial variable
│  ├─ Add: "Rock" → RockMaterial variable
│  ├─ Add: "Stone" → RockMaterial variable
│  ├─ Add: "Boulder" → RockMaterial variable
│  ├─ Add: "Grass" → GrassMaterial variable
│  ├─ Add: "Ground" → GroundMaterial variable
│  └─ Add: "Terrain" → GroundMaterial variable
│
└─ Auto Assign Materials In Level (C++ function)
   ├─ Material Mapping: Map from above
   └─ Log Assignments: TRUE
```

### **Usage:**

1. Run Editor Utility Widget (right-click → Run Editor Utility Widget)
2. Set material references in UI
3. Click "Assign Materials to Level"
4. Check Output Log for results

---

# Phase 4: Scene Composition

## Step 4.1: Build Test Scene

### **Scene Layout:**

1. Open `ArtTest_SummerForest` level
2. Delete default objects (if any)

### **Add Ground Plane:**

```
1. Place Plane or Landscape
   - Scale: 100, 100, 1 (large flat surface)
   - Location: 0, 0, 0

2. Assign MI_Environment_Ground material
```

### **Place Forest Assets:**

```
Placement Strategy:
- Foreground: 2-3 large trees, 1-2 rocks
- Midground: 5-7 trees of varying types, 2-3 rocks
- Background: 3-5 trees (can be smaller/distant)

Asset Distribution:
- Trees: 10-15 total
  - Mix types if pack has oak, pine, birch, etc.
- Rocks: 5-8 total
  - Vary sizes
- Grass/Foliage: Scattered throughout
- Props: 2-3 (logs, stumps if available)

Layout Tips:
- Avoid grid placement (organic randomness)
- Create depth with layering
- Group some assets (natural clustering)
- Leave open spaces (don't overfill)
```

### **Camera Setup:**

```
1. Place Camera Actor
   Location: (-500, 0, 100) - looking at scene center
   Rotation: Pitch 0, Yaw 0, Roll 0

2. Create additional camera positions:
   - Wide shot (shows full scene)
   - Close-up (shows material detail)
   - Mid shot (composition)

3. Save camera bookmarks (Ctrl+1, Ctrl+2, etc.)
```

**✓ CHECKPOINT: Scene Composition**
- [ ] Scene has good variety of assets
- [ ] Depth established (foreground/midground/background)
- [ ] Camera positions set and bookmarked
- [ ] Assets placed but materials not yet assigned (we'll use C++ utility next)

---

## Step 4.2: Assign Materials Using C++ Utility

### **Option A: Via Editor Utility Widget**

1. Run `EUW_MaterialAssigner`
2. Set material references:
   - Tree Material: `MI_Environment_Tree_Foliage`
   - Rock Material: `MI_Environment_Rock`
   - Grass Material: `MI_Environment_Grass`
   - Ground Material: `MI_Environment_Ground`
3. Click "Assign Materials to Level"
4. Check Output Log for results

### **Option B: Via Level Blueprint**

```
1. Open Level Blueprint (Blueprints → Open Level Blueprint)

2. Create Event:
   Custom Event: "AssignSceneMaterials"

3. Add nodes:
   ├─ Make Map (String → Material Instance)
   │  ├─ "Tree" → MI_Environment_Tree_Foliage
   │  ├─ "Bark" → MI_Environment_Tree_Bark
   │  ├─ "Foliage" → MI_Environment_Tree_Foliage
   │  ├─ "Rock" → MI_Environment_Rock
   │  ├─ "Grass" → MI_Environment_Grass
   │  └─ "Ground" → MI_Environment_Ground
   │
   └─ Auto Assign Materials In Level
      ├─ Material Mapping: Map from above
      └─ Log Assignments: TRUE

4. Right-click event → Execute (manually trigger)
   OR connect to BeginPlay for auto-assignment
```

### **Manual Assignment (If Needed):**

If automated assignment doesn't work perfectly:
1. Select assets in viewport
2. Details panel → Materials → Override material slots
3. Set appropriate Material Instance

**✓ CHECKPOINT: Materials Assigned**
- [ ] All assets have appropriate solid-color materials
- [ ] Colors match palette (forest green, brown, gray)
- [ ] No default gray materials remaining
- [ ] Ready for lighting tests

---

## Step 4.3: Configure Ultra Dynamic Sky

### **Add Ultra Dynamic Sky:**

1. Content Browser → Search "Ultra Dynamic Sky"
2. Drag `BP_Ultra_Dynamic_Sky` into level
3. Location: 0, 0, 0 (or anywhere - it's environment)

### **Configure Sky Settings:**

In BP_Ultra_Dynamic_Sky Details panel:
```
Time of Day:
- Time of Day: 15.0 (3:00 PM - late afternoon)
- Day Length: 20.0 minutes (for testing - adjust as needed)
- Animate Time of Day: FALSE (static for testing)

Sun:
- Sun Brightness: 10.0 (moderate)
- Sun Angle: Controlled by Time of Day
- Sun Color: Leave default (warm afternoon)

Sky:
- Cloud Coverage: 0.3 (partial clouds)
- Cloud Speed: 0.5 (slow drift)
- Sky Mode: Volumetric (if performance allows) or Static

Fog:
- Fog Density: 0.01 (subtle atmospheric fog)
- Fog Height Falloff: 0.2

Weather:
- Weather: Clear (start with clear, test variations later)
```

### **Test Sky System:**

1. Play in Editor (Alt+P)
2. Verify:
   - [ ] Sky renders correctly
   - [ ] Sun position appropriate for time of day
   - [ ] Clouds visible and look good
   - [ ] Fog adds atmosphere
3. Stop Play

### **Create Sky Presets:**

Document settings for different scenarios:
```
Preset 1: Late Afternoon (Testing Default)
- Time: 15.0
- Cloud Coverage: 0.3
- Weather: Clear

Preset 2: Overcast Day
- Time: 12.0
- Cloud Coverage: 0.8
- Weather: Overcast

Preset 3: Dawn
- Time: 6.0
- Cloud Coverage: 0.2
- Weather: Clear

Preset 4: Dusk
- Time: 19.0
- Cloud Coverage: 0.4
- Weather: Clear

Preset 5: Night
- Time: 1.0
- Cloud Coverage: 0.1
- Weather: Clear
```

**✓ CHECKPOINT: Sky System Ready**
- [ ] Ultra Dynamic Sky functional
- [ ] Late afternoon lighting configured
- [ ] Presets documented for later testing
- [ ] Scene ready for lighting approach testing

---

# Phase 5: Lighting Testing (Three Approaches)

## Step 5.1: Duplicate Scene for Each Approach

### **Create Duplicates:**

1. Save current level
2. File → Save Current As...
   - `ArtTest_SummerForest_Naturalistic`
3. Open `ArtTest_SummerForest_Naturalistic`
4. File → Save Current As...
   - `ArtTest_SummerForest_CelShaded`
5. Open `ArtTest_SummerForest_Naturalistic`
6. File → Save Current As...
   - `ArtTest_SummerForest_Hybrid`

**Result:** Three identical scenes for parallel testing

---

## Step 5.2: Approach A - Naturalistic Lighting

**Scene:** `ArtTest_SummerForest_Naturalistic`

### **Setup Lighting:**

#### **Primary Light: Directional Light (Sun)**

```
1. Ultra Dynamic Sky already provides directional light
   OR
2. Add Directional Light manually:
   
Settings:
- Intensity: 5.0 lux (moderate afternoon sun)
- Light Color: (255, 245, 230) - Warm white
- Temperature: 5500K (warm afternoon)
- Source Radius: 0.5 (soft shadows)
- Source Angle: 1.0 (sun angular size)

Shadow Settings:
- Cast Shadows: TRUE
- Dynamic Shadow Distance: 20000
- Cascade Distribution Exponent: 3.0

Transform:
- Rotation: 
  - Pitch: -45 (angled down)
  - Yaw: 45 (side lighting for depth)
  - Roll: 0
```

#### **Fill Light: Sky Light**

```
1. Add Sky Light (if not already present from Ultra Dynamic Sky)

Settings:
- Intensity: 1.0
- Light Color: (230, 240, 255) - Cool blue (sky)
- Source Type: Captured Scene (or SLS Captured Scene)
- Lower Hemisphere: (20, 25, 30) - Dark blue-gray

Capture Settings:
- Recapture Scene (to update with current sky)
```

#### **Optional Accent Lights:**

```
If scene feels flat, add subtle fill:

Point Light (near camera):
- Intensity: 0.5
- Color: (255, 240, 220) - Warm fill
- Attenuation Radius: 5000
- Falloff Exponent: 2.0
```

### **Material Settings (Verify):**

All materials should have:
```
- EnableCelShading: FALSE (standard PBR)
- Roughness: 0.6-0.8 range
- Metallic: 0.0
- UseNormalMap: TRUE (for lighting depth)
```

### **Lighting Build:**

```
1. Build → Build Lighting Only
   OR
2. Build → Build Lighting Quality: Production

Wait for build to complete.
```

### **Capture Reference Screenshots:**

From each camera bookmark:
```
1. Press camera bookmark hotkey (1, 2, 3, etc.)
2. High Res Screenshot:
   - Console: `HighResShot 2` (2x resolution)
   - Or use screenshot tool
3. Save as:
   - `Naturalistic_Wide_[Date].png`
   - `Naturalistic_Close_[Date].png`
   - `Naturalistic_Mid_[Date].png`
```

**✓ CHECKPOINT: Naturalistic Lighting Complete**
- [ ] Directional light provides main illumination
- [ ] Sky light provides ambient fill
- [ ] Shadows visible and appropriate softness
- [ ] Materials respond correctly to PBR lighting
- [ ] Screenshots captured for comparison

---

## Step 5.3: Approach B - Cel-Shaded Lighting

**Scene:** `ArtTest_SummerForest_CelShaded`

### **Setup Same Base Lighting:**

Use identical light setup as Naturalistic (Directional + Sky Light)

### **Add Post-Process Volume:**

```
1. Place: Modes Panel → Volumes → Post Process Volume
2. Location: Anywhere in scene
3. Settings:
   - Infinite Extent (Unbound): TRUE
   - Priority: 1
   - Blend Weight: 1.0
```

### **Add Cel-Shading Post-Process Material:**

```
In Post Process Volume Details:
1. Rendering Features → Post Process Materials
2. Array → Add Element
3. Asset Reference: PP_CelShading
```

### **Configure Cel-Shading Parameters:**

```
In Post Process Volume → Overrides:
Check "Blendables" and configure PP_CelShading:

Parameters:
- CelSteps: 3 (tri-tone: highlight, mid, shadow)
- Intensity: 1.0 (full effect)
- OutlineThickness: 0.0 (skip outlines for now)
- OutlineColor: (0, 0, 0)

Test different CelSteps values:
- 2: Two-tone (very graphic)
- 3: Tri-tone (recommended)
- 4: Four-tone (more gradual)
- 5+: Closer to naturalistic
```

### **Adjust Material Settings (If Needed):**

Materials can stay the same, or optionally adjust:
```
- Roughness: Can increase (0.9) for flatter look
- Specular: Can reduce (0.3) for less shine
```

### **Test Variations:**

```
Variation 1: Subtle Cel (Blend)
- Intensity: 0.5
- Blends 50% between naturalistic and cel

Variation 2: Full Cel
- Intensity: 1.0
- Pure posterization

Variation 3: High Steps
- CelSteps: 5
- Smoother gradations
```

### **Capture Screenshots:**

Same camera positions as Naturalistic:
```
- `CelShaded_Wide_[Date].png`
- `CelShaded_Close_[Date].png`
- `CelShaded_Mid_[Date].png`

Capture multiple variations:
- `CelShaded_Steps2_[Date].png`
- `CelShaded_Steps3_[Date].png`
- `CelShaded_Steps4_[Date].png`
```

**✓ CHECKPOINT: Cel-Shaded Lighting Complete**
- [ ] Post-process material applies cel-shading
- [ ] Color quantization visible
- [ ] CelSteps parameter controls band count
- [ ] Can toggle Intensity to compare with naturalistic
- [ ] Screenshots captured for comparison

---

## Step 5.4: Approach C - Hybrid Lighting

**Scene:** `ArtTest_SummerForest_Hybrid`

### **Setup Base Lighting:**

Same as Naturalistic and Cel-Shaded approaches.

### **Hybrid Implementation Options:**

#### **Option 1: Selective Post-Process**

```
Apply cel-shading at reduced intensity:
- Add Post Process Volume
- Add PP_CelShading
- Set Intensity: 0.3-0.5 (subtle effect)

Result: Mostly naturalistic with slight posterization
```

#### **Option 2: Material-Based Hybrid**

```
Assign different material instances per asset type:

Naturalistic Materials (standard):
- Trees: MI_Environment_Tree_Bark (EnableCelShading: FALSE)
- Rocks: MI_Environment_Rock (EnableCelShading: FALSE)

Future: If master material has cel-shading blend parameter:
- Ground: Set blend to 0.5
- Props: Set blend to 0.7

For now: Use post-process approach (Option 1)
```

#### **Option 3: Layered Post-Process**

```
1. Add two Post-Process Volumes with different priorities

Volume 1 (Priority 1, covers whole scene):
- PP_CelShading at Intensity 0.3

Volume 2 (Priority 2, bounded around specific area):
- PP_CelShading at Intensity 1.0
- Place around hero tree or focal point

Result: Different areas have different cel intensity
```

### **Recommended Hybrid Setup:**

```
1. Base lighting: Naturalistic (Directional + Sky)
2. Post-process: PP_CelShading at Intensity 0.4
3. Materials: Standard PBR (no changes)

This gives:
- Naturalistic lighting depth and gradients
- Subtle color banding for stylization
- Best of both approaches
```

### **Test Intensity Variations:**

```
- Intensity 0.2: Very subtle (barely noticeable)
- Intensity 0.4: Moderate (recommended)
- Intensity 0.6: Strong hybrid
- Intensity 0.8: Nearly full cel
```

### **Capture Screenshots:**

```
Capture at different intensities:
- `Hybrid_Intensity02_[Date].png`
- `Hybrid_Intensity04_[Date].png`
- `Hybrid_Intensity06_[Date].png`
```

**✓ CHECKPOINT: Hybrid Lighting Complete**
- [ ] Hybrid approach blends naturalistic + cel-shading
- [ ] Intensity parameter allows easy adjustment
- [ ] Retains depth from PBR while adding stylization
- [ ] Screenshots captured for comparison

---

## Step 5.5: Lighting Comparison & Decision

### **Create Comparison Document:**

Create spreadsheet or document with:
```
Columns:
- Approach (Naturalistic, Cel-Shaded, Hybrid)
- Screenshot (embed images)
- Pros
- Cons
- Score (1-5) per criterion
```

### **Evaluation Criteria:**

Use decision matrix from Lighting.md:

| Criteria | Weight | Naturalistic | Cel-Shaded | Hybrid |
|----------|--------|--------------|------------|---------|
| **Mood/Atmosphere** | High (x3) | ___ / 5 | ___ / 5 | ___ / 5 |
| **Art Style Fit** | High (x3) | ___ / 5 | ___ / 5 | ___ / 5 |
| **Visual Quality** | High (x3) | ___ / 5 | ___ / 5 | ___ / 5 |
| **90s Anime Match** | Med (x2) | ___ / 5 | ___ / 5 | ___ / 5 |
| **Performance** | Med (x2) | ___ / 5 | ___ / 5 | ___ / 5 |
| **Ease of Iteration** | Med (x2) | ___ / 5 | ___ / 5 | ___ / 5 |
| **Technical Complexity** | Low (x1) | ___ / 5 | ___ / 5 | ___ / 5 |
| **TOTAL** | | **___** | **___** | **___** |

### **Evaluation Questions:**

**Mood & Atmosphere:**
- Does it support melancholic, moody tone?
- Feels atmospheric and immersive?
- Matches game's emotional goals?

**Art Style Fit:**
- Works with solid-color materials?
- Consistent look across assets?
- Elevates simple geometry?

**Visual Quality:**
- Shape readability clear?
- Depth and form definition good?
- Visually interesting?

**90s Anime Match:**
- Captures 90s anime aesthetic?
- Dramatic shadows and contrast?
- Fits film-inspired look?

**Performance:**
- Frame rate acceptable on target platforms?
- Shadow rendering cost reasonable?
- Post-processing impact acceptable?

**Ease of Iteration:**
- Easy to adjust and tune?
- Can designers/artists control?
- Fast iteration workflow?

**Technical Complexity:**
- Simple to maintain?
- Easy to apply to new assets?
- Robust and stable?

### **Measure Performance:**

In each scene, run these console commands:
```
stat FPS
stat Unit
stat GPU
stat SceneRendering

Record:
- Average FPS
- Frame time (ms)
- GPU time (ms)
- Shadow rendering cost
```

Compare across all three approaches.

### **Make Decision:**

1. Review all screenshots side-by-side
2. Fill out decision matrix
3. Calculate weighted scores
4. Consider performance data
5. Choose approach based on:
   - Highest score
   - Best fit for art direction
   - Acceptable performance
   - Workflow considerations

### **Document Decision:**

Update `Lighting.md`:
```markdown
## Decision Record

**Chosen Approach:** [A/B/C] - [Name]

**Date Decided:** [Date]

**Rationale:**
- [Why this approach was chosen]
- [Key strengths]
- [Trade-offs accepted]

**Final Settings:**
- [Document specific settings]
- [Light parameters]
- [Post-process settings if applicable]

**Performance:**
- Average FPS: [X]
- Frame time: [X] ms
- GPU time: [X] ms
```

**✓ CHECKPOINT: Lighting Decision Made**
- [ ] All three approaches tested and compared
- [ ] Screenshots captured and evaluated
- [ ] Performance measured
- [ ] Decision matrix filled out
- [ ] Final approach chosen and documented
- [ ] Lighting.md updated with decision

---

# Phase 6: Post-Processing Application

**Apply to chosen lighting approach scene.**

## Step 6.1: Create/Configure Post-Process Volume

If not already present:
```
1. Add Post Process Volume
   - Infinite Extent: TRUE
   - Priority: 1
   - Blend Weight: 1.0
```

---

## Step 6.2: Configure Film Grain

In Post Process Volume Details → Film:
```
Enable Override:
☑ Grain Intensity
☑ Grain Jitter
☑ Grain Highlights Intensity
☑ Grain Shadows Intensity

Settings (from PostProcessing.md):
- Grain Intensity: 0.4
- Grain Jitter: 1.0
- Grain Highlights Intensity: 0.2
- Grain Shadows Intensity: 0.6
```

**Test:**
- Play in editor
- Check grain visibility at different distances
- Adjust if too subtle or too strong

---

## Step 6.3: Configure Vignette

In Post Process Volume → Lens → Vignette:
```
Enable Override:
☑ Vignette Intensity

Settings:
- Vignette Intensity: 0.4
```

**Test:**
- Should darken corners subtly
- Not obscure important scene elements
- Natural lens-like effect

---

## Step 6.4: Configure Bloom (Halation)

In Post Process Volume → Lens → Bloom:
```
Enable Override:
☑ Bloom Intensity
☑ Bloom Threshold
☑ Bloom Size
☑ Bloom Tint

Settings:
- Bloom Intensity: 1.0
- Bloom Threshold: 0.8
- Bloom Size: 4.0
- Bloom Tint: (1.0, 0.8, 0.6) - Subtle warm orange
```

**Test:**
- Look at bright highlights (sky through trees, sun)
- Warm glow should be visible
- Not overwhelming

---

## Step 6.5: Find/Create Color Grading LUT

### **Option A: Use Existing Film LUT (Quick)**

```
1. Search online for free film LUT packs:
   - "Cinematic LUT free download"
   - "Film emulation LUT pack"
   - Look for desaturated/muted presets

2. Download LUT (typically .cube format)

3. Import to Unreal:
   - Content Browser → Import
   - Select .cube file
   - Creates LUT texture asset

4. Apply LUT:
   - Post Process Volume → Color Grading → Misc
   - Color Grading LUT: [Your LUT texture]
   - LUT Intensity: 0.8-1.0
```

### **Option B: Create Custom LUT (Recommended)**

```
1. Export Neutral LUT from UE:
   - Content Browser → Right-click in folder
   - Miscellaneous → Color Lookup Table
   - Name: LUT_Neutral
   - Texture Size: 32 (standard)

2. Export LUT texture:
   - Right-click LUT texture → Asset Actions → Export
   - Save as PNG

3. Edit in DaVinci Resolve (or Photoshop):
   
   DaVinci Resolve:
   - Import neutral LUT image
   - Apply color grading:
     • Reduce saturation: -20 to -30
     • Lift blacks slightly (film look): +0.05
     • Roll off highlights: -0.1
     • Add subtle color cast:
       - Shadows: Cool (blue) +2
       - Highlights: Warm (orange) +2
   - Export image (same size, PNG)

4. Re-import to Unreal:
   - Import graded LUT image
   - Creates new LUT texture

5. Apply:
   - Post Process Volume → Color Grading LUT
   - Set intensity: 0.8-1.0
```

### **Recommended LUT Characteristics:**

Based on ColorPalettes.md:
```
- Desaturated: 20-30% saturation reduction
- Cool or warm bias: Depends on scene mood
- Lifted blacks: Not pure black (film characteristic)
- Rolled highlights: Softer whites
- Subtle teal/orange: Classic cinematic look
```

**Test LUT:**
- View with all palette colors
- Ensure colors still readable
- Should enhance, not fight palette
- Check with different times of day (if testing Ultra Dynamic Sky)

---

## Step 6.6: Configure Ambient Occlusion

In Post Process Volume → Rendering Features → Ambient Occlusion:
```
Enable Override:
☑ AO Intensity
☑ AO Radius

Settings:
- AO Intensity: 0.6
- AO Radius: 100.0 (adjust based on scene scale)
```

**Test:**
- Look at crevices (between rocks, tree roots)
- Darkening should add depth
- Helps solid-color materials feel grounded

---

## Step 6.7: Set Exposure

In Post Process Volume → Lens → Exposure:
```
Enable Override:
☑ Metering Mode
☑ Exposure Compensation

Option 1 - Manual (Recommended):
- Metering Mode: Manual
- Exposure Compensation: 0.0 (adjust to taste)
  - Negative: Darker
  - Positive: Brighter

Option 2 - Auto Constrained:
- Metering Mode: Auto Exposure Histogram
- Min Brightness: 0.8
- Max Brightness: 1.2
- Speed Up/Down: 3.0 (moderate adaptation)
```

**Recommendation:** Manual for consistent look across scene.

---

## Step 6.8: Disable Unnecessary Effects

In Post Process Volume, ensure these are OFF:

```
Lens → Depth of Field:
- Depth of Field: Disabled (or Method: None)

Motion Blur:
- Motion Blur Amount: 0.0 (disabled)

Lens → Chromatic Aberration:
- Chromatic Aberration Intensity: 0.0 (disabled)
  OR very subtle: 0.05-0.1

Lens → Lens Distortion:
- Distortion: 0.0 (disabled)
```

**Rationale:**
- DOF obscures clarity during gameplay
- Motion blur can reduce readability
- Chromatic aberration distracting if too strong
- Lens distortion can cause motion sickness

---

## Step 6.9: Document Post-Process Settings

Fill out template from PostProcessing.md:

```markdown
### Global Post-Process Volume Settings

**Film Grain:**
- Intensity: 0.4
- Jitter: 1.0
- Highlights: 0.2
- Shadows: 0.6
- Custom Texture: None (procedural)

**Vignette:**
- Intensity: 0.4
- Falloff: 0.4 (default)
- Color: Black (0, 0, 0)

**Color Grading (LUT):**
- LUT File: [LUT_SummerForest_Desaturated]
- Intensity: 0.85
- Notes: Desaturated, cool shadows, warm highlights

**Bloom (Halation):**
- Intensity: 1.0
- Threshold: 0.8
- Size: 4.0
- Tint: (1.0, 0.8, 0.6) - Warm orange

**Lens Effects:**
- Distortion: Disabled
- Chromatic Aberration: Disabled
- Corner Softness: Via vignette

**Ambient Occlusion:**
- Intensity: 0.6
- Radius: 100.0

**Exposure:**
- Type: Manual
- Compensation: 0.0

**Other:**
- Depth of Field: Disabled
- Motion Blur: Disabled
```

---

## Step 6.10: Capture Final Post-Processed Look

Take comprehensive screenshots:

**Before/After Comparison:**
```
1. Toggle post-process volume on/off
2. Capture same camera angle:
   - Without post: `NoPost_Wide_[Date].png`
   - With post: `WithPost_Wide_[Date].png`
```

**Final Beauty Shots:**
```
From all camera bookmarks:
- `Final_Wide_[Date].png`
- `Final_Close_[Date].png`
- `Final_Mid_[Date].png`

Multiple angles for portfolio:
- Low angle looking up at trees
- High angle overlooking scene
- Through trees (framing)
```

**✓ CHECKPOINT: Post-Processing Complete**
- [ ] All effects configured and tested
- [ ] Film grain adds analog texture
- [ ] Vignette frames scene naturally
- [ ] LUT enhances mood and color palette
- [ ] Bloom/halation adds film-like glow
- [ ] AO adds depth to solid colors
- [ ] Unnecessary effects disabled
- [ ] Settings documented
- [ ] Before/after screenshots captured
- [ ] Performance still acceptable

---

# Phase 7: Weather & Sky Variations Testing

## Step 7.1: Time of Day Variations

Test scene with Ultra Dynamic Sky at different times:

### **Dawn (6:00 AM):**
```
Settings:
- Time of Day: 6.0
- Cloud Coverage: 0.2
- Weather: Clear

Capture:
- `TimeOfDay_Dawn_[Date].png`

Notes:
- Cool blue light
- Long shadows
- Palette colors: Check if they work
```

### **Midday (12:00 PM):**
```
Settings:
- Time of Day: 12.0
- Cloud Coverage: 0.3
- Weather: Clear

Capture:
- `TimeOfDay_Midday_[Date].png`

Notes:
- Bright, high contrast
- Short shadows
- Palette colors: May need brighter?
```

### **Afternoon (15:00 / 3:00 PM):**
```
Already tested - this is your base setup
```

### **Dusk (19:00 / 7:00 PM):**
```
Settings:
- Time of Day: 19.0
- Cloud Coverage: 0.4
- Weather: Clear

Capture:
- `TimeOfDay_Dusk_[Date].png`

Notes:
- Warm golden light
- Long shadows
- Dramatic sky colors
```

### **Night (1:00 AM):**
```
Settings:
- Time of Day: 1.0
- Cloud Coverage: 0.1
- Weather: Clear

Capture:
- `TimeOfDay_Night_[Date].png`

Notes:
- Moonlight (if system supports)
- Very dark - test readability
- May need emissive lights
```

**Evaluation:**
- Do palette colors work across all times?
- Which time of day best fits mood?
- Do materials need time-specific adjustments?
- Is post-processing LUT appropriate for all times?

---

## Step 7.2: Weather Variations

### **Clear Sky:**
```
Already tested - base setup
```

### **Overcast:**
```
Settings:
- Time of Day: 12.0
- Cloud Coverage: 0.8
- Weather: Overcast (if available)

Lighting Changes:
- Softer shadows (more diffuse)
- Lower contrast
- Cooler color temperature

Capture:
- `Weather_Overcast_[Date].png`

Notes:
- Matches Skyrim overcast mood?
- Melancholic atmosphere?
- Colors desaturated enough?
```

### **Rainy (if supported):**
```
Settings:
- Weather: Rain
- Cloud Coverage: 0.9

Additional Effects (if needed):
- Increase wetness on materials (future)
- Add rain particle effects
- Darken overall scene

Capture:
- `Weather_Rain_[Date].png`

Notes:
- Adds dramatic mood
- Test performance with rain particles
```

### **Foggy:**
```
Settings:
- Fog Density: 0.05 (increase from base)
- Fog Height Falloff: 0.1

Or use Exponential Height Fog:
- Fog Density: 0.02
- Fog Inscattering Color: Desaturated blue-gray

Capture:
- `Weather_Foggy_[Date].png`

Notes:
- Atmospheric depth
- Mysterious mood
- Obscures distant objects
```

**Evaluation:**
- Which weather conditions fit game mood?
- Performance impact of weather effects?
- Do materials/lighting need weather-specific adjustments?

---

## Step 7.3: Document Findings

Create weather testing report:

```markdown
## Weather & Time of Day Testing Results

### Recommended Time of Day:
[Late Afternoon / Dusk / etc.]

**Rationale:**
- [Best matches mood]
- [Palette colors work well]
- [Dramatic lighting]

### Weather Recommendations:

**Primary:** [Clear / Overcast / etc.]
- Use for: [Gameplay areas]
- Mood: [Melancholic / etc.]

**Secondary:** [Fog / Rain / etc.]
- Use for: [Special areas]
- Mood: [Mysterious / etc.]

### Adjustments Needed:

**LUT:**
- [Same LUT works for all conditions]
- OR [Need per-weather LUT variants]

**Post-Processing:**
- [Grain intensity adjust for rain?]
- [Bloom adjust for overcast?]

**Materials:**
- [No changes needed]
- OR [Roughness adjust for wet materials?]
```

**✓ CHECKPOINT: Weather Testing Complete**
- [ ] All time of day variations tested
- [ ] All weather conditions tested
- [ ] Screenshots captured
- [ ] Palette colors work across conditions
- [ ] Recommendations documented
- [ ] Performance acceptable for all variations

---

# Phase 8: Performance Testing & Optimization

## Step 8.1: Performance Benchmarking

### **Setup Benchmark Scene:**

```
1. Populate scene with typical asset density:
   - 50+ trees
   - 20+ rocks
   - Grass/foliage across ground
   - Typical gameplay density

2. Ensure all systems active:
   - Materials applied
   - Lighting built
   - Post-processing enabled
   - Weather system running
```

### **Run Performance Tests:**

```
Console Commands:
1. stat FPS
2. stat Unit
3. stat GPU
4. stat RHI
5. stat SceneRendering

Capture data:
- Average FPS (play for 30 seconds, note min/max/avg)
- Frame time (ms)
- GPU time breakdown
- Draw calls
- Shadow rendering cost
```

### **Test Scenarios:**

#### **Baseline (All Features On):**
```
- Materials: Solid color with normal maps
- Lighting: [Chosen approach]
- Post-processing: Full effects
- Weather: Active

Record:
- FPS: ___
- Frame Time: ___ ms
- GPU Time: ___ ms
```

#### **Materials Only:**
```
Disable:
- Post-processing volume
- Complex lighting (just ambient)

Record:
- FPS: ___
- Impact: Materials alone cost ___ ms
```

#### **Lighting Only:**
```
Disable:
- Post-processing
- Use default materials

Record:
- FPS: ___
- Impact: Lighting cost ___ ms
```

#### **Post-Processing Only:**
```
Disable:
- Complex lighting
- Use default materials
- Enable only post-processing

Test each effect individually:
- Grain: ___ ms
- Vignette: ___ ms
- Bloom: ___ ms
- LUT: ___ ms
- AO: ___ ms
- Cel-shading PP (if used): ___ ms

Record total PP cost: ___ ms
```

---

## Step 8.2: Identify Bottlenecks

**Analyze `stat GPU` output:**

Look for expensive categories:
```
- PrePass (depth/shadows): ___ ms
- BasePass (material complexity): ___ ms
- Lighting: ___ ms
- PostProcessing: ___ ms
- Translucency: ___ ms
```

**Common Issues:**

```
High BasePass time:
→ Material complexity too high
→ Check shader instructions in materials
→ Simplify if needed

High PrePass/Shadows:
→ Shadow resolution too high
→ Too many shadow-casting lights
→ Reduce cascade count or resolution

High PostProcessing:
→ Expensive post effects
→ Reduce bloom quality
→ Simplify LUT
→ Disable unnecessary effects

High Draw Calls:
→ Too many unique materials
→ Batch assets with same material
→ Use material instances, not unique materials
```

---

## Step 8.3: Optimization Passes

### **If Performance Below Target:**

#### **Optimization 1: Material Complexity**
```
1. Review M_Master_3D shader stats
2. Simplify if instruction count high (>200)
3. Test without normal maps (compare quality loss)
4. Use static switches to compile out unused features
```

#### **Optimization 2: Lighting**
```
1. Reduce shadow distance: Dynamic Shadow Distance = 10000 (from 20000)
2. Lower shadow resolution: Shadow Map Resolution = 2048 (from 4096)
3. Reduce cascade count: 3 cascades instead of 4
4. Disable shadows on small/distant objects
```

#### **Optimization 3: Post-Processing**
```
1. Reduce bloom quality:
   - Bloom Quality: 3 (from 5)
   
2. Simplify LUT:
   - Use 16x16 LUT instead of 32x32
   
3. Reduce AO quality:
   - AO Quality: 50% (from 100%)
   
4. Test disabling less critical effects:
   - Grain: Disable and compare visual impact
   - Vignette: Very cheap, keep
```

#### **Optimization 4: Asset LODs**
```
1. Check if assets have LODs
2. Generate LODs for high-poly assets
3. Set LOD transition distances
4. Test LOD performance gain
```

---

## Step 8.4: Platform-Specific Testing

### **Target: Switch 2 (30 FPS)**
```
Simulate lower-end hardware:
- Scalability: Low or Medium
- Reduce resolution: 1280x720
- Disable expensive features:
  - AO: Off
  - Bloom quality: Low
  - Shadow quality: Low

Test and measure FPS
Adjust until stable 30 FPS
```

### **Target: PS5/Xbox (60 FPS)**
```
Scalability: High or Epic
Resolution: 1920x1080 or higher
All features enabled

Test and measure FPS
Should comfortably hit 60 FPS
```

### **Target: PC (60+ FPS)**
```
Scalability: Epic
Resolution: 1920x1080+
All features max quality

Test high-end and mid-range PC specs
```

---

## Step 8.5: Document Performance Data

Create performance report:

```markdown
## Performance Benchmark Results

**Scene:** Summer Forest Test Scene
**Asset Count:** 
- Trees: 50
- Rocks: 20
- Grass/Foliage: [Count]

### Baseline Performance (All Features)

**Lighting Approach:** [Naturalistic/Cel/Hybrid]

| Platform | FPS | Frame Time | GPU Time |
|----------|-----|------------|----------|
| PC (High-end) | ___ | ___ ms | ___ ms |
| PC (Mid-range) | ___ | ___ ms | ___ ms |
| PS5/Xbox (Simulated) | ___ | ___ ms | ___ ms |
| Switch 2 (Simulated) | ___ | ___ ms | ___ ms |

### Performance Breakdown

**Materials:** ___ ms
**Lighting:** ___ ms
**Shadows:** ___ ms
**Post-Processing:** ___ ms
**Other:** ___ ms

### Bottlenecks Identified:
- [List any issues]
- [E.g., "Shadow rendering high"]

### Optimizations Applied:
- [List changes made]
- [Performance gain for each]

### Final Performance:
[After optimizations - meets targets? Yes/No]

### Recommendations:
- [For production assets]
- [Settings to use per platform]
```

**✓ CHECKPOINT: Performance Validated**
- [ ] Baseline performance measured
- [ ] All systems benchmarked individually
- [ ] Bottlenecks identified
- [ ] Optimizations applied if needed
- [ ] Meets performance targets for all platforms
- [ ] Results documented

---

# Phase 9: Documentation & Pipeline Validation

## Step 9.1: Update All Documentation

### **Materials3D.md:**

```markdown
## Progress Tracking

### Implementation Status
- [X] Master material created and tested
- [X] Material Parameter Collection set up
- [X] Base Material Instances created (Environment, etc.)
- [X] Color palette system implemented (MPC storage)
- [ ] Albedo texture system implemented and tested (tested, works)
- [X] Texture palette tinting system functional
- [ ] Edge mutation - Skipped for now
- [X] Lighting approach integrated: [Chosen Approach]
- [X] Performance benchmarked and optimized

### Decisions Made
- [X] Palette system approach chosen: MPC (for reference, manual instances for testing)
- [ ] Edge mutation - Deferred to later testing
- [X] Lighting integration: [Naturalistic/Cel/Hybrid]
- [X] Performance acceptable: Yes

### Performance Data
- Master Material Shader Instructions: ___ 
- Typical frame cost: ___ ms
- Performance target met: [Yes/No]
```

### **Lighting.md:**

```markdown
## Decision Record

**Chosen Approach:** [A/B/C] - [Name]

**Date Decided:** [Date]

**Rationale:**
- [Why chosen]
- [Key strengths]
- [Trade-offs]

**Final Settings:**
[Document light parameters, post-process if applicable]

**Performance:**
- Average FPS: ___
- Frame time: ___ ms
- GPU time: ___ ms

**Hybrid Details (if applicable):**
- [Which assets use which approach]
- [Blending strategy]
```

### **PostProcessing.md:**

```markdown
## Settings Profile - Summer Forest Test

[Use template from earlier, fill in all actual values used]

**Film Grain:**
- Intensity: [value]
- Jitter: [value]
- Highlights: [value]
- Shadows: [value]

[etc. for all settings]
```

### **ColorPalettes.md:**

```markdown
## Palette Library

### Summer Forest (Analogous Green)

**Mood/Area:** Natural forest environment, peaceful to melancholic

**Palette Type:** Analogous (Yellow-Green, Green, Blue-Green)

**Color Scheme:**
```
Primary Color: #6A8A5A (Foliage, 25% saturation)
Secondary Color: #8A7A50 (Ground, 28% saturation)
Shadow Color: #3A4530 (Deep Green-Black, 15% saturation)
Highlight Color: #B0C8A0 (Pale Green-Blue, 30% saturation)
Accent (Tree Bark): #6A5A48 (Brown, 20% saturation)
Accent (Rocks): #5A5A50 (Gray-Green, 12% saturation)
```

**Lighting Notes:**
- [Recommended lighting setup]
- [Time of day that works best]

**Post-Processing Notes:**
- LUT: [Which LUT used]
- [Any special adjustments]

**Usage:** Test scene - Summer Forest

**Reference:** Mushishi (analogous natural), Skyrim (desaturation)

**Status:** [X] Finalized
```

### **Pipeline3D.md:**

```markdown
## Progress Tracking

### Technical Decisions
- [X] Polycount guidelines finalized: [Range from asset pack]
- [X] Texture simplification workflow: Material override (solid colors)
- [X] Master material system implemented
- [X] Lighting approach chosen: [Name]
- [ ] Edge mutation tested: Deferred
- [X] Post-processing settings documented

### Tool Selection
- [X] Asset marketplace: FAB (Summer Forest Pack)
- [ ] Texture editing: N/A (using solid colors)
- [ ] Clay-style materials: Deferred

### Pipeline Testing
- [X] First 3D asset completed through full pipeline: [Date]
- [X] Pipeline documentation validated and updated
- [X] Performance benchmarked with typical asset count
- [X] Workflow time estimated: [~2 hours for material setup]

### Asset Categories Completed
- [X] Environment props (trees, rocks)
- [ ] Architecture/structures
- [ ] Characters (2D sprites)
- [ ] Enemies
- [ ] Interactive objects
- [ ] Special effects meshes
```

---

## Step 9.2: Create Workflow Guide

Document the finalized workflow for production:

**File:** `/Documentation/Art/3D_Production_Workflow.md`

```markdown
# 3D Asset Production Workflow (Finalized)

Based on Summer Forest testing phase.

## Quick Reference

**Time per asset:** ~5-10 minutes after initial setup
**Materials:** Use M_Master_3D instances
**Lighting:** [Chosen approach]
**Post-Processing:** See PostProcessing.md settings

## Step-by-Step Process

### 1. Import Asset
- Import FBX with standard settings
- Auto-generate collision
- Import normals: TRUE

### 2. Assign Material
- Use C++ utility: `UMaterialAssignmentUtility::AutoAssignMaterialsInLevel`
- OR manually assign appropriate MI_Environment_[Type]
- Verify material in viewport

### 3. Test in Scene
- Place in test level
- Check with lighting
- Verify performance

### 4. Adjust if Needed
- Override material parameters if specific color needed
- Adjust roughness for asset-specific look

### 5. Mark Complete
- Add to asset library
- Ready for level design use
```

---

## Step 9.3: Create Troubleshooting Guide

**File:** `/Documentation/Art/Troubleshooting.md`

```markdown
# Art Pipeline Troubleshooting

## Common Issues

### Materials appear black
**Cause:** No lights in scene or normal map issue
**Fix:** 
- Add directional light
- Check UseNormalMap setting
- Rebuild lighting

### Colors don't match palette
**Cause:** Material instance not overriding BaseColor
**Fix:**
- Open Material Instance
- Check box next to BaseColor parameter
- Set correct RGB values

### Performance issues
**Cause:** Too many assets or expensive effects
**Fix:**
- Check stat GPU for bottleneck
- Reduce shadow quality
- Lower post-processing quality
- See Performance Testing section

### C++ utility doesn't assign materials
**Cause:** Asset names don't match mapping keywords
**Fix:**
- Check Output Log for "No matching material" warnings
- Add more keywords to mapping
- Or manually assign problematic assets

[Add more issues as discovered]
```

---

## Step 9.4: Capture Portfolio-Quality Screenshots

Final beauty shots for documentation and portfolio:

### **Screenshot Checklist:**

```
Lighting:
- [X] Best time of day selected
- [X] Weather conditions optimal
- [X] Post-processing enabled

Camera:
- [ ] Wide establishing shot
- [ ] Mid shot (shows detail)
- [ ] Close-up (material quality)
- [ ] Cinematic angles
- [ ] Different perspectives

Quality:
- [ ] High resolution (4K if possible)
- [ ] Proper exposure
- [ ] No artifacts or glitches
- [ ] Clean composition
```

### **Capture Commands:**

```
High-resolution screenshot:
- Console: HighResShot 4
- Or: HighResShot 3840x2160

Disable UI:
- Console: ToggleDebugCamera
- Hide all UI elements
```

### **Screenshot Organization:**

```
/Documentation/Art/Screenshots/
├── Testing/
│   ├── Naturalistic/
│   ├── CelShaded/
│   └── Hybrid/
├── PostProcessing/
│   ├── BeforeAfter/
│   └── EffectComparisons/
├── Weather/
│   └── TimeOfDay/
└── Final/
    ├── Portfolio_Wide_01.png
    ├── Portfolio_Mid_01.png
    └── Portfolio_Close_01.png
```

---

## Step 9.5: Lessons Learned Document

**File:** `/Documentation/Art/LessonsLearned.md`

```markdown
# Lessons Learned - Summer Forest Testing

## What Worked Well

### Materials:
- [Solid color approach successful]
- [Master material flexible]
- [Normal maps add depth even with flat albedo]

### Lighting:
- [Chosen approach fits mood perfectly]
- [Easy to iterate and adjust]

### Workflow:
- [C++ utility saved hours of manual work]
- [Material instancing hierarchy works great]

## What Didn't Work

### Issues Encountered:
- [List any problems]
- [E.g., "Initial palette too saturated"]

### Solutions Found:
- [How issues were resolved]

## Changes Made from Original Plan

### Materials:
- [Any deviations from Materials3D.md]

### Lighting:
- [Any adjustments to planned approaches]

### Post-Processing:
- [Settings different from recommendations]

## Recommendations for Production

### Do This:
- [Best practices discovered]
- [Efficient workflows]

### Avoid This:
- [Mistakes to not repeat]
- [Inefficient approaches]

### Future Improvements:
- [Things to add/change for production]
- [Edge mutation testing when ready]
- [Runtime palette swapping if needed]
```

---

## Step 9.6: Final Validation Checklist

Complete final checklist:

```markdown
## 3D Art Pipeline Validation - Final Checklist

### Phase 1: Setup
- [X] Project structure created
- [X] Summer Forest assets imported
- [X] Ultra Dynamic Sky installed and configured

### Phase 2: Materials
- [X] M_Master_3D created and tested
- [X] MPC_ColorPalettes configured
- [X] All material instances created
- [X] PP_CelShading created (for lighting testing)

### Phase 3: Automation
- [X] C++ Material Assignment Utility compiled
- [X] Blueprint helper created (optional)
- [X] Tested on scene assets

### Phase 4: Scene
- [X] Test scene built with variety of assets
- [X] Materials assigned via automation
- [X] Ultra Dynamic Sky configured

### Phase 5: Lighting
- [X] Naturalistic approach tested
- [X] Cel-shaded approach tested
- [X] Hybrid approach tested
- [X] Decision made and documented

### Phase 6: Post-Processing
- [X] Film grain configured
- [X] Vignette configured
- [X] Bloom/halation configured
- [X] LUT created/applied
- [X] AO configured
- [X] Exposure set
- [X] Settings documented

### Phase 7: Weather
- [X] Time of day variations tested
- [X] Weather conditions tested
- [X] Recommendations documented

### Phase 8: Performance
- [X] Baseline performance measured
- [X] Bottlenecks identified
- [X] Optimizations applied
- [X] Target performance met
- [X] Results documented

### Phase 9: Documentation
- [X] All docs updated
- [X] Workflow guide created
- [X] Troubleshooting guide created
- [X] Screenshots captured
- [X] Lessons learned documented

## Pipeline Status: ✅ VALIDATED

**Ready for Production:** [YES/NO]

**Notes:**
[Any caveats or remaining work]
```

---

**✓ FINAL CHECKPOINT: Pipeline Complete**
- [ ] All phases completed
- [ ] All documentation updated
- [ ] Performance targets met
- [ ] Workflow proven and documented
- [ ] Ready to apply to production assets
- [ ] Team can follow documented process

---

# Appendix A: File Reference

## Created Files

### **Materials:**
```
/Content/Materials/Master/
└── M_Master_3D.uasset

/Content/Materials/Instances/
├── MI_Environment.uasset
├── MI_Environment_Tree_Foliage.uasset
├── MI_Environment_Tree_Bark.uasset
├── MI_Environment_Rock.uasset
├── MI_Environment_Ground.uasset
└── MI_Environment_Grass.uasset

/Content/Materials/PostProcess/
└── PP_CelShading.uasset

/Content/Materials/
└── MPC_ColorPalettes.uasset
```

### **C++ Files:**
```
/Source/Lament/Public/EditorUtilities/
└── MaterialAssignmentUtility.h

/Source/Lament/Private/EditorUtilities/
└── MaterialAssignmentUtility.cpp
```

### **Blueprints:**
```
/Content/Blueprints/Utilities/
└── EUW_MaterialAssigner.uasset (optional)
```

### **Levels:**
```
/Content/Levels/ArtTests/
├── ArtTest_SummerForest_Naturalistic.umap
├── ArtTest_SummerForest_CelShaded.umap
└── ArtTest_SummerForest_Hybrid.umap
```

### **Documentation:**
```
/Documentation/Art/
├── 3D_ArtPipeline_TestingPlan.md (this document)
├── 3D_Production_Workflow.md (created in Phase 9)
├── Troubleshooting.md (created in Phase 9)
├── LessonsLearned.md (created in Phase 9)
└── Screenshots/
    ├── Testing/
    ├── PostProcessing/
    ├── Weather/
    └── Final/
```

---

# Appendix B: Quick Command Reference

## Console Commands

### **Performance:**
```
stat FPS          - Show frames per second
stat Unit         - Show frame time breakdown
stat GPU          - Show GPU time breakdown
stat RHI          - Show rendering stats
stat SceneRendering - Detailed scene rendering stats
```

### **Visualization:**
```
viewmode Lit           - Standard lit view
viewmode Unlit         - No lighting
viewmode ShaderComplexity - Material complexity
viewmode LightComplexity  - Lighting cost

show Collision        - Show collision meshes
show Bounds          - Show asset bounds
```

### **Screenshots:**
```
HighResShot 2         - 2x resolution
HighResShot 4         - 4x resolution
HighResShot 3840x2160 - 4K specific resolution
```

### **Lighting:**
```
BuildLighting        - Build lighting
r.Shadow.DistanceScale [0-1] - Scale shadow distance
```

---

# Appendix C: Color Palette Reference

## Summer Forest Palette (RGB 0-1 Range)

```cpp
// For C++ or Blueprint use:
FLinearColor Foliage    = FLinearColor(0.416f, 0.541f, 0.353f, 1.0f);
FLinearColor Ground     = FLinearColor(0.541f, 0.478f, 0.314f, 1.0f);
FLinearColor Shadow     = FLinearColor(0.227f, 0.271f, 0.188f, 1.0f);
FLinearColor Highlight  = FLinearColor(0.690f, 0.784f, 0.627f, 1.0f);
FLinearColor TreeBark   = FLinearColor(0.416f, 0.353f, 0.282f, 1.0f);
FLinearColor Rock       = FLinearColor(0.353f, 0.353f, 0.314f, 1.0f);
```

## Hex to Linear RGB Conversion

```
Formula:
Linear = (Hex_Value_Decimal / 255.0)

Example: #6A8A5A
Hex: 6A = 106, 8A = 138, 5A = 90
Linear: (106/255, 138/255, 90/255) = (0.416, 0.541, 0.353)
```

---

# Appendix D: Estimated Timeline

## Week 1: Foundation
- **Day 1-2:** Phase 1 (Import assets, setup project) - ~8 hours
- **Day 3:** Phase 2 & 3 (Materials + C++) - ~4 hours
- **Day 4-5:** Phase 4 (Scene composition, material assignment) - ~6 hours

**Total: 18 hours / 2.5 days**

## Week 2: Lighting Core
- **Day 1-2:** Phase 5.2 (Naturalistic lighting test) - ~6 hours
- **Day 3-4:** Phase 6 (Post-processing) - ~6 hours
- **Day 5:** Phase 7.1 (Time of day) - ~3 hours

**Total: 15 hours / 2 days**

## Week 3: Lighting Alternatives
- **Day 1-2:** Phase 5.3-5.4 (Cel + Hybrid) - ~8 hours
- **Day 3:** Phase 5.5 (Compare & decide) - ~3 hours
- **Day 4-5:** Phase 7.2 (Weather variations) - ~4 hours

**Total: 15 hours / 2 days**

## Week 4: Polish & Documentation
- **Day 1-2:** Phase 8 (Performance testing) - ~6 hours
- **Day 3-5:** Phase 9 (Documentation, screenshots) - ~8 hours

**Total: 14 hours / 2 days**

---

**Grand Total: ~62 hours (~4 weeks at ~15 hours/week)**

Can be compressed to 2-3 weeks with full-time focus or by skipping some weather variations.

---

# Questions & Support

If you encounter issues during testing:

1. **Check Troubleshooting.md** (created in Phase 9)
2. **Review relevant section** in this testing plan
3. **Check Output Log** for errors/warnings
4. **Compare with documentation** (Materials3D.md, etc.)
5. **Document the issue** for LessonsLearned.md

---

**END OF TESTING PLAN**

**Status:** Ready to Execute  
**Last Updated:** [Date]  
**Version:** 1.0
