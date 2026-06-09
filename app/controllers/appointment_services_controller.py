import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.database import db
from app.models.schemas.appointment_services_schema import AppointmentServiceCreate, AppointmentServiceResponse

router = APIRouter(prefix="/appointment-services", tags=["Appointment Services CRUD"])

@router.get("", response_model=List[AppointmentServiceResponse])
async def list_appointment_services(appointment_id: Optional[str] = None, service_id: Optional[str] = None):
    """
    Lista las relaciones entre citas y servicios, permitiendo filtrar por appointment_id y/o service_id.
    """
    where_filter = {}
    if appointment_id:
        where_filter["appointment_id"] = appointment_id
    if service_id:
        where_filter["service_id"] = service_id

    relations = await db.appointment_services.find_many(where=where_filter)
    return relations

@router.get("/{relation_id}", response_model=AppointmentServiceResponse)
async def get_appointment_service(relation_id: str):
    """
    Obtiene los detalles de una relación cita-servicio por su ID.
    """
    relation = await db.appointment_services.find_unique(where={"id": relation_id})
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación cita-servicio no encontrada."
        )
    return relation

@router.post("", response_model=AppointmentServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment_service(body: AppointmentServiceCreate):
    """
    Vincula un servicio a una cita en la base de datos.
    """
    # Check duplicate
    existing = await db.appointment_services.find_first(
        where={
            "appointment_id": body.appointment_id,
            "service_id": body.service_id
        }
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El servicio ya está vinculado a esta cita."
        )

    try:
        new_relation = await db.appointment_services.create(
            data={
                "id": str(uuid.uuid4()),
                "appointment_id": body.appointment_id,
                "service_id": body.service_id
            }
        )
        return new_relation
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al vincular el servicio a la cita en BD: {str(e)}"
        )

@router.delete("/{relation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment_service(relation_id: str):
    """
    Desvincula un servicio de una cita por el ID de la relación.
    """
    relation = await db.appointment_services.find_unique(where={"id": relation_id})
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación cita-servicio no encontrada."
        )

    try:
        await db.appointment_services.delete(where={"id": relation_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la relación cita-servicio en BD: {str(e)}"
        )

@router.delete("/appointment/{appointment_id}/service/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_ids(appointment_id: str, service_id: str):
    """
    Desvincula un servicio de una cita usando directamente el ID de la cita y del servicio.
    """
    relation = await db.appointment_services.find_first(
        where={
            "appointment_id": appointment_id,
            "service_id": service_id
        }
    )
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación cita-servicio no encontrada para los IDs provistos."
        )

    try:
        await db.appointment_services.delete(where={"id": relation.id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desvincular el servicio de la cita: {str(e)}"
        )
