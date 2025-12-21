"""
Preset Manager for World Generation Configurations

Allows saving and loading world configuration presets from JSON files.
Presets define world parameters like level count, difficulty curves, themes, etc.
"""

import json
import os
from typing import Dict, List, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from world_generator import WorldConfig


class WorldPreset:
    """Represents a world generation preset configuration."""
    
    def __init__(self, data: Dict):
        """Initialize preset from dictionary data."""
        self.name = data.get('name', 'Unnamed')
        self.description = data.get('description', '')
        self.level_count = data.get('level_count', 5)
        self.difficulty_curve = data.get('difficulty_curve', 'linear')
        
        # Support both new and old systems
        if 'horizontal_vertical_ratio' in data:
            self.horizontal_vertical_ratio = data['horizontal_vertical_ratio']
        elif 'predominance' in data:
            # Convert old predominance to ratio
            ratio_map = {'horizontal': 0.2, 'vertical': 0.8, 'mixed': 0.5}
            self.horizontal_vertical_ratio = ratio_map.get(data['predominance'], 0.5)
        else:
            self.horizontal_vertical_ratio = 0.5
        
        self.slope_count = data.get('slope_count', 2)
        self.max_elevation_change = data.get('max_elevation_change', 8)
        self.enemy_theme = data.get('enemy_theme', 'balanced')
        self.obstacle_themes = data.get('obstacle_themes', ['mixed'])
        self.save_point_frequency = data.get('save_point_frequency', 3)
        self.quality_attempts = data.get('quality_attempts', 5)
        self.tags = data.get('tags', [])
        
    def to_dict(self) -> Dict:
        """Convert preset to dictionary format."""
        return {
            'name': self.name,
            'description': self.description,
            'level_count': self.level_count,
            'difficulty_curve': self.difficulty_curve,
            'horizontal_vertical_ratio': self.horizontal_vertical_ratio,
            'slope_count': self.slope_count,
            'max_elevation_change': self.max_elevation_change,
            'enemy_theme': self.enemy_theme,
            'obstacle_themes': self.obstacle_themes,
            'save_point_frequency': self.save_point_frequency,
            'quality_attempts': self.quality_attempts,
            'tags': self.tags
        }
    
    def to_world_config(self):
        """Convert preset to WorldConfig object."""
        from world_generator import WorldConfig
        return WorldConfig(
            world_name=self.name,
            level_count=self.level_count,
            difficulty_curve=self.difficulty_curve,
            horizontal_vertical_ratio=self.horizontal_vertical_ratio,
            slope_count=self.slope_count,
            max_elevation_change=self.max_elevation_change
        )
    
    def __repr__(self):
        return f"WorldPreset('{self.name}', {self.level_count} levels, {self.difficulty_curve})"


