from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from typing import Optional
from app.core.config import templates
from app.db.blog import BlogDatabase

router = APIRouter()

def is_htmx_request(request: Request) -> bool:
    """Check if request is coming from HTMX"""
    return request.headers.get("hx-request") is not None

@router.get("/scribblings/{slug}", response_class=HTMLResponse)
async def get_blog_post_by_slug(request: Request, slug: str):
    """Get a specific blog post by slug under /scribblings/"""
    post = await BlogDatabase.get_post_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    context = {
        "request": request,
        "post": post
    }
    
    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("detail.html", context)
    else:
        # Return full page for direct access
        context["content_template"] = "detail.html"
        return templates.TemplateResponse("base.html", context)
