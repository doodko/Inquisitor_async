from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Inquisitor"
    token: SecretStr
    superuser_id: int
    admins: set
    api_url: str
    rules_url: str
    jar_url: str

    class Config:
        env_file = ".env"


config = Settings()
