from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    TOKEN: str
    NGROK_URL: str = "https://ee88322b1e0d.ngrok-free.app"
    WEBHOOK_PATH: str = "/webhook"
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    DB_URL: str
    ECHO: bool = False
    ADMIN: int
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", extra="ignore")


settings = Settings()
