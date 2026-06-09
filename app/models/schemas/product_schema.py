from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProductCreate(BaseModel):
    barbershop_id: str
    name: str
    description: Optional[str] = None
    price: Optional[float] = 0.0
    stock: Optional[int] = 0
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class ProductResponse(BaseModel):
    id: str
    barbershop_id: str
    name: str
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: float(v) if v is not None else None
        }
