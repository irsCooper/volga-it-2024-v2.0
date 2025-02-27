from datetime import datetime
import uuid

from sqlalchemy import TIMESTAMP, UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base_model import BaseModel


class HistoryModel(BaseModel):
    __tablename__ = "historys"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4())
    date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    pacient_id: Mapped[uuid.UUID] = mapped_column(UUID, index=True, nullable=False)
    hospital_id: Mapped[uuid.UUID] = mapped_column(UUID, index=True, nullable=False)
    doctor_id: Mapped[uuid.UUID] = mapped_column(UUID, index=True, nullable=False)
    room: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[str] = mapped_column(String, nullable=True)
