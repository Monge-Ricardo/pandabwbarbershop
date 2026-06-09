from pydantic import BaseModel

class AppointmentServiceCreate(BaseModel):
    appointment_id: str
    service_id: str

class AppointmentServiceResponse(BaseModel):
    id: str
    appointment_id: str
    service_id: str

    class Config:
        from_attributes = True
