import os
import pathlib
from dotenv import load_dotenv

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator

from typing import List, Optional, Union

load_dotenv()


ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    API_V1_STR: str = os.getenv("API_V1_STR")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM")


    #60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins

    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost.tiangolo.com", "https://localhost", "https://localhost:4200", "https://localhost.tiangolo.com", "http://localhost:8080", "http://localhost:8081"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv("BACKEND_CORS_ORIGINS")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("SQLALCHEMY_DATABASE_URI")
    FIRST_SUPERUSER: EmailStr = os.getenv("FIRST_SUPERUSER")
    
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")

    class Config:
        case_sensitive = True


settings = Settings()