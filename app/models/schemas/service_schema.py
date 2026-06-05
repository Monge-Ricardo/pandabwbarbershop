from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ServiceCreate(BaseModel):
    barbershop_id: str
    name: str
    description: Optional[str] = None
    price: Decimal
    duration_minutes: int

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None

class ServiceResponse(BaseModel):
    id: str
    barbershop_id: str
    name: str
    description: Optional[str] = None
    price: Decimal
    duration_minutes: int
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
