from typing import List, Optional
from app.models.blog import BlogPost

class BlogDatabase:
    """Wrapper class for blog database operations using Tortoise ORM"""
    
    @staticmethod
    async def get_all_posts() -> List[BlogPost]:
        """Fetch all blog posts"""
        return await BlogPost.all()
    
    @staticmethod
    async def get_post_by_id(post_id: int) -> Optional[BlogPost]:
        """Fetch a specific blog post by ID"""
        return await BlogPost.get_or_none(id=post_id)
    
    @staticmethod
    async def get_posts_by_tag(tag: str) -> List[BlogPost]:
        """Fetch blog posts that contain a specific tag"""
        return await BlogPost.get_posts_by_tag(tag)
    
    @staticmethod
    async def search_posts(search_term: str) -> List[BlogPost]:
        """Search blog posts by text content and title"""
        return await BlogPost.search_posts(search_term)
    
    @staticmethod
    async def get_post_by_slug(slug: str) -> Optional[BlogPost]:
        """Fetch a blog post by its URL slug"""
        return await BlogPost.get_by_slug(slug)