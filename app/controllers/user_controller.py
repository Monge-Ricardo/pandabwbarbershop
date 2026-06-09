from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.database import db
from app.models.schemas.user_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users CRUD"])

@router.get("", response_model=List[UserResponse])
async def list_users(email: Optional[str] = None):
    """
    Lista todos los perfiles de usuario públicos en el sistema.
    Opcionalmente filtra por correo electrónico.
    """
    if email:
        users = await db.public_users.find_many(where={"email": email})
    else:
        users = await db.public_users.find_many()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """
    Obtiene los detalles de un perfil público de usuario por su ID.
    """
    user = await db.public_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de usuario no encontrado."
        )
    return user

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreate):
    """
    Crea un nuevo perfil público de usuario.
    """
    existing_profile = await db.public_users.find_unique(where={"id": body.id})
    if existing_profile:
        # Si ya existe (p. ej. creado por un trigger de Supabase), actualizamos sus datos
        try:
            updated_profile = await db.public_users.update(
                where={"id": body.id},
                data={
                    "full_name": body.full_name,
                    "email": body.email,
                    "phone": body.phone,
                    "avatar_url": body.avatar_url
                }
            )
            return updated_profile
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar el perfil de usuario existente: {str(e)}"
            )

    try:
        new_user = await db.public_users.create(
            data={
                "id": body.id,
                "full_name": body.full_name,
                "email": body.email,
                "phone": body.phone,
                "avatar_url": body.avatar_url
            }
        )
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el perfil de usuario: {str(e)}"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, body: UserUpdate):
    """
    Actualiza un perfil público de usuario existente.
    """
    user = await db.public_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de usuario no encontrado."
        )

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        return user

    try:
        updated_user = await db.public_users.update(
            where={"id": user_id},
            data=update_data
        )
        return updated_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el perfil de usuario: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Elimina un perfil público de usuario.
    """
    user = await db.public_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de usuario no encontrado."
        )

    try:
        await db.public_users.delete(where={"id": user_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el perfil de usuario: {str(e)}"
        )
