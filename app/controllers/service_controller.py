import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from decimal import Decimal
from app.database import db
from app.models.schemas.service_schema import ServiceCreate, ServiceUpdate, ServiceResponse

router = APIRouter(prefix="/services", tags=["Services CRUD"])

@router.get("", response_model=List[ServiceResponse])
async def list_services(barbershop_id: Optional[str] = None):
    """
    Lista todos los servicios del sistema, permitiendo filtrar por barbershop_id.
    """
    if barbershop_id:
        services = await db.services.find_many(where={"barbershop_id": barbershop_id})
    else:
        services = await db.services.find_many()
    return services

@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: str):
    """
    Obtiene los detalles de un servicio por su ID.
    """
    service = await db.services.find_unique(where={"id": service_id})
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado."
        )
    return service

@router.post("", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(body: ServiceCreate):
    """
    Crea un nuevo servicio en la base de datos.
    """
    try:
        new_service = await db.services.create(
            data={
                "id": str(uuid.uuid4()),
                "barbershop_id": body.barbershop_id,
                "name": body.name,
                "description": body.description,
                "price": Decimal(str(body.price)),
                "duration_minutes": body.duration_minutes,
                "is_active": True
            }
        )
        return new_service
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el servicio en BD: {str(e)}"
        )

@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(service_id: str, body: ServiceUpdate):
    """
    Actualiza un servicio existente en la base de datos.
    """
    service = await db.services.find_unique(where={"id": service_id})
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado."
        )

    update_data = body.model_dump(exclude_unset=True)
    if "price" in update_data and update_data["price"] is not None:
        update_data["price"] = Decimal(str(update_data["price"]))
        
    if not update_data:
        return service

    try:
        updated = await db.services.update(
            where={"id": service_id},
            data=update_data
        )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el servicio en BD: {str(e)}"
        )

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: str):
    """
    Elimina un servicio de la base de datos.
    """
    service = await db.services.find_unique(where={"id": service_id})
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado."
        )

    try:
        await db.services.delete(where={"id": service_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el servicio de la BD: {str(e)}"
        )
