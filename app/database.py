import logging
from prisma import Prisma
from app.config import settings

logger = logging.getLogger("uvicorn")

# Initialize Prisma Client with programmatic database URL injection
db = Prisma(
    datasource={
        "url": settings.DATABASE_URL
    },
    auto_register=True
)

async def connect_db():
    if not db.is_connected():
        logger.info("Connecting to Supabase PostgreSQL database via Prisma...")
        await db.connect()
        logger.info("Successfully connected to database.")

async def disconnect_db():
    if db.is_connected():
        logger.info("Disconnecting from Supabase PostgreSQL database...")
        await db.disconnect()
        logger.info("Disconnected from database.")
