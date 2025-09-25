from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Optional, List
import re

class BlogPost(Model):
    """Tortoise ORM model for blog posts with JSONB data column"""
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    # Keep the existing JSONB structure
    data = fields.JSONField()
    
    class Meta:
        table = "blog"
        ordering = ["-created_at"]
    
    @property
    def title(self) -> Optional[str]:
        """Get title from JSONB data"""
        return self.data.get('title') if self.data else None
    
    @property
    def text(self) -> str:
        """Get text from JSONB data"""
        return self.data.get('text', '') if self.data else ''
    
    @property
    def tags(self) -> List[str]:
        """Get tags from JSONB data"""
        return self.data.get('tags', []) if self.data else []
    
    @property
    def slug(self) -> str:
        """Generate URL-friendly slug from title"""
        if not self.title:
            return f"post-{self.id}" if self.id else "untitled-post"
        
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = self.title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars except hyphens
        slug = re.sub(r'[-\s]+', '-', slug)   # Replace spaces and multiple hyphens with single hyphen
        slug = slug.strip('-')                # Remove leading/trailing hyphens
        
        return slug if slug else f"post-{self.id}" if self.id else "untitled-post"
    
    @classmethod
    async def get_by_slug(cls, slug: str) -> Optional['BlogPost']:
        """Get a blog post by its slug"""
        # Since slug is generated from title, we need to find posts and check slugs
        posts = await cls.all()
        for post in posts:
            if post.slug == slug:
                return post
        return None
    
    @classmethod
    async def search_posts(cls, search_term: str) -> List['BlogPost']:
        """Search blog posts by title and text content in JSONB data"""
        # Get all posts and filter in Python since JSONB text search is complex
        posts = await cls.all()
        search_lower = search_term.lower()
        
        matching_posts = []
        for post in posts:
            title = post.title or ""
            text = post.text or ""
            if search_lower in title.lower() or search_lower in text.lower():
                matching_posts.append(post)
        
        return matching_posts
    
    @classmethod
    async def get_posts_by_tag(cls, tag: str) -> List['BlogPost']:
        """Get posts that contain a specific tag in JSONB data"""
        posts = await cls.all()
        # Filter posts that have the tag in their data.tags array
        return [post for post in posts if tag in post.tags]

# Create Pydantic models from Tortoise model for API responses
BlogPostPydantic = pydantic_model_creator(BlogPost, name="BlogPost")
BlogPostInPydantic = pydantic_model_creator(BlogPost, name="BlogPostIn", exclude_readonly=True)