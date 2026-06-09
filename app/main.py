from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_db, disconnect_db, db
from app.controllers import (
    auth_users_controller,
    user_controller,
    barbershop_controller,
    barbershop_members_controller,
    service_controller,
    product_controller,
    appointment_controller,
    appointment_services_controller,
    availability_controller,
    invitation_codes_controller,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    await connect_db()
    yield
    # Shutdown: Disconnect from the database
    await disconnect_db()

app = FastAPI(
    title="SharkHub CRUD Database API",
    description="API RESTful de acceso directo a datos para la gestión de SharkHub Barbershop.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for decentralized frontend/microservice consumption
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register CRUD routers directly to the root path
app.include_router(auth_users_controller.router)
app.include_router(user_controller.router)
app.include_router(barbershop_controller.router)
app.include_router(barbershop_members_controller.router)
app.include_router(service_controller.router)
app.include_router(product_controller.router)
app.include_router(appointment_controller.router)
app.include_router(appointment_services_controller.router)
app.include_router(availability_controller.router)
app.include_router(invitation_codes_controller.router)

@app.get("/health", tags=["System"])
async def health_check():
    """
    Verifica el estado del servidor API y su conectividad con la base de datos Supabase.
    """
    db_status = "disconnected"
    if db.is_connected():
        try:
            # Query verification via raw SQL execution
            await db.execute_raw("SELECT 1;")
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
