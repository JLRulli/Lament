"""
Test script for Week 5 world generation with entities

Generates a complete world and exports to JSON.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from world_generator import WorldConfig, generate_world
from export.json_exporter import export_world
from preview.visualizer import render_world_spatial


def main():
    print("=" * 70)
    print("WEEK 5 TEST: World Generation with Entities")
    print("=" * 70)
    print()
    
    # Test 1: Small world with linear difficulty
    print("TEST 1: Linear difficulty progression (5 levels)")
    print("-" * 70)
    
    config1 = WorldConfig(
        world_name='LinearTest',
        level_count=5,
        difficulty_curve='linear',
        predominance='mixed'
    )
    
    levels1 = generate_world(config1, verbose=True)
    
    # Export
    print("Exporting to output/LinearTest/...")
    files1 = export_world(levels1, 'output/LinearTest', 'LinearTest')
    print(f"✓ Exported {len(files1)} files")
    
    # Generate world map visualization
    print("Generating world map visualization...")
    render_world_spatial(levels1, 'output/LinearTest/LinearTest_world_map.png')
    print()
    
    # Test 2: Spike curve with horizontal predominance
    print("TEST 2: Spike difficulty curve (7 levels)")
    print("-" * 70)
    
    config2 = WorldConfig(
        world_name='SpikeTest',
        level_count=7,
        difficulty_curve='spike',
        predominance='horizontal'
    )
    
    levels2 = generate_world(config2, verbose=True)
    
    # Export
    print("Exporting to output/SpikeTest/...")
    files2 = export_world(levels2, 'output/SpikeTest', 'SpikeTest')
    print(f"✓ Exported {len(files2)} files")
    
    # Generate world map visualization
    print("Generating world map visualization...")
    render_world_spatial(levels2, 'output/SpikeTest/SpikeTest_world_map.png')
    print()
    
    # Test 3: Plateau curve with vertical predominance
    print("TEST 3: Plateau difficulty curve (6 levels)")
    print("-" * 70)
    
    config3 = WorldConfig(
        world_name='PlateauTest',
        level_count=6,
        difficulty_curve='plateau',
        predominance='vertical'
    )
    
    levels3 = generate_world(config3, verbose=True)
    
    # Export
    print("Exporting to output/PlateauTest/...")
    files3 = export_world(levels3, 'output/PlateauTest', 'PlateauTest')
    print(f"✓ Exported {len(files3)} files")
    
    # Generate world map visualization
    print("Generating world map visualization...")
    render_world_spatial(levels3, 'output/PlateauTest/PlateauTest_world_map.png')
    print()
    
    # Final Summary
    print("=" * 70)
    print("WEEK 5 TEST COMPLETE")
    print("=" * 70)
    print(f"Total worlds generated: 3")
    print(f"Total levels generated: {len(levels1) + len(levels2) + len(levels3)}")
    print(f"Total files exported: {len(files1) + len(files2) + len(files3)}")
    print()
    print("Exported worlds:")
    print("  - output/LinearTest/")
    print("  - output/SpikeTest/")
    print("  - output/PlateauTest/")
    print()
    print("World map visualizations:")
    print("  - output/LinearTest/LinearTest_world_map.png")
    print("  - output/SpikeTest/SpikeTest_world_map.png")
    print("  - output/PlateauTest/PlateauTest_world_map.png")
    print()
    print("✓ All tests passed!")
    print()


if __name__ == "__main__":
    main()
