from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from app.core.config import templates
from app.db.blog import BlogDatabase

router = APIRouter()

def is_htmx_request(request: Request) -> bool:
    """Check if request is coming from HTMX"""
    return request.headers.get("hx-request") is not None

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {
            "request": request,
            "section_id": "me",
            "content_template": "sections/me.html"
        })

# Individual routes for each section with clean URLs
@router.get("/me", response_class=HTMLResponse)
async def get_me_section(request: Request):
    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("sections/me.html", {
            "request": request, 
            "section_id": "me"
        })
    else:
        # Return full page for direct access
        return templates.TemplateResponse("base.html", {
            "request": request,
            "section_id": "me",
            "content_template": "sections/me.html"
        })

@router.get("/work", response_class=HTMLResponse)
async def get_work_section(request: Request):
    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("sections/work.html", {
            "request": request, 
            "section_id": "work"
        })
    else:
        # Return full page for direct access
        return templates.TemplateResponse("base.html", {
            "request": request,
            "section_id": "work",
            "content_template": "sections/work.html"
        })

@router.get("/cv", response_class=HTMLResponse)
async def get_cv_section(request: Request):
    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("sections/cv.html", {
            "request": request, 
            "section_id": "cv"
        })
    else:
        # Return full page for direct access
        return templates.TemplateResponse("base.html", {
            "request": request,
            "section_id": "cv",
            "content_template": "sections/cv.html"
        })

@router.get("/thoughts", response_class=HTMLResponse)
async def get_thoughts_section(request: Request):
    posts = await BlogDatabase.get_all_posts()
    context = {
        "request": request, 
        "section_id": "thoughts",
        "posts": posts
    }

    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("sections/scribblings.html", context)
    else:
        # Return full page for direct access
        context["content_template"] = "sections/scribblings.html"
        return templates.TemplateResponse("base.html", context)

@router.get("/tangents", response_class=HTMLResponse)
async def get_tangents_section(request: Request):
    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("sections/mystery.html", {
            "request": request, 
            "section_id": "tangents"
        })
    else:
        # Return full page for direct access
        return templates.TemplateResponse("base.html", {
            "request": request,
            "section_id": "tangents",
            "content_template": "sections/mystery.html"
        })

# Backwards compatibility routes
@router.get("/scribblings", response_class=HTMLResponse)
async def redirect_scribblings_to_thoughts(request: Request):
    """Redirect old scribblings URL to thoughts"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/thoughts", status_code=301)

@router.get("/mindfield", response_class=HTMLResponse)
async def redirect_mindfield_to_tangents(request: Request):
    """Redirect old mindfield URL to tangents"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/tangents", status_code=301)
