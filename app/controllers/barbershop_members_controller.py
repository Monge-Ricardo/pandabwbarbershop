import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.database import db
from app.models.schemas.barbershop_member_schema import BarbershopMemberCreate, BarbershopMemberUpdate, BarbershopMemberResponse

router = APIRouter(prefix="/barbershop-members", tags=["Barbershop Members CRUD"])

@router.get("", response_model=List[BarbershopMemberResponse])
async def list_members(barbershop_id: Optional[str] = None, user_id: Optional[str] = None):
    """
    Lista todos los miembros de barberías.
    Permite filtrar por barbershop_id y/o user_id.
    """
    where_filter = {}
    if barbershop_id:
        where_filter["barbershop_id"] = barbershop_id
    if user_id:
        where_filter["user_id"] = user_id
        
    members = await db.barbershop_members.find_many(where=where_filter)
    return members

@router.get("/{member_id}", response_model=BarbershopMemberResponse)
async def get_member(member_id: str):
    """
    Obtiene los detalles de un miembro por su ID.
    """
    member = await db.barbershop_members.find_unique(where={"id": member_id})
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Miembro de barbería no encontrado."
        )
    return member

@router.post("", response_model=BarbershopMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(body: BarbershopMemberCreate):
    """
    Añade un nuevo miembro a una barbería en la base de datos.
    """
    # Check if unique constraint is violated
    existing = await db.barbershop_members.find_first(
        where={
            "barbershop_id": body.barbershop_id,
            "user_id": body.user_id
        }
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya es miembro de esta barbería."
        )

    try:
        new_member = await db.barbershop_members.create(
            data={
                "id": str(uuid.uuid4()),
                "barbershop_id": body.barbershop_id,
                "user_id": body.user_id,
                "role": body.role,
                "status": body.status
            }
        )
        return new_member
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al añadir miembro a la barbería en BD: {str(e)}"
        )

@router.put("/{member_id}", response_model=BarbershopMemberResponse)
async def update_member(member_id: str, body: BarbershopMemberUpdate):
    """
    Actualiza el rol o estado de un miembro de barbería.
    """
    member = await db.barbershop_members.find_unique(where={"id": member_id})
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Miembro de barbería no encontrado."
        )

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        return member

    try:
        updated = await db.barbershop_members.update(
            where={"id": member_id},
            data=update_data
        )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el miembro en BD: {str(e)}"
        )

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(member_id: str):
    """
    Elimina a un miembro de una barbería.
    """
    member = await db.barbershop_members.find_unique(where={"id": member_id})
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Miembro de barbería no encontrado."
        )

    try:
        await db.barbershop_members.delete(where={"id": member_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el miembro de la BD: {str(e)}"
        )
