import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, date, time
from app.database import db
from app.models.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("", response_model=List[AppointmentResponse])
async def list_appointments():
    """
    Obtiene todas las citas registradas en el sistema.
    """
    appointments = await db.appointments.find_many()
    return appointments

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: str):
    """
    Obtiene los detalles de una cita específica.
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
    Crea una nueva cita (reserva).
    """
    # 1. Verify barbershop exists
    shop = await db.barbershops.find_unique(where={"id": body.barbershop_id})
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La barbería seleccionada no existe."
        )

    # 2. Verify client exists
    client = await db.public_users.find_unique(where={"id": body.client_id})
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente especificado no existe."
        )

    # 3. Verify barber exists
    barber = await db.public_users.find_unique(where={"id": body.barber_id})
    if not barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El barbero especificado no existe."
        )

    try:
        # Convert date and time fields into Python datetime objects to store in PostgreSQL.
        # Prisma Python expects python datetime objects.
        # date is converted to datetime at midnight.
        # time is stored as datetime at minimum date.
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
                "notes": body.notes,
                "created_at": datetime.now()
            }
        )
        return new_appointment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agendar la cita: {str(e)}"
        )

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(appointment_id: str, body: AppointmentUpdate):
    """
    Modifica una cita existente (reprogramar, cambiar estado o notas).
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
        updated_appointment = await db.appointments.update(
            where={"id": appointment_id},
            data=update_data
        )
        return updated_appointment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la cita: {str(e)}"
        )

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: str):
    """
    Cancela/elimina una cita del sistema.
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
            detail=f"Error al eliminar la cita: {str(e)}"
        )
