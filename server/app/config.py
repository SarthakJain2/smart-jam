from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- JWT settings ---
    JWT_SECRET: str
    JWT_REFRESH_SECRET: str
    JWT_RESET_SECRET: str

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/smart_jam"

    # --- Optional extras (ignored if not present) ---
    JWT_ALG: str = "HS256"
    JWT_EXPIRES_MIN: int = 30
    EMBEDDINGS_PROVIDER: str = "local"

    # --- Config ---
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
