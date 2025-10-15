from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactForm(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "phone": "+1234567890",
                "message": "I'm interested in your AI automation services."
            }
        }