import uuid
import hashlib
from fastapi import APIRouter, HTTPException, status
from app.database import db
from app.models.schemas.auth_schema import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])

def hash_password(password: str) -> str:
    """Simple SHA-256 password hashing."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    """
    Registra un nuevo usuario en el sistema.
    Crea la cuenta en el esquema 'auth' y el perfil público en 'public'.
    """
    # 1. Check if user already exists in public schema
    existing_user = await db.public_users.find_unique(where={"email": body.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    user_uuid = str(uuid.uuid4())
    hashed_pass = hash_password(body.password)

    try:
        # 2. Create user in auth.users schema
        await db.auth_users.create(
            data={
                "id": user_uuid,
                "email": body.email,
                "encrypted_password": hashed_pass,
                "aud": "authenticated",
                "role": "authenticated"
            }
        )

        # 3. Create user in public.users schema (linked via foreign key)
        new_profile = await db.public_users.create(
            data={
                "id": user_uuid,
                "full_name": body.name,
                "email": body.email
            }
        )

        return {
            "message": "Usuario registrado exitosamente",
            "user": {
                "id": new_profile.id,
                "name": new_profile.full_name,
                "email": new_profile.email
            }
        }
    except Exception as e:
        # If anything fails, return the error details
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el registro: {str(e)}"
        )

@router.post("/login")
async def login(body: LoginRequest):
    """
    Inicia sesión de un usuario y devuelve un token de autenticación.
    """
    # Find user in auth schema
    auth_user = await db.auth_users.find_first(where={"email": body.email})
    if not auth_user or auth_user.encrypted_password != hash_password(body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas."
        )

    # Get public profile
    public_profile = await db.public_users.find_unique(where={"id": auth_user.id})

    # Return a mock token for development (can be replaced with a JWT)
    mock_token = f"eyJhbGciOiJIUzI1NiJ9.mock_token_for_user_{auth_user.id}"

    return {
        "message": "Sesión iniciada correctamente",
        "token": mock_token,
        "user": {
            "id": public_profile.id if public_profile else auth_user.id,
            "name": public_profile.full_name if public_profile else "",
            "email": auth_user.email
        }
    }