class PresetManager:
    """Manages loading, saving, and listing world presets."""
    
    def __init__(self, presets_dir: Optional[str] = None):
        """Initialize preset manager with directory path."""
        if presets_dir is None:
            # Default to presets/ directory relative to this file
            presets_dir = os.path.join(os.path.dirname(__file__), '')
        self.presets_dir = Path(presets_dir)
        self.presets_dir.mkdir(parents=True, exist_ok=True)
    
    def save_preset(self, preset: WorldPreset, filename: Optional[str] = None) -> str:
        """
        Save a preset to JSON file.
        
        Args:
            preset: WorldPreset object to save
            filename: Optional custom filename (without extension)
        
        Returns:
            Path to saved file
        """
        if filename is None:
            # Use preset name as filename
            filename = preset.name.replace(' ', '_').lower()
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.presets_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(preset.to_dict(), f, indent=2)
        
        return str(filepath)
    
    def load_preset(self, filename: str) -> WorldPreset:
        """
        Load a preset from JSON file.
        
        Args:
            filename: Name of preset file (with or without .json extension)
        
        Returns:
            WorldPreset object
        
        Raises:
            FileNotFoundError: If preset file doesn't exist
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.presets_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Preset not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return WorldPreset(data)
    
    def list_presets(self) -> List[Dict]:
        """
        List all available presets with basic info.
        
        Returns:
            List of dictionaries with preset info (name, description, tags)
        """
        presets = []
        
        for filepath in self.presets_dir.glob('*.json'):
            try:
                preset = self.load_preset(filepath.name)
                presets.append({
                    'filename': filepath.name,
                    'name': preset.name,
                    'description': preset.description,
                    'tags': preset.tags,
                    'levels': preset.level_count,
                    'curve': preset.difficulty_curve
                })
            except Exception as e:
                print(f"Warning: Failed to load {filepath.name}: {e}")
        
        return presets
    
    def get_preset_by_tag(self, tag: str) -> List[WorldPreset]:
        """
        Find all presets with a specific tag.
        
        Args:
            tag: Tag to search for
        
        Returns:
            List of matching WorldPreset objects
        """
        matching = []
        
        for filepath in self.presets_dir.glob('*.json'):
            try:
                preset = self.load_preset(filepath.name)
                if tag in preset.tags:
                    matching.append(preset)
            except Exception:
                pass
        
        return matching
    
    def create_default_presets(self):
        """Create a set of default example presets."""
        defaults = [
            {
                'name': 'CaveWorld',
                'description': 'Horizontal cave exploration with gradual difficulty increase',
                'level_count': 8,
                'difficulty_curve': 'linear',
                'predominance': 'horizontal',
                'enemy_theme': 'balanced',
                'obstacle_themes': ['hazards', 'platforming'],
                'save_point_frequency': 3,
                'quality_attempts': 5,
                'tags': ['beginner', 'horizontal', 'exploration']
            },
            {
                'name': 'TowerClimb',
                'description': 'Vertical tower ascent with increasing challenge',
                'level_count': 10,
                'difficulty_curve': 'linear',
                'predominance': 'vertical',
                'enemy_theme': 'balanced',
                'obstacle_themes': ['platforming', 'mixed'],
                'save_point_frequency': 2,
                'quality_attempts': 5,
                'tags': ['vertical', 'platforming', 'endurance']
            },
            {
                'name': 'GauntletRun',
                'description': 'Intense combat-focused challenge with difficulty spikes',
                'level_count': 7,
                'difficulty_curve': 'spike',
                'predominance': 'mixed',
                'enemy_theme': 'aggressive',
                'obstacle_themes': ['combat', 'hazards'],
                'save_point_frequency': 2,
                'quality_attempts': 5,
                'tags': ['combat', 'challenge', 'advanced']
            },
            {
                'name': 'PlateauAdventure',
                'description': 'Mixed exploration with difficulty plateaus for learning',
                'level_count': 12,
                'difficulty_curve': 'plateau',
                'predominance': 'mixed',
                'enemy_theme': 'balanced',
                'obstacle_themes': ['mixed', 'platforming'],
                'save_point_frequency': 3,
                'quality_attempts': 5,
                'tags': ['beginner', 'mixed', 'learning']
            },
            {
                'name': 'MinimalChallenge',
                'description': 'Pure platforming with minimal enemies, focus on precision',
                'level_count': 6,
                'difficulty_curve': 'linear',
                'predominance': 'mixed',
                'enemy_theme': 'sparse',
                'obstacle_themes': ['platforming', 'minimal'],
                'save_point_frequency': 4,
                'quality_attempts': 5,
                'tags': ['platforming', 'precision', 'intermediate']
            },
            {
                'name': 'ShortTest',
                'description': 'Quick 3-level test world for rapid iteration',
                'level_count': 3,
                'difficulty_curve': 'linear',
                'predominance': 'horizontal',
                'enemy_theme': 'balanced',
                'obstacle_themes': ['mixed'],
                'save_point_frequency': 2,
                'quality_attempts': 3,
                'tags': ['test', 'quick', 'development']
            }
        ]
        
        for preset_data in defaults:
            preset = WorldPreset(preset_data)
            self.save_preset(preset)
            print(f"Created preset: {preset.name}")


def main():
    """Example usage of preset manager."""
    manager = PresetManager()
    
    # Create default presets
    print("Creating default presets...")
    manager.create_default_presets()
    print()
    
    # List all presets
    print("Available presets:")
    print("-" * 80)
    for info in manager.list_presets():
        print(f"{info['name']:20} - {info['description']}")
        print(f"{'':20}   {info['levels']} levels, {info['curve']} curve")
        print(f"{'':20}   Tags: {', '.join(info['tags'])}")
        print()
    
    # Load and display a specific preset
    print("-" * 80)
    print("Loading 'TowerClimb' preset...")
    preset = manager.load_preset('TowerClimb')
    print(f"Name: {preset.name}")
    print(f"Description: {preset.description}")
    print(f"Levels: {preset.level_count}")
    print(f"Difficulty: {preset.difficulty_curve}")
    ratio_pct = int(preset.horizontal_vertical_ratio * 100)
    print(f"Horizontal/Vertical: {100-ratio_pct}%/{ratio_pct}%")
    print(f"Tags: {', '.join(preset.tags)}")


if __name__ == '__main__':
    main()
