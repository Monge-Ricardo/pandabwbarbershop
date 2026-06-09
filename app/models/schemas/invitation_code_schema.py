from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InvitationCodeCreate(BaseModel):
    barbershop_id: str
    code: str
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = True

class InvitationCodeUpdate(BaseModel):
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class InvitationCodeResponse(BaseModel):
    id: str
    barbershop_id: str
    code: str
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
