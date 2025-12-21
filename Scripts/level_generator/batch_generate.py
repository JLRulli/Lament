#!/usr/bin/env python3
"""
Batch Generation Script

Generates base templates and creates variations, with validation filtering.
"""
import os
import random
from datetime import datetime
from collections import defaultdict

from generators.room_generator import generate_room
from preview.visualizer import render_room_simple
from validation import validate_room_simple  # type: ignore
from variation.variator import generate_variations  # type: ignore


def batch_generate(num_variations=5, filter_impossible=True):
    """
    Generate batch of templates with validation and variations
    
    Args:
        num_variations: Number of variations to create per base template
        filter_impossible: Whether to filter out IMPOSSIBLE tier rooms
    """
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_dir = os.path.join("output", f"batch_{timestamp}")
    os.makedirs(batch_dir, exist_ok=True)
    
    print("=" * 60)
    print("BATCH ROOM GENERATION WITH VALIDATION & VARIATIONS")
    print("=" * 60)
    print(f"Output directory: {batch_dir}")
    print(f"Variations per base: {num_variations}")
    print(f"Filter impossible: {filter_impossible}\n")
    
    # Define generation parameters
    shapes_config = [
        {
            "shape": "horizontal_right",
            "sizes": ["short", "medium", "long"],
            "difficulties": [2, 5, 8]
        },
        {
            "shape": "vertical_up",
            "sizes": ["short", "medium", "long"],
            "difficulties": [2, 5, 8]
        },
        {
            "shape": "box",
            "sizes": ["small", "medium", "large"],
            "difficulties": [2, 5, 8]
        }
    ]
    
    features = ["platforms", "spikes", "slopes"]
    
    # Statistics tracking
    stats = {
        'base_generated': 0,
        'base_playable': 0,
        'base_failed': 0,
        'variations_generated': 0,
        'variations_playable': 0,
        'total_saved': 0,
        'tier_distribution': defaultdict(int),
        'by_shape': defaultdict(lambda: {'total': 0, 'playable': 0})
    }
    
    # Generate templates
    for shape_config in shapes_config:
        shape = shape_config["shape"]
        print(f"\n{'='*60}")
        print(f"Generating {shape} templates...")
        print(f"{'='*60}\n")
        
        for size in shape_config["sizes"]:
            for difficulty in shape_config["difficulties"]:
                stats['base_generated'] += 1
                
                try:
                    # Generate base room
                    room = generate_room(shape, difficulty, size, features)
                    
                    # Validate base room
                    validation = validate_room_simple(room)
                    tier = validation['tier']
                    stats['tier_distribution'][tier] += 1
                    stats['by_shape'][shape]['total'] += 1
                    
                    if validation['valid']:
                        stats['base_playable'] += 1
                        stats['by_shape'][shape]['playable'] += 1
                    
                    # Skip impossible rooms if filtering enabled
                    if filter_impossible and tier == 'IMPOSSIBLE':
                        print(f"  [SKIP] {shape} d{difficulty} {size} - IMPOSSIBLE tier")
                        continue
                    
                    # Save base room
                    filename = f"{shape}_d{difficulty}_{size}_base.png"
                    output_path = os.path.join(batch_dir, filename)
                    render_room_simple(room, output_path)
                    stats['total_saved'] += 1
                    
                    tier_emoji = {'EASY': '🟢', 'NORMAL': '🔵', 'HARD': '🟠', 'EXPERT': '🔴', 'IMPOSSIBLE': '⚫'}
                    print(f"  ✓ BASE: {filename} - {tier_emoji.get(tier, '❓')} {tier}")
                    
                    # Generate variations
                    if validation['valid']:  # Only create variations for playable rooms
                        try:
                            variations = generate_variations(room, count=num_variations)
                            
                            # Validate and save each variation
                            for i, variant in enumerate(variations[1:], 1):  # Skip base (index 0)
                                var_validation = validate_room_simple(variant)
                                var_tier = var_validation['tier']
                                stats['variations_generated'] += 1
                                stats['tier_distribution'][var_tier] += 1
                                
                                if var_validation['valid']:
                                    stats['variations_playable'] += 1
                                
                                # Skip impossible variations if filtering enabled
                                if filter_impossible and var_tier == 'IMPOSSIBLE':
                                    continue
                                
                                # Save variation
                                var_filename = f"{shape}_d{difficulty}_{size}_var{i:02d}.png"
                                var_output = os.path.join(batch_dir, var_filename)
                                render_room_simple(variant, var_output)
                                stats['total_saved'] += 1
                                
                                print(f"    → VAR{i}: {var_tier}")
                        
                        except Exception as e:
                            print(f"    ✗ Variation generation failed: {e}")
                
                except Exception as e:
                    stats['base_failed'] += 1
                    print(f"  ✗ FAILED: {shape} d{difficulty} {size} - {e}")
    
    # Print summary statistics
    print_summary(stats, batch_dir)


def print_summary(stats, batch_dir):
    """Print batch generation summary statistics"""
    print("\n" + "=" * 60)
    print("BATCH GENERATION COMPLETE")
    print("=" * 60)
    
    print("\nBASE TEMPLATES:")
    print(f"  Generated:        {stats['base_generated']}")
    print(f"  Playable:         {stats['base_playable']} ({100 * stats['base_playable'] / max(1, stats['base_generated']):.1f}%)")
    print(f"  Failed:           {stats['base_failed']}")
    
    print("\nVARIATIONS:")
    print(f"  Generated:        {stats['variations_generated']}")
    print(f"  Playable:         {stats['variations_playable']} ({100 * stats['variations_playable'] / max(1, stats['variations_generated']):.1f}%)")
    
    print("\nTOTAL:")
    print(f"  Files saved:      {stats['total_saved']}")
    print(f"  Total playable:   {stats['base_playable'] + stats['variations_playable']}")
    
    print("\nTIER DISTRIBUTION:")
    for tier in ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'IMPOSSIBLE']:
        count = stats['tier_distribution'][tier]
        if count > 0:
            emoji = {'EASY': '🟢', 'NORMAL': '🔵', 'HARD': '🟠', 'EXPERT': '🔴', 'IMPOSSIBLE': '⚫'}
            print(f"  {emoji.get(tier, '❓')} {tier:12s}: {count:3d}")
    
    print("\nBY SHAPE:")
    for shape, data in stats['by_shape'].items():
        playable_pct = 100 * data['playable'] / max(1, data['total'])
        print(f"  {shape:20s}: {data['playable']}/{data['total']} playable ({playable_pct:.1f}%)")
    
    print(f"\nOutput location: {batch_dir}")
    print("=" * 60)


if __name__ == "__main__":
    batch_generate()
