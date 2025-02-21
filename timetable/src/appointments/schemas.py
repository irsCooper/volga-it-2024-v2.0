import uuid
from datetime import datetime

from pydantic import BaseModel

class AppointmentCreate(BaseModel): 
    timetable_id: uuid.UUID
    user_id: uuid.UUID
    time: datetime


class AppointmentUpdate(BaseModel):
    pass