from typing import Optional

from sqlalchemy import select
from src.base_dao import BaseDAO
from src.appointments.schemas import AppointmentCreate, AppointmentUpdate
from src.appointments.model import AppointmentModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

class AppointmentDAO(BaseDAO[AppointmentModel, AppointmentCreate, AppointmentUpdate]):
    model = AppointmentModel

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        *where,
        obj_in: AppointmentUpdate,
    ):
        raise Exception('This method no allowed')
    

    @classmethod
    async def find_one_or_none(
        cls,
        session: AsyncSession,
        *filters,
        **filter_by
    ) -> Optional[AppointmentModel]:
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.timetable)
            )
            .filter(*filters)
            .filter_by(**filter_by)
        )

        result = await session.execute(stmt)
        return result.scalars().one_or_none()