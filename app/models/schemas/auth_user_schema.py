from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AuthUserCreate(BaseModel):
    id: str
    email: str
    encrypted_password: str
    aud: Optional[str] = "authenticated"
    role: Optional[str] = "authenticated"

class AuthUserUpdate(BaseModel):
    email: Optional[str] = None
    encrypted_password: Optional[str] = None
    aud: Optional[str] = None
    role: Optional[str] = None

class AuthUserResponse(BaseModel):
    id: str
    email: Optional[str] = None
    encrypted_password: Optional[str] = None
    aud: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
