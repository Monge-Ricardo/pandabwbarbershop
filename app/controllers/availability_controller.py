import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime, date, time
from app.database import db
from app.models.schemas.availability_schema import AvailabilityCreate, AvailabilityUpdate, AvailabilityResponse

router = APIRouter(prefix="/availabilities", tags=["Availability CRUD"])

@router.get("", response_model=List[AvailabilityResponse])
async def list_availabilities(barber_id: Optional[str] = None, barbershop_id: Optional[str] = None):
    """
    Lista todos los bloques de disponibilidad, permitiendo filtrar por barber_id y barbershop_id.
    """
    where_filter = {}
    if barber_id:
        where_filter["barber_id"] = barber_id
    if barbershop_id:
        where_filter["barbershop_id"] = barbershop_id

    availabilities = await db.availability.find_many(where=where_filter)
    return availabilities

@router.get("/{availability_id}", response_model=AvailabilityResponse)
async def get_availability(availability_id: str):
    """
    Obtiene los detalles de un bloque de disponibilidad por su ID.
    """
    av = await db.availability.find_unique(where={"id": availability_id})
    if not av:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bloque de disponibilidad no encontrado."
        )
    return av

@router.post("", response_model=AvailabilityResponse, status_code=status.HTTP_201_CREATED)
async def create_availability(body: AvailabilityCreate):
    """
    Registra un nuevo bloque de disponibilidad para un barbero en BD.
    """
    try:
        start_dt = datetime.combine(date.min, body.start_time)
        end_dt = datetime.combine(date.min, body.end_time)

        new_av = await db.availability.create(
            data={
                "id": str(uuid.uuid4()),
                "barbershop_id": body.barbershop_id,
                "barber_id": body.barber_id,
                "day_of_week": body.day_of_week,
                "start_time": start_dt,
                "end_time": end_dt,
                "is_available": body.is_available
            }
        )
        return new_av
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear disponibilidad en BD: {str(e)}"
        )

@router.put("/{availability_id}", response_model=AvailabilityResponse)
async def update_availability(availability_id: str, body: AvailabilityUpdate):
    """
    Actualiza un bloque de disponibilidad existente en la BD.
    """
    av = await db.availability.find_unique(where={"id": availability_id})
    if not av:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bloque de disponibilidad no encontrado."
        )

    update_data = {}
    if body.day_of_week is not None:
        update_data["day_of_week"] = body.day_of_week
    if body.start_time is not None:
        update_data["start_time"] = datetime.combine(date.min, body.start_time)
    if body.end_time is not None:
        update_data["end_time"] = datetime.combine(date.min, body.end_time)
    if body.is_available is not None:
        update_data["is_available"] = body.is_available

    if not update_data:
        return av

    try:
        updated = await db.availability.update(
            where={"id": availability_id},
            data=update_data
        )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar disponibilidad en BD: {str(e)}"
        )

@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_availability(availability_id: str):
    """
    Elimina un bloque de disponibilidad de la base de datos.
    """
    av = await db.availability.find_unique(where={"id": availability_id})
    if not av:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bloque de disponibilidad no encontrado."
        )

    try:
        await db.availability.delete(where={"id": availability_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar disponibilidad de la BD: {str(e)}"
        )
