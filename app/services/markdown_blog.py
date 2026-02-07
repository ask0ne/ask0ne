"""Markdown blog service for reading and parsing blog posts from the scribs directory"""

import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import markdown
import yaml


class BlogPost:
    """Represents a blog post with metadata and content"""
    
    def __init__(self, filename: str, title: str, content: str, created_at: datetime, tags: List[str] = None):
        self.filename = filename
        self.title = title.lower()
        self.content = content
        self.created_at = created_at
        self.tags = tags or []
        self._slug = self._generate_slug()
    
    def _generate_slug(self) -> str:
        """Generate URL-friendly slug from filename (without extension)"""
        base_name = Path(self.filename).stem
        # Keep the base name as slug, it's already formatted in the filesystem
        return base_name
    
    @property
    def slug(self) -> str:
        return self._slug
    
    @property
    def text(self) -> str:
        """Return rendered HTML content from markdown"""
        return markdown.markdown(self.content).lower()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert post to dictionary for template rendering"""
        return {
            'title': self.title,
            'slug': self.slug,
            'text': self.text,
            'content': self.content,
            'created_at': self.created_at,
            'tags': self.tags,
            'filename': self.filename
        }


class MarkdownBlogService:
    """Service for managing markdown-based blog posts"""
    
    SCRIBS_DIR = Path(__file__).parent.parent.parent / "scribs"
    
    @classmethod
    def get_all_posts(cls) -> List[BlogPost]:
        """Get all blog posts sorted by created_at (newest first)"""
        posts = []
        
        if not cls.SCRIBS_DIR.exists():
            return posts
        
        for md_file in sorted(cls.SCRIBS_DIR.glob("*.md"), reverse=True):
            post = cls._parse_markdown_file(md_file)
            if post:
                posts.append(post)
        
        # Sort by created_at descending (newest first)
        posts.sort(key=lambda p: p.created_at, reverse=True)
        return posts
    
    @classmethod
    def get_post_by_slug(cls, slug: str) -> Optional[BlogPost]:
        """Get a specific blog post by its slug"""
        filename = f"{slug}.md"
        filepath = cls.SCRIBS_DIR / filename
        
        if filepath.exists():
            return cls._parse_markdown_file(filepath)
        
        return None
    
    @classmethod
    def get_posts_by_tag(cls, tag: str) -> List[BlogPost]:
        """Get all blog posts with a specific tag"""
        all_posts = cls.get_all_posts()
        return [post for post in all_posts if tag.lower() in [t.lower() for t in post.tags]]
    
    @classmethod
    def search_posts(cls, search_term: str) -> List[BlogPost]:
        """Search blog posts by title and content"""
        all_posts = cls.get_all_posts()
        search_term_lower = search_term.lower()
        
        results = []
        for post in all_posts:
            if search_term_lower in post.title.lower() or search_term_lower in post.content.lower():
                results.append(post)
        
        return results
    
    @classmethod
    def _parse_markdown_file(cls, filepath: Path) -> Optional[BlogPost]:
        """Parse a markdown file with YAML frontmatter"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1])
                        markdown_content = parts[2].strip()
                    except yaml.YAMLError:
                        # Fallback if YAML parsing fails
                        frontmatter = {}
                        markdown_content = content
                else:
                    frontmatter = {}
                    markdown_content = content
            else:
                frontmatter = {}
                markdown_content = content
            
            # Extract metadata
            title = frontmatter.get('title', filepath.stem.replace('-', ' ').title())
            tags = frontmatter.get('tags', [])
            
            # Parse created_at date
            created_at_str = frontmatter.get('date')
            if created_at_str:
                try:
                    if isinstance(created_at_str, datetime):
                        created_at = created_at_str
                    else:
                        created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                except (ValueError, AttributeError):
                    created_at = datetime.fromtimestamp(filepath.stat().st_ctime)
            else:
                # Use file creation time as fallback
                created_at = datetime.fromtimestamp(filepath.stat().st_ctime)
            
            return BlogPost(
                filename=filepath.name,
                title=title,
                content=markdown_content,
                created_at=created_at,
                tags=tags
            )
        
        except Exception as e:
            print(f"Error parsing markdown file {filepath}: {e}")
            return None
