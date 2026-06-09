from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BarbershopMemberCreate(BaseModel):
    barbershop_id: str
    user_id: str
    role: str
    status: Optional[str] = "active"

class BarbershopMemberUpdate(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None

class BarbershopMemberResponse(BaseModel):
    id: str
    barbershop_id: str
    user_id: str
    role: str
    status: Optional[str] = None
    joined_at: Optional[datetime] = None

    class Config:
        from_attributes = True
