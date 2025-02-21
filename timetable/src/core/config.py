import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

ROLE_ADMIN = 'Admin'
ROLE_USER = 'User'
ROLE_DOCTOR = 'Doctr'
ROLE_MANAGER = 'Manager'

class Settings(BaseSettings):
    echo: bool = True
    db_url: str = os.environ.get('DB_URL')

settings = Settings()
