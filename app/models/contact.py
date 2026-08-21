from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "user@example.com",
                "phone": "+1234567890",
                "message": "I'm interested in your AI automation services."
            }
        }