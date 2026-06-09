from pydantic import BaseModel, field_validator
from typing import Optional, Any
from datetime import time, datetime

class AvailabilityCreate(BaseModel):
    barbershop_id: str
    barber_id: str
    day_of_week: int
    start_time: time
    end_time: time
    is_available: Optional[bool] = True

class AvailabilityUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_available: Optional[bool] = None

class AvailabilityResponse(BaseModel):
    id: str
    barbershop_id: str
    barber_id: str
    day_of_week: int
    start_time: time
    end_time: time
    is_available: Optional[bool] = True

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def convert_datetime_to_time(cls, v: Any) -> Any:
        if isinstance(v, datetime):
            return v.time()
        return v

    class Config:
        from_attributes = True
