import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import db
from app.models.schemas.service_schema import ServiceCreate, ServiceUpdate, ServiceResponse

router = APIRouter(tags=["Services"])

@router.get("/services", response_model=List[ServiceResponse])
async def list_global_services():
    """
    Obtiene la lista de todos los servicios registrados en todo el sistema.
    """
    services = await db.services.find_many()
    return services

@router.get("/barbershops/{shop_id}/services", response_model=List[ServiceResponse])
async def list_shop_services(shop_id: str):
    """
    Obtiene todos los servicios ofrecidos por una barbería específica.
    """
    # Verify if shop exists
    shop = await db.barbershops.find_unique(where={"id": shop_id})
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada."
        )

    services = await db.services.find_many(where={"barbershop_id": shop_id})
    return services

@router.post("/barbershops/{shop_id}/services", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(shop_id: str, body: ServiceCreate):
    """
    Crea un nuevo servicio dentro de una barbería.
    """
    if body.barbershop_id != shop_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de la barbería en la ruta no coincide con el cuerpo de la petición."
        )

    # Verify if shop exists
    shop = await db.barbershops.find_unique(where={"id": shop_id})
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada."
        )

    try:
        new_service = await db.services.create(
            data={
                "id": str(uuid.uuid4()),
                "barbershop_id": shop_id,
                "name": body.name,
                "description": body.description,
                "price": body.price,
                "duration_minutes": body.duration_minutes,
                "is_active": True
            }
        )
        return new_service
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el servicio: {str(e)}"
        )

@router.get("/barbershops/{shop_id}/services/{service_id}", response_model=ServiceResponse)
async def get_service(shop_id: str, service_id: str):
    """
    Obtiene los detalles de un servicio específico dentro de una barbería.
    """
    service = await db.services.find_first(
        where={
            "id": service_id,
            "barbershop_id": shop_id
        }
    )
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado en esta barbería."
        )
    return service

@router.put("/barbershops/{shop_id}/services/{service_id}", response_model=ServiceResponse)
async def update_service(shop_id: str, service_id: str, body: ServiceUpdate):
    """
    Actualiza la información de un servicio.
    """
    service = await db.services.find_first(
        where={
            "id": service_id,
            "barbershop_id": shop_id
        }
    )
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado en esta barbería."
        )

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        return service

    try:
        updated_service = await db.services.update(
            where={"id": service_id},
            data=update_data
        )
        return updated_service
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el servicio: {str(e)}"
        )

@router.delete("/barbershops/{shop_id}/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(shop_id: str, service_id: str):
    """
    Elimina un servicio de una barbería.
    """
    service = await db.services.find_first(
        where={
            "id": service_id,
            "barbershop_id": shop_id
        }
    )
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Servicio no encontrado en esta barbería."
        )

    try:
        await db.services.delete(where={"id": service_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el servicio: {str(e)}"
        )
