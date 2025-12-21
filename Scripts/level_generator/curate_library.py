"""
Template library curation script

Generates a large batch of rooms, validates them, scores their quality,
and keeps only the best templates for a curated library.

Usage:
    python curate_library.py [--count 500] [--keep 200] [--min-quality 5.5]
"""
import sys
import os
import random
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generators.room_generator import generate_room
from validation.validator_simple import validate_room_simple
from validation.quality import score_room_quality
from validation.spawn_zones import assign_spawn_zones_to_room
from curation.template_library import TemplateLibrary


# Configuration for room generation
SHAPES = ['horizontal_right', 'vertical_up', 'box']

SIZE_OPTIONS = {
    'horizontal_right': ['short', 'medium', 'long'],
    'vertical_up': ['short', 'medium', 'long'],
    'box': ['small', 'medium', 'large']
}

FEATURE_OPTIONS = ['platforms', 'spikes', 'slopes']


def curate_library(
    total_count: int = 500,
    keep_count: int = 200,
    min_quality: float = 5.5,
    use_pathfinding: bool = False
):
    """
    Generate and curate a library of high-quality templates
    
    Args:
        total_count: Total number of rooms to generate
        keep_count: Number of best rooms to keep
        min_quality: Minimum quality score to consider
        use_pathfinding: Whether to use A* pathfinding validation
    
    Returns:
        TemplateLibrary: The curated library
    """
    print("=" * 60)
    print("TEMPLATE LIBRARY CURATION")
    print("=" * 60)
    print(f"Target: Generate {total_count}, keep best {keep_count}")
    print(f"Minimum quality threshold: {min_quality}")
    print(f"Pathfinding validation: {'ENABLED' if use_pathfinding else 'DISABLED'}")
    print()
    
    library = TemplateLibrary()
    
    valid_count = 0
    quality_passed_count = 0
    failed_validation = 0
    failed_quality = 0
    
    print(f"Generating {total_count} rooms...")
    for i in range(total_count):
        # Randomly select parameters
        shape = random.choice(SHAPES)
        difficulty = random.randint(1, 10)
        size = random.choice(SIZE_OPTIONS[shape])
        
        # Randomly select 1-3 features
        num_features = random.randint(1, 3)
        features = random.sample(FEATURE_OPTIONS, num_features)
        
        # Generate room
        room = generate_room(shape, difficulty, size, features)
        
        # Validate
        validation = validate_room_simple(room, use_pathfinding=use_pathfinding)
        
        if not validation['valid']:
            failed_validation += 1
            continue
        
        valid_count += 1
        
        # Assign spawn zones
        assign_spawn_zones_to_room(room)
        
        # Score quality
        quality = score_room_quality(room, validation)
        
        # Check quality threshold
        if quality['overall'] < min_quality:
            failed_quality += 1
            continue
        
        quality_passed_count += 1
        
        # Add to library
        library.add_template(room, validation, quality)
        
        # Progress update every 50 rooms
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i + 1}/{total_count} generated, "
                  f"{valid_count} valid, {quality_passed_count} high-quality")
    
    print()
    print(f"Generation complete!")
    print(f"  Total generated: {total_count}")
    print(f"  Passed validation: {valid_count} ({valid_count/total_count*100:.1f}%)")
    print(f"  Failed validation: {failed_validation}")
    print(f"  Passed quality threshold: {quality_passed_count} ({quality_passed_count/total_count*100:.1f}%)")
    print(f"  Failed quality threshold: {failed_quality}")
    print()
    
    # Keep only top N
    if len(library.templates) > keep_count:
        print(f"Keeping top {keep_count} templates by quality...")
        library.keep_top_n(keep_count)
    else:
        print(f"Generated {len(library.templates)} templates (less than target {keep_count})")
    
    print()
    
    return library


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Curate a library of high-quality room templates')
    parser.add_argument('--count', type=int, default=500,
                        help='Total number of rooms to generate (default: 500)')
    parser.add_argument('--keep', type=int, default=200,
                        help='Number of best rooms to keep (default: 200)')
    parser.add_argument('--min-quality', type=float, default=5.5,
                        help='Minimum quality score threshold (default: 5.5)')
    parser.add_argument('--pathfinding', action='store_true',
                        help='Enable A* pathfinding validation (slower but more accurate)')
    parser.add_argument('--output', type=str, default='output/template_catalog.json',
                        help='Output catalog file (default: output/template_catalog.json)')
    
    args = parser.parse_args()
    
    # Generate library
    start_time = datetime.now()
    
    library = curate_library(
        total_count=args.count,
        keep_count=args.keep,
        min_quality=args.min_quality,
        use_pathfinding=args.pathfinding
    )
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    # Show statistics
    print("=" * 60)
    print("LIBRARY STATISTICS")
    print("=" * 60)
    
    stats = library.get_statistics()
    
    print(f"Total templates: {stats['total']}")
    print(f"Average quality: {stats['avg_quality']}")
    print()
    
    print("By Difficulty Tier:")
    for tier, count in sorted(stats['by_tier'].items()):
        print(f"  {tier:12s}: {count:3d} ({count/stats['total']*100:.1f}%)")
    print()
    
    print("By Shape:")
    for shape, count in sorted(stats['by_shape'].items()):
        print(f"  {shape:20s}: {count:3d} ({count/stats['total']*100:.1f}%)")
    print()
    
    print("Quality Distribution:")
    for label, count in stats['quality_distribution'].items():
        print(f"  {label:22s}: {count:3d} ({count/stats['total']*100:.1f}%)")
    print()
    
    # Export catalog
    print(f"Exporting catalog to {args.output}...")
    library.export_catalog(args.output)
    
    print()
    print("=" * 60)
    print(f"Curation complete in {elapsed:.1f}s")
    print(f"Catalog saved to: {args.output}")
    print("=" * 60)


if __name__ == "__main__":
    main()
