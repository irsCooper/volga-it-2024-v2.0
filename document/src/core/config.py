import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


ROLE_ADMIN = 'Admin'
ROLE_USER = 'User'
ROLE_DOCTOR = 'Doctr'
ROLE_MANAGER = 'Manager'


BASE_DIR = Path(__file__).parent.parent.parent


load_dotenv()


class AuthJWT(BaseModel):
    public_key_path: Path = BASE_DIR / "certificates" / "jwt-publick.pem"
    algorithms: str = "RS256"


class Settings(BaseSettings):
    echo: bool = True
    db_url: str = os.environ.get('DB_URL')
    rabbit_mq_url: str = os.environ.get('RMQ_URL')
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()
