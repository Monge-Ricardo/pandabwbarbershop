from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load env variables into system environment for Prisma child processes
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    DIRECT_URL: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    PORT: int = 8000

    # Pydantic v2 configuration to read from .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
