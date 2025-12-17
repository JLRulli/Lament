# Naming Conventions

This document defines naming standards for the Lament project across code, documentation, and assets.

---

## Unreal Engine C++ Code

Follow Unreal Engine coding standards strictly.

### Classes

**Format**: `PascalCase` with Unreal prefix

**Prefixes**:
- `A` - Actors (placeable objects in the world)
- `U` - UObjects and components
- `F` - Structs and plain C++ classes
- `E` - Enums
- `I` - Interfaces
- `T` - Templates

**Examples**:
```cpp
APlayerCharacter      // Actor class
AEnemySpawner        // Actor class
UHealthComponent     // Component class
UInventorySystem     // UObject class
FItemData           // Struct
FDamageInfo         // Struct
EWeaponType         // Enum
EGameState          // Enum
IInteractable       // Interface
```

### Functions

**Format**: `PascalCase`

**Examples**:
```cpp
GetHealth()
TakeDamage()
OnInventoryChanged()
CalculateDamageOutput()
IsPlayerAlive()
```

**Naming Guidelines**:
- Use descriptive, action-oriented names
- Getters start with `Get`: `GetCurrentHealth()`
- Setters start with `Set`: `SetMaxHealth()`
- Booleans phrased as questions: `IsAlive()`, `CanJump()`, `HasWeapon()`
- Event handlers start with `On`: `OnDeath()`, `OnLevelUp()`

### Variables

**Format**: `PascalCase` with prefix for specific types

**Prefixes**:
- `b` - Booleans only
- No prefix for most variables

**Examples**:
```cpp
// Booleans
bool bIsAlive;
bool bCanJump;
bool bHasWeapon;
bool bIsInCombat;

// Other types (no prefix)
int32 CurrentHealth;
float MaxSpeed;
FString PlayerName;
TArray<AActor*> NearbyEnemies;
UInventoryComponent* Inventory;
```

**Naming Guidelines**:
- Use descriptive names over abbreviations
- Avoid single-letter variables (except loop counters)
- Constants in all caps with underscores: `MAX_HEALTH`, `DEFAULT_SPEED`

### Files

**Format**: Match class name exactly

**Examples**:
```
PlayerCharacter.h
PlayerCharacter.cpp
HealthComponent.h
HealthComponent.cpp
ItemData.h
WeaponType.h
```

**Organization**:
- Header files (`.h`) and implementation files (`.cpp`) in appropriate Source/ folders
- One class per file pair (header + implementation)
- Group related classes in subfolders (e.g., `Source/Combat/`, `Source/Inventory/`)

### Namespaces

**Format**: `PascalCase`

**Examples**:
```cpp
namespace LamentGame
{
    namespace Combat
    {
        // Combat-related code
    }
}
```

---

## Documentation

### Files

**Format**: `PascalCase` with `.md` extension

**Examples**:
```
Overview.md
CoreMechanics.md
CombatSystem.md
PlayerProgression.md
NamingConventions.md
```

**Naming Guidelines**:
- Use descriptive, clear names
- Avoid abbreviations unless widely understood
- Multi-word names use PascalCase without spaces or hyphens

### Folders

**Format**: `PascalCase`

**Examples**:
```
GameDesign/
Mechanics/
Systems/
Narrative/
Technical/
Projects/
Reference/
```

### Obsidian Links

**Format**: Use wiki-style links

**Examples**:
```markdown
[[Overview]]
[[Mechanics/CombatSystem]]
[[Reference/NamingConventions|Naming Guide]]
```

---

## Python Scripts

Follow PEP 8 Python style guidelines.

### Files

**Format**: `snake_case` with `.py` extension

**Examples**:
```
color_palette_extractor.py
asset_importer.py
build_automation.py
texture_optimizer.py
```

### Functions

**Format**: `snake_case`

**Examples**:
```python
def extract_colors(image_path):
    pass

def calculate_palette(pixels):
    pass

def save_results(output_file, data):
    pass
```

### Variables

**Format**: `snake_case`

**Examples**:
```python
image_path = "path/to/image.png"
color_count = 5
output_directory = "./output"
is_valid = True
max_iterations = 100
```

### Constants

**Format**: `UPPER_SNAKE_CASE`

**Examples**:
```python
MAX_COLORS = 10
DEFAULT_OUTPUT_DIR = "./output"
SUPPORTED_FORMATS = [".png", ".jpg", ".bmp"]
```

### Classes

**Format**: `PascalCase`

