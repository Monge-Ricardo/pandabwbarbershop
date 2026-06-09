import uuid
import random
import string
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.database import db
from app.models.schemas.barbershop_schema import BarbershopCreate, BarbershopUpdate, BarbershopResponse

router = APIRouter(prefix="/barbershops", tags=["Barbershops CRUD"])

def generate_invite_code() -> str:
    """Generates a random invite code like SH-123-XYZ."""
    chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"SH-{chars[:3]}-{chars[3:]}"

@router.get("", response_model=List[BarbershopResponse])
async def list_barbershops(slug: Optional[str] = None, invite_code: Optional[str] = None):
    """
    Lista todas las barberías, permitiendo filtrar opcionalmente por slug o invite_code.
    """
    if slug:
        shops = await db.barbershops.find_many(where={"slug": slug})
    elif invite_code:
        shops = await db.barbershops.find_many(where={"invite_code": invite_code})
    else:
        shops = await db.barbershops.find_many()
    return shops

@router.get("/{shop_id}", response_model=BarbershopResponse)
async def get_barbershop(shop_id: str):
    """
    Obtiene los detalles de una barbería por su ID.
    """
    shop = await db.barbershops.find_unique(where={"id": shop_id})
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada."
        )
    return shop

@router.get("/slug/{slug}", response_model=BarbershopResponse)
async def get_barbershop_by_slug(slug: str):
    """
    Obtiene los detalles de una barbería por su slug.
    """
    shop = await db.barbershops.find_unique(where={"slug": slug})
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada por slug."
        )
    return shop

@router.post("", response_model=BarbershopResponse, status_code=status.HTTP_201_CREATED)
async def create_barbershop(body: BarbershopCreate):
    """
    Registra una nueva barbería directamente en la base de datos.
    """
    existing_shop = await db.barbershops.find_unique(where={"slug": body.slug})
    if existing_shop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El slug de la barbería ya está en uso."
        )

    invite_code = generate_invite_code()
    
    try:
        new_shop = await db.barbershops.create(
            data={
                "id": str(uuid.uuid4()),
                "name": body.name,
                "slug": body.slug,
                "description": body.description,
                "logo_url": body.logo_url,
                "address": body.address,
                "phone": body.phone,
                "email": body.email,
                "invite_code": invite_code,
                "is_active": True
            }
        )
        return new_shop
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la barbería en BD: {str(e)}"
        )

@router.put("/{shop_id}", response_model=BarbershopResponse)
async def update_barbershop(shop_id: str, body: BarbershopUpdate):
    """
    Actualiza la información de una barbería existente.
    """
    shop = await db.barbershops.find_unique(where={"id": shop_id})
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada."
        )

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        return shop

    try:
        updated_shop = await db.barbershops.update(
            where={"id": shop_id},
            data=update_data
        )
        return updated_shop
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la barbería en BD: {str(e)}"
        )

@router.delete("/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_barbershop(shop_id: str):
    """
    Elimina una barbería de la base de datos.
    """
    shop = await db.barbershops.find_unique(where={"id": shop_id})
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada."
        )

    try:
        await db.barbershops.delete(where={"id": shop_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la barbería de la BD: {str(e)}"
        )
