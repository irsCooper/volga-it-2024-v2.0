from typing import Optional

from sqlalchemy import select
from src.base_dao import BaseDAO
from src.timetables.schemas import TimetableCreate, TimetableUpdate
from src.timetables.model import TimetableModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

class TimetableDAO(BaseDAO[TimetableModel, TimetableCreate, TimetableUpdate]):
    model = TimetableModel

    @classmethod
    async def find_all(
        cls, 
        session: AsyncSession, 
        *filters, 
        offset: int = 0, 
        limit: int = 100, 
        **filter_by
    ) -> Optional[list[TimetableModel]]:
        stmt = (
            select(cls.model)
            .options(
                selectinload(cls.model.appointments)
            )
            .filter(*filters)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )

        result = await session.execute(stmt)
        return result.scalars().all()
    

    @classmethod
    async def find_one_or_none(
        cls, 
        session: AsyncSession, 
        *filters, 
        **filter_by
    ) -> Optional[TimetableModel]:
        stmt = (
            select(cls.model)
            .filter(*filters)
            .filter_by(**filter_by)
            .options(
                selectinload(cls.model.appointments)
            )
        )

        result = await session.execute(stmt)
        return result.scalars().one_or_none()