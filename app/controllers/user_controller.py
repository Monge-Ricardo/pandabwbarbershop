import uuid
from fastapi import APIRouter, HTTPException, status, Header
from typing import List, Optional
from app.database import db
from app.models.schemas.user_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
async def list_users():
    """
    Obtiene la lista de todos los usuarios registrados en la base de datos pública.
    """
    users = await db.public_users.find_many()
    return users

@router.get("/me", response_model=UserResponse)
async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Obtiene el perfil del usuario actualmente autenticado (basado en el Token recibido).
    """
    if not authorization or not authorization.startswith("Bearer "):
        # For academic purposes, if no authorization header is sent, return the first user
        first_user = await db.public_users.find_first()
        if not first_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autorizado. Inicie sesión primero."
            )
        return first_user
    
    # Extract mock user id from the token
    # Format: Bearer eyJhbGciOiJIUzI1NiJ9.mock_token_for_user_{user_id}
    token = authorization.split(" ")[1]
    try:
        parts = token.split("_user_")
        if len(parts) < 2:
            raise ValueError()
        user_id = parts[1]
        
        user = await db.public_users.find_unique(where={"id": user_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o malformado."
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """
    Obtiene los detalles de un usuario específico.
    """
    user = await db.public_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    return user

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreate):
    """
    Crea manualmente un usuario y su cuenta de autenticación correspondiente.
    """
    # Check if email is already registered
    existing_user = await db.public_users.find_unique(where={"email": body.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    user_uuid = str(uuid.uuid4())
    
    try:
        # Create auth record first
        await db.auth_users.create(
            data={
                "id": user_uuid,
                "email": body.email,
                "encrypted_password": "hashed_default_password", # Default placeholder password
                "aud": "authenticated",
                "role": "authenticated"
            }
        )

        # Create public profile
        new_user = await db.public_users.create(
            data={
                "id": user_uuid,
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
            detail=f"Error al crear el usuario: {str(e)}"
        )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, body: UserUpdate):
    """
    Actualiza la información de perfil de un usuario existente.
    """
    user = await db.public_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    # Filter out None values to perform partial updates
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
            detail=f"Error al actualizar el usuario: {str(e)}"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Elimina a un usuario del sistema (tanto el perfil como su cuenta de autenticación).
    """
    user = await db.public_users.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    try:
        # Deleting from public_users will automatically trigger cascading delete if defined,
        # but to be safe, we delete both.
        await db.public_users.delete(where={"id": user_id})
        await db.auth_users.delete(where={"id": user_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el usuario: {str(e)}"
        )
