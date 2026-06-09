import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime, date, time
from app.database import db
from app.models.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointments CRUD"])

@router.get("", response_model=List[AppointmentResponse])
async def list_appointments(
    barbershop_id: Optional[str] = None,
    client_id: Optional[str] = None,
    barber_id: Optional[str] = None,
    appointment_date: Optional[str] = None  # Format: YYYY-MM-DD
):
    """
    Lista todas las citas de la base de datos, permitiendo filtrar por barbershop_id, client_id, barber_id y fecha.
    """
    where_filter = {}
    if barbershop_id:
        where_filter["barbershop_id"] = barbershop_id
    if client_id:
        where_filter["client_id"] = client_id
    if barber_id:
        where_filter["barber_id"] = barber_id
    if appointment_date:
        try:
            # Parse date and combine with min time to create datetime for database query
            parsed_date = datetime.combine(datetime.strptime(appointment_date, "%Y-%m-%d").date(), datetime.min.time())
            where_filter["appointment_date"] = parsed_date
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de fecha inválido. Use YYYY-MM-DD."
            )

    appointments = await db.appointments.find_many(where=where_filter)
    return appointments

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: str):
    """
    Obtiene los detalles de una cita por su ID.
    """
    appointment = await db.appointments.find_unique(where={"id": appointment_id})
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada."
        )
    return appointment

@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(body: AppointmentCreate):
    """
    Crea una nueva cita (reserva) directamente en la base de datos.
    """
    try:
        date_dt = datetime.combine(body.appointment_date, datetime.min.time())
        start_dt = datetime.combine(date.min, body.start_time)
        end_dt = datetime.combine(date.min, body.end_time)

        new_appointment = await db.appointments.create(
            data={
                "id": str(uuid.uuid4()),
                "barbershop_id": body.barbershop_id,
                "client_id": body.client_id,
                "barber_id": body.barber_id,
                "appointment_date": date_dt,
                "start_time": start_dt,
                "end_time": end_dt,
                "status": "pending",
                "notes": body.notes
            }
        )
        return new_appointment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agendar la cita en BD: {str(e)}"
        )

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(appointment_id: str, body: AppointmentUpdate):
    """
    Actualiza una cita existente en la base de datos.
    """
    appointment = await db.appointments.find_unique(where={"id": appointment_id})
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada."
        )

    update_data = {}
    if body.status is not None:
        update_data["status"] = body.status
    if body.notes is not None:
        update_data["notes"] = body.notes
    if body.appointment_date is not None:
        update_data["appointment_date"] = datetime.combine(body.appointment_date, datetime.min.time())
    if body.start_time is not None:
        update_data["start_time"] = datetime.combine(date.min, body.start_time)
    if body.end_time is not None:
        update_data["end_time"] = datetime.combine(date.min, body.end_time)

    if not update_data:
        return appointment

    try:
        updated = await db.appointments.update(
            where={"id": appointment_id},
            data=update_data
        )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la cita en BD: {str(e)}"
        )

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: str):
    """
    Elimina una cita de la base de datos.
    """
    appointment = await db.appointments.find_unique(where={"id": appointment_id})
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada."
        )

    try:
        await db.appointments.delete(where={"id": appointment_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la cita de la BD: {str(e)}"
        )