**Examples**:
```python
class ColorExtractor:
    pass

class ImageProcessor:
    pass

class PaletteGenerator:
    pass
```

---

## Shell Scripts

### Files

**Format**: `snake_case` with appropriate extension

**Examples**:
```
build_project.sh
clean_intermediate.sh
package_game.bat
setup_environment.sh
```

---

## Assets

### Source Assets (Pre-Import)

**Format**: Descriptive names with underscores

**Textures**:
```
character_diffuse_1024.png
environment_normal_2048.png
ui_icon_health.png
```

**Models**:
```
character_player_lod0.fbx
prop_crate_wooden.fbx
weapon_sword_iron.fbx
```

**Audio**:
```
sfx_footstep_stone.wav
music_combat_theme_01.mp3
voice_player_hurt.wav
```

**Naming Pattern**: `[type]_[description]_[variant/detail].[extension]`

### Unreal Content (Post-Import)

Follow Unreal's recommended asset naming conventions.

**Prefixes**:
- `T_` - Textures
- `M_` - Materials
- `MI_` - Material Instances
- `SM_` - Static Meshes
- `SK_` - Skeletal Meshes
- `BP_` - Blueprints
- `ABP_` - Animation Blueprints
- `A_` - Animations
- `S_` - Sounds
- `SFX_` - Sound effects
- `MUS_` - Music

**Examples**:
```
T_Character_Diffuse
M_Character_Master
MI_Character_Player
SM_Prop_Crate
SK_Character_Player
BP_PlayerCharacter
ABP_Character_Player
A_Character_Idle
SFX_Footstep_Stone
MUS_Combat_Theme_01
```

---

## Folders & Directory Structure

### Project Root

**Format**: `PascalCase` for documentation/organization, `snake_case` for tool/script folders

**Examples**:
```
Documentation/
UnrealProjects/
Scripts/
Assets/
.opencode/
```

### Script Subfolders

**Format**: `snake_case`

**Examples**:
```
Scripts/tools/
Scripts/build/
Scripts/tools/color_palette_extractor/
Scripts/tools/asset_importer/
```

---

## Special Cases

### Acronyms

**In PascalCase contexts**: Treat as regular words
```cpp
class AHttpManager;      // NOT AHTTPManager
class UJsonParser;       // NOT UJSONParser
```

**Exceptions**: Well-known Unreal acronyms
```cpp
class UFPSController;    // FPS is commonly capitalized
class UUIWidget;         // UI is commonly capitalized
```

### Numbers in Names

**Allowed**: When part of a version or variant
```cpp
FVector3D  // Okay
T_Character_LOD0  // Okay
Level_01  // Okay
```

### Abbreviations

**Avoid** unless widely understood in game dev context:
- ❌ `char` → ✅ `Character`
- ❌ `pos` → ✅ `Position`
- ❌ `vel` → ✅ `Velocity`

**Acceptable abbreviations**:
- `Max`, `Min`, `Num`, `Id`, `Ui`, `Fps`, `Ai`, `Hp`, `Mp`

---

## Summary Quick Reference

| Context | Format | Example |
|---------|--------|---------|
| **C++ Classes** | PascalCase + Prefix | `APlayerCharacter`, `UHealthComponent` |
| **C++ Functions** | PascalCase | `GetHealth()`, `TakeDamage()` |
| **C++ Variables** | PascalCase (+ `b` for bool) | `CurrentHealth`, `bIsAlive` |
| **C++ Files** | Match class name | `PlayerCharacter.h` |
| **Documentation Files** | PascalCase | `Overview.md`, `CoreMechanics.md` |
| **Documentation Folders** | PascalCase | `GameDesign/`, `Mechanics/` |
| **Python Files** | snake_case | `color_extractor.py` |
| **Python Functions** | snake_case | `extract_colors()` |
| **Python Variables** | snake_case | `image_path`, `color_count` |
| **Python Classes** | PascalCase | `ColorExtractor` |
| **Shell Scripts** | snake_case | `build_project.sh` |
| **Source Assets** | snake_case | `character_diffuse.png` |
| **Unreal Assets** | Prefix + PascalCase | `T_Character_Diffuse` |

---

## Enforcement

- Code reviews should check naming conventions
- OpenCode agent is configured to follow these standards
- When in doubt, consistency with existing code takes precedence
- Update this document if new patterns emerge

---

## Related Documentation

- [[Overview]] - Project overview
- [[index]] - Documentation hub
