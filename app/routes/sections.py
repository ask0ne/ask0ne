import json

from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from app.core.config import templates
from app.services.markdown_blog import MarkdownBlogService
from app.models.contact import ContactForm
from app.services.email import send_contact_email, send_auto_reply_email

router = APIRouter()

# Per-section page metadata. htmx only swaps #main-content, so the title,
# description and canonical URL have to travel with the partial as well.
SECTION_META = {
    "me": {
        "template": "sections/me.html",
        "path": "/me",
        "title": "atharva kawade - software engineer & ai optimist",
        "description": "software engineer with 4+ years in early stage startups, currently at arise. previously oleander and mortgage kart.",
    },
    "work": {
        "template": "sections/work.html",
        "path": "/work",
        "title": "work - atharva kawade",
        "description": "projects atharva kawade has built, from sql visualisation with llms to a teen digital wallet.",
    },
    "cv": {
        "template": "sections/cv.html",
        "path": "/cv",
        "title": "cv - atharva kawade",
        "description": "experience, skills, achievements and education for atharva kawade, software engineer and ai engineer.",
    },
    "thoughts": {
        "template": "sections/scribblings.html",
        "path": "/thoughts",
        "title": "thoughts - atharva kawade",
        "description": "random thoughts, ramblings and anecdotes from atharva kawade - short reads and quick notes.",
    },
    "tangents": {
        "template": "sections/mystery.html",
        "path": "/tangents",
        "title": "tangents - atharva kawade",
        "description": "talks, videos and essays atharva kawade keeps coming back to.",
    },
    "whelmed": {
        "template": "sections/whelmed.html",
        "path": "/whelmed",
        "title": "the whelmed engineers - ai & automation services",
        "description": "ai and automation services that cut manual work and ship measurable outcomes.",
    },
    "cases": {
        "template": "sections/cases.html",
        "path": "/cases",
        "title": "case studies - the whelmed engineers",
        "description": "ai and automation case studies with the problems, the builds and the measured results.",
    },
}

def is_htmx_request(request: Request) -> bool:
    """Check if request is coming from HTMX"""
    return request.headers.get("hx-request") is not None

def render_section(request: Request, section_id: str, **extra_context):
    """Render a section as an HTMX partial or a full page, carrying page metadata either way"""
    meta = SECTION_META[section_id]
    context = {"request": request, "section_id": section_id, **extra_context}

    if is_htmx_request(request):
        # Return partial template for HTMX requests
        response = templates.TemplateResponse(meta["template"], context)
        response.headers["HX-Trigger"] = json.dumps({
            "pageMeta": {
                "title": meta["title"],
                "description": meta["description"],
                "path": meta["path"],
                "section_id": section_id,
            }
        })
        return response

    # Return full page for direct access
    context.update({
        "content_template": meta["template"],
        "page_title": meta["title"],
        "page_description": meta["description"],
        "canonical_path": meta["path"],
    })
    return templates.TemplateResponse("base.html", context)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render_section(request, "me")

# Individual routes for each section with clean URLs
@router.get("/me", response_class=HTMLResponse)
async def get_me_section(request: Request):
    return render_section(request, "me")

@router.get("/work", response_class=HTMLResponse)
async def get_work_section(request: Request):
    return render_section(request, "work")

@router.get("/cv", response_class=HTMLResponse)
async def get_cv_section(request: Request):
    return render_section(request, "cv")

@router.get("/whelmed", response_class=HTMLResponse)
async def get_whelmed_section(request: Request):
    """The Whelmed Engineers - AI & Automation Services"""
    return render_section(request, "whelmed")

@router.get("/cases", response_class=HTMLResponse)
async def get_cases_section(request: Request):
    """Case Studies - AI & Automation Success Stories"""
    return render_section(request, "cases")

@router.get("/thoughts", response_class=HTMLResponse)
async def get_thoughts_section(request: Request):
    posts = MarkdownBlogService.get_all_posts()
    # Convert post objects to dictionaries for template rendering
    posts_dicts = [post.to_dict() for post in posts]
    return render_section(request, "thoughts", posts=posts_dicts)

@router.get("/tangents", response_class=HTMLResponse)
async def get_tangents_section(request: Request):
    return render_section(request, "tangents")

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

@router.post("/contact")
async def submit_contact_form(
    email: str = Form(...),
    message: str = Form(...),
    phone: str = Form(None),
):
    """
    Handle contact form submission and send emails
    """
    try:
        form_data = ContactForm(email=email, message=message, phone=phone or None)
        # Send notification email to the business
        email_sent = await send_contact_email(form_data)
        
        # Send auto-reply to the customer
        auto_reply_sent = await send_auto_reply_email(form_data)
        
        if email_sent:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "Thank you for your message! We'll get back to you within 24 hours.",
                    "auto_reply_sent": auto_reply_sent
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": "Sorry, there was an error sending your message. Please try again or contact us directly."
                }
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Sorry, there was an error processing your request. Please try again later."
            }
        )
