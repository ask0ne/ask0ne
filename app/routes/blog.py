from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from app.core.config import templates
from app.services.markdown_blog import MarkdownBlogService

router = APIRouter()

def is_htmx_request(request: Request) -> bool:
    """Check if request is coming from HTMX"""
    return request.headers.get("hx-request") is not None

@router.get("/thoughts/{slug}", response_class=HTMLResponse)
async def get_blog_post_by_slug(request: Request, slug: str):
    """Get a specific blog post by slug under /thoughts/"""
    post = MarkdownBlogService.get_post_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    context = {
        "request": request,
        "post": post.to_dict()
    }
    
    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("detail.html", context)
    else:
        # Return full page for direct access
        context["content_template"] = "detail.html"
        return templates.TemplateResponse("base.html", context)
