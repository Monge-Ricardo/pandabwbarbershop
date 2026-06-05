from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_db, disconnect_db, db
from app.controllers import (
    auth_controller,
    user_controller,
    barbershop_controller,
    service_controller,
    appointment_controller,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    await connect_db()
    yield
    # Shutdown: Disconnect from the database
    await disconnect_db()

app = FastAPI(
    title="SharkHub Barbershop Management API",
    description="API RESTful descentralizada para la gestión de SharkHub Barbershop.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for decentralized frontend consumption
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers directly to the root path (no /api prefix)
# This maps URLs like /users/{id} and /barbershops directly.
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(barbershop_controller.router)
app.include_router(service_controller.router)
app.include_router(appointment_controller.router)

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
