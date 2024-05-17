from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Inquisitor"
    token: SecretStr
    app_env: str = "development"
    superuser_id: int
    admins: set
    api_url: str
    rules_url: str
    jar_url: str
    sentry_dns: str

    class Config:
        env_file = ".env"


config = Settings()
