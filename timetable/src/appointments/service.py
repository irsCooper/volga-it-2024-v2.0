import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.appointments.dao import AppointmentDAO, AppointmentModel

class AppointmentsService:
    @classmethod
    async def delete_appoointment(
        cls,
        appointment_id: uuid.UUID,
        session: AsyncSession
    ):
        await AppointmentDAO.delete(
            session,
            AppointmentModel.id == appointment_id
        )