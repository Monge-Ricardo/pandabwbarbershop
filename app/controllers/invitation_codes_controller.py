import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.database import db
from app.models.schemas.invitation_code_schema import InvitationCodeCreate, InvitationCodeUpdate, InvitationCodeResponse

router = APIRouter(prefix="/invitation-codes", tags=["Invitation Codes CRUD"])

@router.get("", response_model=List[InvitationCodeResponse])
async def list_invitation_codes(barbershop_id: Optional[str] = None, code: Optional[str] = None):
    """
    Lista todos los códigos de invitación del sistema, filtrando opcionalmente por barbershop_id y/o código.
    """
    where_filter = {}
    if barbershop_id:
        where_filter["barbershop_id"] = barbershop_id
    if code:
        where_filter["code"] = code

    codes = await db.invitation_codes.find_many(where=where_filter)
    return codes

@router.get("/{code_id}", response_model=InvitationCodeResponse)
async def get_invitation_code(code_id: str):
    """
    Obtiene los detalles de un código de invitación por su ID.
    """
    code = await db.invitation_codes.find_unique(where={"id": code_id})
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código de invitación no encontrado."
        )
    return code

@router.post("", response_model=InvitationCodeResponse, status_code=status.HTTP_201_CREATED)
async def create_invitation_code(body: InvitationCodeCreate):
    """
    Crea un nuevo código de invitación en la base de datos.
    """
    # Check if duplicate code exists
    existing = await db.invitation_codes.find_unique(where={"code": body.code})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código de invitación ya existe."
        )

    try:
        new_code = await db.invitation_codes.create(
            data={
                "id": str(uuid.uuid4()),
                "barbershop_id": body.barbershop_id,
                "code": body.code,
                "expires_at": body.expires_at,
                "is_active": body.is_active
            }
        )
        return new_code
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el código de invitación en BD: {str(e)}"
        )

@router.put("/{code_id}", response_model=InvitationCodeResponse)
async def update_invitation_code(code_id: str, body: InvitationCodeUpdate):
    """
    Actualiza la fecha de expiración o estado activo de un código de invitación en la BD.
    """
    code = await db.invitation_codes.find_unique(where={"id": code_id})
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código de invitación no encontrado."
        )

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        return code

    try:
        updated = await db.invitation_codes.update(
            where={"id": code_id},
            data=update_data
        )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el código de invitación en BD: {str(e)}"
        )

@router.delete("/{code_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invitation_code(code_id: str):
    """
    Elimina un código de invitación de la base de datos.
    """
    code = await db.invitation_codes.find_unique(where={"id": code_id})
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código de invitación no encontrado."
        )

    try:
        await db.invitation_codes.delete(where={"id": code_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el código de invitación de la BD: {str(e)}"
        )
