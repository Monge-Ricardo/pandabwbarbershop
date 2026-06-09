from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.database import db
from app.models.schemas.auth_user_schema import AuthUserCreate, AuthUserUpdate, AuthUserResponse

router = APIRouter(prefix="/auth-users", tags=["Auth Users CRUD"])

@router.get("", response_model=List[AuthUserResponse])
async def list_auth_users(email: Optional[str] = None):
    """
    Lista todos los registros de usuarios en la tabla auth.users.
    Opcionalmente filtra por email.
    """
    if email:
        users = await db.auth_users.find_many(where={"email": email})
    else:
        users = await db.auth_users.find_many()
    return users

@router.get("/{user_id}", response_model=AuthUserResponse)
async def get_auth_user(user_id: str):
    """
    Obtiene un registro de auth.users por su ID.
    """
    user = await db.auth_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario de autenticación no encontrado."
        )
    return user

@router.get("/email/{email}", response_model=AuthUserResponse)
async def get_auth_user_by_email(email: str):
    """
    Obtiene un registro de auth.users por su correo electrónico.
    """
    user = await db.auth_users.find_first(where={"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario de autenticación no encontrado para el correo provisto."
        )
    return user

@router.post("", response_model=AuthUserResponse, status_code=status.HTTP_201_CREATED)
async def create_auth_user(body: AuthUserCreate):
    """
    Crea un nuevo registro en auth.users.
    """
    existing = await db.auth_users.find_first(where={"email": body.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado en auth_users."
        )
    
    try:
        new_user = await db.auth_users.create(
            data={
                "id": body.id,
                "email": body.email,
                "encrypted_password": body.encrypted_password,
                "aud": body.aud,
                "role": body.role
            }
        )
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el registro auth_user: {str(e)}"
        )

@router.put("/{user_id}", response_model=AuthUserResponse)
async def update_auth_user(user_id: str, body: AuthUserUpdate):
    """
    Actualiza campos específicos de un registro en auth.users.
    """
    user = await db.auth_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario de autenticación no encontrado."
        )
    
    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        return user
        
    try:
        updated = await db.auth_users.update(
            where={"id": user_id},
            data=update_data
        )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar auth_user: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_auth_user(user_id: str):
    """
    Elimina un registro de auth.users.
    """
    user = await db.auth_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario de autenticación no encontrado."
        )
        
    try:
        await db.auth_users.delete(where={"id": user_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar auth_user: {str(e)}"
        )
