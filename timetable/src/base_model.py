from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    __abstract__ = True 
    metadata = MetaData()