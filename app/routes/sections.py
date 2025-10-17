from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from app.core.config import templates
from app.db.blog import BlogDatabase
from app.models.contact import ContactForm
from app.services.email import send_contact_email, send_auto_reply_email

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

@router.get("/whelmed", response_class=HTMLResponse)
async def get_whelmed_section(request: Request):
    """The Whelmed Engineers - AI & Automation Services"""
    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("sections/whelmed.html", {
            "request": request, 
            "section_id": "whelmed"
        })
    else:
        # Return full page for direct access
        return templates.TemplateResponse("base.html", {
            "request": request,
            "section_id": "whelmed",
            "content_template": "sections/whelmed.html"
        })

@router.get("/cases", response_class=HTMLResponse)
async def get_cases_section(request: Request):
    """Case Studies - AI & Automation Success Stories"""
    if is_htmx_request(request):
        # Return partial template for HTMX requests
        return templates.TemplateResponse("sections/cases.html", {
            "request": request, 
            "section_id": "cases"
        })
    else:
        # Return full page for direct access
        return templates.TemplateResponse("base.html", {
            "request": request,
            "section_id": "cases",
            "content_template": "sections/cases.html"
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

@router.post("/contact")
async def submit_contact_form(form_data: ContactForm):
    """
    Handle contact form submission and send emails
    """
    try:
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
