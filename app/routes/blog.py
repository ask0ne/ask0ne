import json

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

    post_dict = post.to_dict()
    context = {
        "request": request,
        "post": post_dict
    }

    page_title = f"{post_dict['title']} - atharva kawade"
    page_description = post_dict["title"]
    canonical_path = f"/thoughts/{slug}"

    if is_htmx_request(request):
        # Return partial template for HTMX requests
        response = templates.TemplateResponse("detail.html", context)
        response.headers["HX-Trigger"] = json.dumps({
            "pageMeta": {
                "title": page_title,
                "description": page_description,
                "path": canonical_path,
                "section_id": "thoughts",
            }
        })
        return response
    else:
        # Return full page for direct access
        context.update({
            "content_template": "detail.html",
            "section_id": "thoughts",
            "page_title": page_title,
            "page_description": page_description,
            "canonical_path": canonical_path,
        })
        return templates.TemplateResponse("base.html", context)
