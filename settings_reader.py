from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    app_name: str = 'Inquisitor'
    token: SecretStr
    superuser_id: int
    admins: set
    db: str
    ping_period: int = 60
    ping_flag: bool = False

    class Config:
        env_file = "../.env"


config = Settings()
