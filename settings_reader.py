from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Inquisitor'
    token: SecretStr
    superuser_id: int
    admins: set

    class Config:
        env_file = ".env"


config = Settings()
