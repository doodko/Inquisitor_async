from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    app_name: str = 'Inquisitor'
    token: SecretStr
    superuser_id: int
    admins: set

    class Config:
        env_file = ".env"


config = Settings()
