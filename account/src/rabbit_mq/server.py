import asyncio
from functools import partial
import uuid
from aio_pika.abc import AbstractIncomingMessage
from aio_pika import RobustChannel, Message, connect_robust
from fastapi import HTTPException

from src.accounts.service import UserService
from src.authentication.router import validate_token
from src.core.db_helper import db
from src.doctors.service import DoctorSrvice
from src.core.config import settings
from src.accounts.schemas import ROLE_USER
from src.dependencies import delete_timetable_doctor, get_current_role

async def check_doctor(
    message: AbstractIncomingMessage,
    channel: RobustChannel
):
    async with message.process():
        doctor_id = message.body.decode()
        try:
            async with db.session_dependency() as session:
                await DoctorSrvice.get_doctor(
                    uuid.UUID(doctor_id),
                    session
                )
                response = b'\x01'
        except HTTPException:
            response = b'\x00'
        
        if message.reply_to:
            await channel.default_exchange.publish(
                Message(
                    body=response,
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )


async def check_pacient(
    message: AbstractIncomingMessage, 
    channel: RobustChannel
):
    async with message.process():
        user_id = message.body.decode()
        try:
            async with db.session_dependency() as session:
                user = await UserService.get_user(uuid.UUID(user_id), session)
                # response = b'\x00' if ROLE_USER not in [role.name_role for role in user.roles] else b'\x01'
                await get_current_role(ROLE_USER, user)
                response = b'\x01'
        except HTTPException:
            response = b'\x00'

        if message.reply_to:
            await channel.default_exchange.publish(
                Message(
                    body=response,
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )


async def check_token(
    message: AbstractIncomingMessage, 
    channel: RobustChannel
):
    async with message.process():
        token = message.body.decode()
        try:
            await validate_token(token)
            response = b'\x01'
        except HTTPException as e:
            response = str(e.detail).encode()

        if message.reply_to:
            await channel.default_exchange.publish(
                Message(
                    body=response,
                    correlation_id=message.correlation_id
                ),
                routing_key=message.reply_to
            )


async def consume_rabbitmq():
    # while True:
        try:
            connection = await connect_robust(settings.rabbit_mq_url)
            channel = await connection.channel()

            doctor_queue = await channel.declare_queue(
                'check_doctor', auto_delete=True
            )

            await doctor_queue.consume(partial(check_doctor, channel=channel))

            token_queue = await channel.declare_queue(
                'check_token', auto_delete=True
            )

            await token_queue.consume(partial(check_token, channel=channel))

            user_queue = await channel.declare_queue(
                'check_pacient', auto_delete=True
            )

            await user_queue.consume(partial(check_pacient, channel=channel))

            print('Успешное подключение к RabbitMQ')
            # break
        except Exception as e:
            print(f'Ошибка подключения к RabbitMQ: {e}. Переподключение через 5 секунд...')
            await asyncio.sleep(5)