#!/usr/bin/env python3
"""
Level Generator - Command Line Interface

Generate single room templates from the command line.
"""
import argparse
import os
import sys
from datetime import datetime

from generators.room_generator import generate_room, get_available_shapes, get_size_options
from preview.visualizer import render_room_simple
from validation.validator_simple import validate_room_simple


def main():
    parser = argparse.ArgumentParser(
        description="Generate procedural room templates for Lament platformer game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --shape horizontal_right --difficulty 5 --length medium
  python main.py --shape vertical_up --difficulty 8 --length long
  python main.py --shape box --difficulty 5 --size medium --features spikes,platforms
        """
    )
    
    parser.add_argument(
        '--shape',
        type=str,
        required=True,
        choices=get_available_shapes(),
        help='Room shape type'
    )
    
    parser.add_argument(
        '--difficulty',
        type=int,
        required=True,
        choices=range(1, 11),
        metavar='1-10',
        help='Difficulty level (1=easy, 10=hard)'
    )
    
    parser.add_argument(
        '--length',
        type=str,
        help='Room length for horizontal/vertical shapes (short, medium, long)'
    )
    
    parser.add_argument(
        '--size',
        type=str,
        help='Room size for box arenas (small, medium, large)'
    )
    
    parser.add_argument(
        '--features',
        type=str,
        default='spikes,slopes,platforms',
        help='Comma-separated list of features (default: spikes,slopes,platforms)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output filename (optional, auto-generates if not provided)'
    )
    
    parser.add_argument(
        '--no-grid',
        action='store_true',
        help='Disable grid lines in output image'
    )
    
    parser.add_argument(
        '--no-metadata',
        action='store_true',
        help='Disable metadata banner in output image'
    )
    
    args = parser.parse_args()
    
    # Determine size parameter
    if args.shape == "box":
        if not args.size:
            print("Error: --size required for box shape (small, medium, large)")
            sys.exit(1)
        size = args.size
        if size not in ['small', 'medium', 'large']:
            print(f"Error: Invalid size '{size}' for box. Use: small, medium, large")
            sys.exit(1)
    else:
        if not args.length:
            print("Error: --length required for this shape (short, medium, long)")
            sys.exit(1)
        size = args.length
        if size not in ['short', 'medium', 'long']:
            print(f"Error: Invalid length '{size}'. Use: short, medium, long")
            sys.exit(1)
    
    # Parse features
    features = [f.strip() for f in args.features.split(',')]
    
    # Generate room
    print(f"Generating {args.shape} room...")
    print(f"  Difficulty: {args.difficulty}")
    print(f"  Size: {size}")
    print(f"  Features: {', '.join(features)}")
    
    try:
        room = generate_room(args.shape, args.difficulty, size, features)
        print(f"✓ Generated room: {room.id}")
        
        # Validate room and display tier
        validation_result = validate_room_simple(room)
        tier = validation_result['tier']
        playable = validation_result['valid']
        
        tier_colors = {
            'EASY': '🟢',
            'NORMAL': '🔵',
            'HARD': '🟠',
            'EXPERT': '🔴',
            'IMPOSSIBLE': '⚫'
        }
        
        print(f"  Validation: {tier_colors.get(tier, '❓')} {tier} ({'Playable' if playable else 'Not Playable'})")
        if validation_result['errors']:
            print(f"  Issues: {', '.join(validation_result['errors'][:3])}")
        
    except Exception as e:
        print(f"✗ Error generating room: {e}")
        sys.exit(1)
    
    # Determine output filename
    if args.output:
        output_path = args.output
    else:
        # Auto-generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{args.shape}_d{args.difficulty}_{size}_{timestamp}.png"
        output_path = os.path.join("output", filename)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "output", exist_ok=True)
    
    # Render room
    print(f"Rendering preview...")
    try:
        from preview.visualizer import render_room
        render_room(
            room, 
            output_path,
            show_grid=not args.no_grid,
            show_metadata=not args.no_metadata
        )
        print(f"✓ Success! Room saved to: {output_path}")
    except Exception as e:
        print(f"✗ Error rendering room: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
