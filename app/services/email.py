import os
from datetime import datetime
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, FileSystemLoader
from app.models.contact import ContactForm

# Set up Jinja2 environment for email templates
template_env = Environment(loader=FileSystemLoader('templates/emails'))

# Email configuration from environment variables
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "The Whelmed Engineers"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "true").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "false").lower() == "true",
    VALIDATE_CERTS=os.getenv("VALIDATE_CERTS", "true").lower() == "true",
    USE_CREDENTIALS=True,
)

# Initialize FastMail
fm = FastMail(conf)

async def send_contact_email(form_data: ContactForm) -> bool:
    """
    Send contact form email to the specified recipient
    """
    try:
        # Email content
        subject = "New Inquiry from The Whelmed Engineers Landing Page"
        
        # Render email template
        template = template_env.get_template('contact_form.html')
        html_body = template.render(
            email=form_data.email,
            phone=form_data.phone,
            message=form_data.message,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        )
        
        # Create message
        message = MessageSchema(
            subject=subject,
            recipients=[os.getenv("CONTACT_EMAIL", "atharva@whelmedthinker.com")],
            body=html_body,
            subtype="html"
        )
        
        # Send email
        await fm.send_message(message)
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

async def send_auto_reply_email(form_data: ContactForm) -> bool:
    """
    Send an auto-reply email to the person who submitted the form
    """
    try:
        subject = "Thank you for contacting The Whelmed Engineers!"
        
        # Render auto-reply template
        template = template_env.get_template('auto_reply.html')
        html_body = template.render(
            email=form_data.email,
            phone=form_data.phone,
            message_preview=form_data.message[:200] + ('...' if len(form_data.message) > 200 else '')
        )
        
        # Create auto-reply message
        message = MessageSchema(
            subject=subject,
            recipients=[form_data.email],
            body=html_body,
            subtype="html"
        )
        
        # Send auto-reply
        await fm.send_message(message)
        return True
        
    except Exception as e:
        print(f"Failed to send auto-reply email: {str(e)}")
        return False