from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from app.core.config import templates
from app.db.blog import BlogDatabase

router = APIRouter()

@router.get("/blog", response_class=HTMLResponse)
async def get_blog_list(request: Request, tag: Optional[str] = Query(None), search: Optional[str] = Query(None)):
    """Get all blog posts, optionally filtered by tag or search term"""
    if tag:
        posts = BlogDatabase.get_posts_by_tag(tag)
    elif search:
        posts = BlogDatabase.search_posts(search)
    else:
        posts = BlogDatabase.get_all_posts()
    
    return templates.TemplateResponse("list.html", {
        "request": request, 
        "posts": posts
    })

# New route for blog posts with clean URLs under /scribblings/
@router.get("/scribblings/{slug}", response_class=HTMLResponse)
async def get_blog_post_by_slug(request: Request, slug: str):
    """Get a specific blog post by slug under /scribblings/"""
    post = BlogDatabase.get_post_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse("detail.html", {
        "request": request,
        "post": post
    })

# Keep old route for backwards compatibility
@router.get("/blog/{post_id}", response_class=HTMLResponse)
async def get_blog_post(request: Request, post_id: int):
    """Get a specific blog post by ID"""
    post = BlogDatabase.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse("detail.html", {
        "request": request,
        "post": post
    })