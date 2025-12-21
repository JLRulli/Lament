"""
Validation reporting utilities
"""
from typing import Dict, List
from collections import defaultdict


def generate_validation_report(results: List[Dict]) -> str:
    """
    Generate a text report from validation results
    
    Args:
        results: List of validation result dictionaries
    
    Returns:
        Formatted report string
    """
    if not results:
        return "No validation results to report"
    
    # Collect statistics
    total = len(results)
    playable = sum(1 for r in results if r['valid'])
    
    tier_counts = defaultdict(int)
    for r in results:
        tier_counts[r['tier']] += 1
    
    # Build report
    lines = []
    lines.append("=" * 60)
    lines.append("VALIDATION REPORT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Total rooms validated: {total}")
    lines.append(f"Playable rooms:        {playable} ({100 * playable / total:.1f}%)")
    lines.append(f"Unplayable rooms:      {total - playable} ({100 * (total - playable) / total:.1f}%)")
    lines.append("")
    lines.append("TIER DISTRIBUTION:")
    
    tier_emoji = {
        'EASY': '🟢',
        'NORMAL': '🔵',
        'HARD': '🟠',
        'EXPERT': '🔴',
        'IMPOSSIBLE': '⚫'
    }
    
    for tier in ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'IMPOSSIBLE']:
        count = tier_counts[tier]
        if count > 0:
            pct = 100 * count / total
            emoji = tier_emoji.get(tier, '❓')
            lines.append(f"  {emoji} {tier:12s}: {count:3d} ({pct:5.1f}%)")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def format_validation_result(result: Dict) -> str:
    """
    Format a single validation result for display
    
    Args:
        result: Validation result dictionary
    
    Returns:
        Formatted string
    """
    tier = result['tier']
    valid = result['valid']
    
    tier_emoji = {
        'EASY': '🟢',
        'NORMAL': '🔵',
        'HARD': '🟠',
        'EXPERT': '🔴',
        'IMPOSSIBLE': '⚫'
    }
    
    emoji = tier_emoji.get(tier, '❓')
    status = "Playable" if valid else "Unplayable"
    
    output = f"{emoji} {tier} - {status}"
    
    if result.get('errors'):
        output += f"\n  Issues: {', '.join(result['errors'][:3])}"
    
    return output


def save_validation_report(results: List[Dict], output_file: str) -> None:
    """
    Save validation report to file
    
    Args:
        results: List of validation result dictionaries
        output_file: Path to output file
    """
    report = generate_validation_report(results)
    
    with open(output_file, 'w') as f:
        f.write(report)
        f.write("\n\nDETAILED RESULTS:\n")
        f.write("=" * 60 + "\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"\n{i}. Room {result.get('room_id', 'unknown')}\n")
            f.write(f"   {format_validation_result(result)}\n")
            
            if result.get('warnings'):
                f.write(f"   Warnings: {', '.join(result['warnings'])}\n")
