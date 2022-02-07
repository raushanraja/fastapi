from pydantic import BaseSettings
from typing import Set


class Settings(BaseSettings):
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SCHEMA: str = "postgresql"
    POSTUSER: str = "raushan"
    POSTPASSWORD: str = "meraushan"
    POSTHOST: str = "localhost"
    POSTPATH: str = ""
    POSTPORT: str = "5432"


settings = Settings()

print(settings)
