from datetime import datetime
import uuid

from sqlalchemy import TIMESTAMP, UUID, String
from src.base_model import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship


class TimetableModel(BaseModel):
    __tablename__ = 'timetables'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    hospital_id: Mapped[uuid.UUID] = mapped_column(UUID, index=True, nullable=False)
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID, index=True, nullable=False)
    from_column: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    to: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    room: Mapped[str] = mapped_column(String, nullable=False)

    appointments = relationship(
        "AppointmentModel",
        back_populates="timetable",
        cascade="all, delete-orphan",
        passive_deletes=True
    )