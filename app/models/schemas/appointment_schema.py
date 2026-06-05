from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class AppointmentCreate(BaseModel):
    barbershop_id: str
    client_id: str
    barber_id: str
    appointment_date: date
    start_time: time
    end_time: time
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: str
    barbershop_id: str
    client_id: str
    barber_id: str
    appointment_date: date
    start_time: time
    end_time: time
    status: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
