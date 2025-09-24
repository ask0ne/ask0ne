from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

class BlogPostData(BaseModel):
    """JSONB data structure for blog posts"""
    title: Optional[str] = Field(None, description="The title of the blog post")
    text: str = Field(..., description="The blog post content")
    tags: List[str] = Field(default_factory=list, description="List of tags for the blog post")

class BlogPost(BaseModel):
    """Main blog post model matching PostgreSQL schema"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    data: BlogPostData

    @property
    def title(self) -> Optional[str]:
        """Convenience property to access the blog title"""
        return self.data.title

    @property
    def text(self) -> str:
        """Convenience property to access the blog text"""
        return self.data.text

    @property  
    def tags(self) -> List[str]:
        """Convenience property to access the blog tags"""
        return self.data.tags

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

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "text": "This is a sample blog post content with some meaningful text.",
                    "tags": ["fastapi", "python", "web-development"]
                }
            }
        }

class BlogPostCreate(BaseModel):
    """Model for creating new blog posts"""
    data: BlogPostData

class BlogPostUpdate(BaseModel):
    """Model for updating existing blog posts"""
    data: Optional[BlogPostData] = None