from pydantic import BaseModel, EmailStr, Field
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


class TalkForm(BaseModel):
    who: str = Field(min_length=3, max_length=200)
    what: str = Field(min_length=1, max_length=2000)
    website: str = ""  # honeypot: real visitors never fill it
