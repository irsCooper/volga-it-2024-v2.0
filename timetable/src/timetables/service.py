from datetime import datetime
from typing import Optional
import uuid
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.timetables.schemas import TimetableCreate, TimetableUpdate
from src.timetables.model import TimetableModel
from src.timetables.dao import TimetableDAO
from src.exception.TimetableException import TimetableNotFound

class TimetableService:
    @classmethod
    async def create_timetable(
        cls,
        data: TimetableCreate,
        session: AsyncSession
    ) -> Optional[TimetableModel]:
        return await TimetableDAO.add(
            session=session,
            obj_in=TimetableCreate(**data.model_dump())
        )
    

    @classmethod
    async def update_timetable(
        cls,
        timetable_id: uuid.UUID,
        data: TimetableUpdate,
        session: AsyncSession
    ) -> Optional[TimetableModel]:
        timetable = await TimetableDAO.update(
            session,
            TimetableModel.id == timetable_id,
            obj_in=data
        )

        if not timetable:
            raise TimetableNotFound
        
        return timetable
    

    @classmethod
    async def delete_timetable(
        cls,
        timetable_id: uuid.UUID,
        session: AsyncSession
    ):
        await TimetableDAO.delete(
            session,
            TimetableModel.id == timetable_id,
        )


    @classmethod
    async def delete_timetables_for_doctor_id(
        cls,
        doctor_id: uuid.UUID,
        session: AsyncSession
    ):
        await TimetableDAO.delete(
            session,
            TimetableModel.doctor_id == doctor_id
        )

    
    @classmethod
    async def delete_timetables_for_hospital_id(
        cls,
        hospital_id: uuid.UUID,
        session: AsyncSession
    ):
        await TimetableDAO.delete(
            session,
            TimetableModel.hospital_id == hospital_id
        )

    @classmethod
    async def get_timetables_for_doctor_id(
        cls,
        doctor_id: uuid.UUID,
        session: AsyncSession,
        from_column: datetime,
        to: datetime
    ) -> Optional[list[TimetableModel]]:
        if from_column >= to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The "to" field should be larger than the "from" field'
            )
        return await TimetableDAO.find_all(
            session,
            and_(
                TimetableModel.doctor_id == doctor_id,
                TimetableModel.from_column < to,
                TimetableModel.to > from_column
            ),
        )
    

    @classmethod
    async def get_timetables_for_hospital_id(
        cls,
        hospital_id: uuid.UUID,
        session: AsyncSession,
        from_column: datetime,
        to: datetime
    ) -> Optional[list[TimetableModel]]:
        if from_column >= to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The "to" field should be larger than the "from" field'
            )
        return await TimetableDAO.find_all(
            session,
            and_(
                TimetableModel.hospital_id == hospital_id,
                TimetableModel.from_column < to,
                TimetableModel.to > from_column
            ),
        )
    

    @classmethod
    async def get_timetables_for_hospital_room(
        cls,
        hospital_id: uuid.UUID,
        room: str,
        session: AsyncSession,
        from_column: datetime,
        to: datetime
    ) -> Optional[list[TimetableModel]]:
        if from_column >= to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The "to" field should be larger than the "from" field'
            )
        return await TimetableDAO.find_all(
            session,
            and_(
                TimetableModel.hospital_id == hospital_id,
                TimetableModel.room == room,
                TimetableModel.from_column < to,
                TimetableModel.to > from_column
            ),
        )