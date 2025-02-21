import uuid
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_helper import db
from src.appointments.service import AppointmentsService

router = APIRouter(
    prefix='/Appointments',
    tags=['Appointment']
)

@router.get("/{id}")
async def delete_appointments(
    id: uuid.UUID,
    session: AsyncSession
):
    await AppointmentsService.delete_appoointment(
        appointment_id=id,
        session=session
    )