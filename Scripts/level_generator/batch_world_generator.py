"""
Batch World Generation Script

Generates multiple complete worlds in one run, either from presets or custom configurations.
Useful for generating a variety of content or testing different parameters.
"""

import os
import time
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from world_generator import WorldConfig, generate_world
from export.json_exporter import export_world
from preview.visualizer import render_world_spatial
from presets.preset_manager import PresetManager


class BatchWorldGenerator:
    """Manages batch generation of multiple worlds."""
    
    def __init__(self, output_base_dir: str = "output"):
        """Initialize batch generator."""
        self.output_base_dir = Path(output_base_dir)
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        self.preset_manager = PresetManager()
        self.results: List[Dict] = []
    
    def generate_from_preset(self, preset_name: str, verbose: bool = True) -> Dict:
        """
        Generate a world from a preset configuration.
        
        Args:
            preset_name: Name of preset file (with or without .json)
            verbose: Print generation progress
        
        Returns:
            Dictionary with generation results and statistics
        """
        if verbose:
            print(f"\n{'='*80}")
            print(f"Generating world from preset: {preset_name}")
            print(f"{'='*80}")
        
        # Load preset
        preset = self.preset_manager.load_preset(preset_name)
        config = preset.to_world_config()
        
        if verbose:
            print(f"Description: {preset.description}")
            ratio_pct = int(preset.horizontal_vertical_ratio * 100)
            print(f"Configuration: {preset.level_count} levels, {preset.difficulty_curve} curve, {100-ratio_pct}%H/{ratio_pct}%V")
            print()
        
        # Generate world
        start_time = time.time()
        levels = generate_world(config, verbose=verbose)
        generation_time = time.time() - start_time
        
        # Create output directory
        output_dir = self.output_base_dir / preset.name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Export JSON files
        if verbose:
            print(f"\nExporting to {output_dir}...")
        export_world(levels, str(output_dir), preset.name)
        
        # Generate world map visualization
        map_path = output_dir / f"{preset.name}_world_map.png"
        if verbose:
            print(f"Rendering world map to {map_path}...")
        render_world_spatial(levels, str(map_path))
        
        # Calculate statistics
        total_enemies = sum(len(level['entities'].get('enemies', [])) for level in levels)
        total_obstacles = sum(len(level['entities'].get('obstacles', [])) for level in levels)
        total_save_points = sum(1 if level['entities'].get('save_point') else 0 for level in levels)
        avg_quality = sum(level['stats']['quality_score'] for level in levels) / len(levels)
        
        result = {
            'preset_name': preset.name,
            'level_count': len(levels),
            'total_enemies': total_enemies,
            'total_obstacles': total_obstacles,
            'total_save_points': total_save_points,
            'avg_quality': round(avg_quality, 2),
            'generation_time': round(generation_time, 2),
            'output_dir': str(output_dir),
            'files_generated': len(list(output_dir.glob('*.json'))) + 1  # +1 for PNG
        }
        
        self.results.append(result)
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"World '{preset.name}' generated successfully!")
            print(f"  - {result['level_count']} levels")
            print(f"  - {result['total_enemies']} enemies")
            print(f"  - {result['total_obstacles']} obstacles")
            print(f"  - {result['total_save_points']} save points")
            print(f"  - Average quality: {result['avg_quality']}")
            print(f"  - Generation time: {result['generation_time']}s")
            print(f"  - Files: {result['files_generated']} (JSON + PNG)")
            print(f"{'='*80}")
        
        return result
    
    def generate_all_presets(self, verbose: bool = True, tags: Optional[List[str]] = None):
        """
        Generate worlds for all available presets.
        
        Args:
            verbose: Print generation progress
            tags: Optional list of tags to filter presets (e.g., ['beginner', 'test'])
        """
        presets = self.preset_manager.list_presets()
        
        # Filter by tags if specified
        if tags:
            presets = [p for p in presets if any(tag in p['tags'] for tag in tags)]
        
        if verbose:
            print(f"\n{'#'*80}")
            print(f"BATCH GENERATION - {len(presets)} presets")
            if tags:
                print(f"Filtered by tags: {', '.join(tags)}")
            print(f"{'#'*80}")
        
        total_start = time.time()
        
        for preset_info in presets:
            try:
                self.generate_from_preset(preset_info['filename'], verbose=verbose)
            except Exception as e:
                print(f"\nERROR generating {preset_info['name']}: {e}")
                import traceback
                traceback.print_exc()
        
        total_time = time.time() - total_start
        
        if verbose:
            self.print_summary(total_time)
    
    def generate_custom_batch(self, configs: List[WorldConfig], verbose: bool = True):
        """
        Generate worlds from a list of custom WorldConfig objects.
        
        Args:
            configs: List of WorldConfig objects to generate
            verbose: Print generation progress
        """
        if verbose:
            print(f"\n{'#'*80}")
            print(f"CUSTOM BATCH GENERATION - {len(configs)} worlds")
            print(f"{'#'*80}")
        
        total_start = time.time()
        
        for i, config in enumerate(configs, 1):
            try:
                if verbose:
                    print(f"\n{'='*80}")
                    print(f"[{i}/{len(configs)}] Generating: {config.world_name}")
                    print(f"{'='*80}")
                
                start_time = time.time()
                levels = generate_world(config, verbose=verbose)
                generation_time = time.time() - start_time
                
                # Create output directory
                output_dir = self.output_base_dir / config.world_name
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Export
                export_world(levels, str(output_dir), config.world_name)
                map_path = output_dir / f"{config.world_name}_world_map.png"
                render_world_spatial(levels, str(map_path))
                
                # Statistics
                total_enemies = sum(len(level['entities'].get('enemies', [])) for level in levels)
                total_obstacles = sum(len(level['entities'].get('obstacles', [])) for level in levels)
                avg_quality = sum(level['stats']['quality_score'] for level in levels) / len(levels)
                
                result = {
                    'preset_name': config.world_name,
                    'level_count': len(levels),
                    'total_enemies': total_enemies,
                    'total_obstacles': total_obstacles,
                    'avg_quality': round(avg_quality, 2),
                    'generation_time': round(generation_time, 2),
                    'output_dir': str(output_dir)
                }
                
                self.results.append(result)
                
                if verbose:
                    print(f"\nGenerated in {generation_time:.2f}s - Quality: {avg_quality:.2f}")
            
            except Exception as e:
                print(f"\nERROR generating {config.world_name}: {e}")
                import traceback
                traceback.print_exc()
        
        total_time = time.time() - total_start
        
        if verbose:
            self.print_summary(total_time)
    
    def print_summary(self, total_time: float):
        """Print summary statistics for batch generation."""
        print(f"\n{'#'*80}")
        print(f"BATCH GENERATION COMPLETE")
        print(f"{'#'*80}")
        print(f"\nGenerated {len(self.results)} worlds in {total_time:.2f}s")
        print(f"\nSummary by world:")
        print(f"{'-'*80}")
        print(f"{'World':<20} {'Levels':<8} {'Enemies':<10} {'Obstacles':<12} {'Quality':<10} {'Time(s)':<10}")
        print(f"{'-'*80}")
        
        total_levels = 0
        total_enemies = 0
        total_obstacles = 0
        
        for result in self.results:
            print(f"{result['preset_name']:<20} "
                  f"{result['level_count']:<8} "
                  f"{result['total_enemies']:<10} "
                  f"{result['total_obstacles']:<12} "
                  f"{result['avg_quality']:<10.2f} "
                  f"{result['generation_time']:<10.2f}")
            
            total_levels += result['level_count']
            total_enemies += result['total_enemies']
            total_obstacles += result['total_obstacles']
        
        print(f"{'-'*80}")
        print(f"{'TOTAL':<20} "
              f"{total_levels:<8} "
              f"{total_enemies:<10} "
              f"{total_obstacles:<12}")
        print(f"{'-'*80}")
        
        # Export summary
        summary_path = self.output_base_dir / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        summary_data = {
            'timestamp': datetime.now().isoformat(),
            'total_time': round(total_time, 2),
            'world_count': len(self.results),
            'total_levels': total_levels,
            'total_enemies': total_enemies,
            'total_obstacles': total_obstacles,
            'worlds': self.results
        }
        
        with open(summary_path, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"\nSummary exported to: {summary_path}")
        print(f"Output directory: {self.output_base_dir}")
    
    def clear_results(self):
        """Clear accumulated results."""
        self.results = []


def main():
    """Example usage of batch generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch world generation')
    parser.add_argument('--all', action='store_true', help='Generate all presets')
    parser.add_argument('--preset', type=str, help='Generate specific preset by name')
    parser.add_argument('--tags', type=str, nargs='+', help='Filter presets by tags')
    parser.add_argument('--quiet', action='store_true', help='Suppress verbose output')
    parser.add_argument('--output', type=str, default='output', help='Output directory')
    
    args = parser.parse_args()
    
    generator = BatchWorldGenerator(output_base_dir=args.output)
    verbose = not args.quiet
    
    if args.all:
        # Generate all presets
        generator.generate_all_presets(verbose=verbose, tags=args.tags)
    
    elif args.preset:
        # Generate specific preset
        generator.generate_from_preset(args.preset, verbose=verbose)
    
    else:
        # Default: generate a selection of presets for demonstration
        print("Generating selection of preset worlds...")
        print("(Use --all to generate all presets, or --preset <name> for specific preset)")
        print()
        
        selected = ['ShortTest', 'CaveWorld', 'TowerClimb']
        for preset_name in selected:
            generator.generate_from_preset(preset_name, verbose=verbose)


if __name__ == '__main__':
    main()
