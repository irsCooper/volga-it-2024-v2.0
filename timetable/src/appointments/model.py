import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base_model import BaseModel



class AppointmentModel(BaseModel):
    __tablename__ = 'appointments'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    timetable_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('timetables.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    timetable = relationship(
        "TimetableModel",
        back_populates="appointments",
    )