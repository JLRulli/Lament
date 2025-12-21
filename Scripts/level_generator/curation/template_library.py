"""
Template library management system

Manages a curated collection of high-quality room templates.
"""
import json
from typing import List, Dict, Any, Optional


class TemplateLibrary:
    """
    Manages a collection of validated, quality-scored room templates
    
    Provides filtering, tagging, and export capabilities for building
    a curated library of reusable room templates.
    """
    
    def __init__(self):
        self.templates = []
    
    def add_template(self, room, validation: Dict, quality: Dict):
        """
        Add a template to the library
        
        Args:
            room: RoomTemplate object
            validation: Validation results dict
            quality: Quality scoring results dict
        """
        template = {
            'room': room,
            'validation': validation,
            'quality': quality,
            'tags': self._auto_tag(room, validation, quality),
            'id': room.id
        }
        self.templates.append(template)
    
    def _auto_tag(self, room, validation: Dict, quality: Dict) -> List[str]:
        """
        Automatically generate tags for a template
        
        Tags help with filtering and selection during runtime.
        
        Args:
            room: RoomTemplate object
            validation: Validation results
            quality: Quality scores
        
        Returns:
            List of tag strings
        """
        tags = []
        
        # Shape tag
        tags.append(f"shape_{room.shape_type}")
        
        # Difficulty tier tag
        tier = validation.get('tier', 'NORMAL')
        tags.append(f"tier_{tier.lower()}")
        
        # Beginner-friendly tag
        if tier in ['EASY', 'NORMAL']:
            tags.append('beginner_friendly')
        
        # Expert tag
        if tier == 'EXPERT':
            tags.append('expert_only')
        
        # Quality tags
        overall_quality = quality.get('overall', 0)
        if overall_quality >= 8.0:
            tags.append('exceptional')
        elif overall_quality >= 7.0:
            tags.append('high_quality')
        elif overall_quality >= 6.0:
            tags.append('good_quality')
        
        # Challenge type tags
        if validation.get('spike_count', 0) >= 8:
            tags.append('spike_heavy')
        
        if validation.get('platform_count', 0) >= 6:
            tags.append('platform_heavy')
        
        # Special features
        if quality.get('has_secret_area', False):
            tags.append('has_secret')
        
        return tags
    
    def filter(
        self,
        min_quality: Optional[float] = None,
        max_quality: Optional[float] = None,
        tier: Optional[str] = None,
        tags: Optional[List[str]] = None,
        shape: Optional[str] = None
    ) -> List[Dict]:
        """
        Filter templates by various criteria
        
        Args:
            min_quality: Minimum overall quality score
            max_quality: Maximum overall quality score
            tier: Difficulty tier (EASY, NORMAL, HARD, EXPERT)
            tags: List of required tags (template must have ALL)
            shape: Room shape type
        
        Returns:
            List of matching template dicts
        """
        results = self.templates
        
        # Filter by quality range
        if min_quality is not None:
            results = [t for t in results if t['quality']['overall'] >= min_quality]
        
        if max_quality is not None:
            results = [t for t in results if t['quality']['overall'] <= max_quality]
        
        # Filter by tier
        if tier is not None:
            results = [t for t in results if t['validation']['tier'] == tier]
        
        # Filter by shape
        if shape is not None:
            results = [t for t in results if t['room'].shape_type == shape]
        
        # Filter by tags (must have ALL specified tags)
        if tags is not None:
            results = [
                t for t in results
                if all(tag in t['tags'] for tag in tags)
            ]
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the library
        
        Returns:
            Dict with various statistics
        """
        if not self.templates:
            return {
                'total': 0,
                'by_tier': {},
                'by_shape': {},
                'avg_quality': 0,
                'quality_distribution': {}
            }
        
        # Count by tier
        by_tier = {}
        for t in self.templates:
            tier = t['validation']['tier']
            by_tier[tier] = by_tier.get(tier, 0) + 1
        
        # Count by shape
        by_shape = {}
        for t in self.templates:
            shape = t['room'].shape_type
            by_shape[shape] = by_shape.get(shape, 0) + 1
        
        # Average quality
        avg_quality = sum(t['quality']['overall'] for t in self.templates) / len(self.templates)
        
        # Quality distribution
        quality_dist = {
            'exceptional (8.0+)': len([t for t in self.templates if t['quality']['overall'] >= 8.0]),
            'high (7.0-7.9)': len([t for t in self.templates if 7.0 <= t['quality']['overall'] < 8.0]),
            'good (6.0-6.9)': len([t for t in self.templates if 6.0 <= t['quality']['overall'] < 7.0]),
            'acceptable (5.0-5.9)': len([t for t in self.templates if 5.0 <= t['quality']['overall'] < 6.0]),
            'poor (<5.0)': len([t for t in self.templates if t['quality']['overall'] < 5.0])
        }
        
        return {
            'total': len(self.templates),
            'by_tier': by_tier,
            'by_shape': by_shape,
            'avg_quality': round(avg_quality, 2),
            'quality_distribution': quality_dist
        }
    
    def export_catalog(self, filename: str):
        """
        Export a catalog of templates (metadata only, no tilemap data)
        
        Creates a JSON file with template metadata for quick lookup.
        
        Args:
            filename: Output JSON file path
        """
        catalog = {
            'total': len(self.templates),
            'statistics': self.get_statistics(),
            'templates': [
                {
                    'id': t['id'],
                    'shape': t['room'].shape_type,
                    'dimensions': {
                        'width': t['room'].width,
                        'height': t['room'].height
                    },
                    'tier': t['validation']['tier'],
                    'quality': round(t['quality']['overall'], 2),
                    'tags': t['tags'],
                    'features': {
                        'spike_count': t['validation'].get('spike_count', 0),
                        'platform_count': t['validation'].get('platform_count', 0),
                        'floor_coverage': round(t['validation'].get('floor_coverage', 0), 2)
                    }
                }
                for t in self.templates
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(catalog, f, indent=2)
    
    def sort_by_quality(self, descending: bool = True):
        """
        Sort templates by quality score
        
        Args:
            descending: If True, best quality first
        """
        self.templates.sort(
            key=lambda t: t['quality']['overall'],
            reverse=descending
        )
    
    def keep_top_n(self, n: int):
        """
        Keep only the top N templates by quality
        
        Args:
            n: Number of templates to keep
        """
        self.sort_by_quality(descending=True)
        self.templates = self.templates[:n]
    
    def remove_duplicates(self, similarity_threshold: float = 0.95):
        """
        Remove near-duplicate templates (placeholder for future implementation)
        
        Args:
            similarity_threshold: How similar templates must be to be considered duplicates
        """
        # TODO: Implement similarity detection
        # For now, just remove exact ID duplicates
        seen_ids = set()
        unique_templates = []
        
        for t in self.templates:
            if t['id'] not in seen_ids:
                seen_ids.add(t['id'])
                unique_templates.append(t)
        
        removed = len(self.templates) - len(unique_templates)
        self.templates = unique_templates
        
        return removed
