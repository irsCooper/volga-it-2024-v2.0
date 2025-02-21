import uuid
import asyncio

from fastapi import HTTPException
from functools import partial
from aio_pika.abc import AbstractIncomingMessage
from aio_pika import RobustChannel, Message, connect_robust

from src.timetables.service import TimetableService
from src.core.db_helper import db
from src.core.config import settings


async def delete_timetable_doctor(
    message: AbstractIncomingMessage,
    channel: RobustChannel
):
    async with message.process():
        doctor_id = message.body.decode()
        # try:
        #     async with db.session_dependency() as sessin:
                # await 