import asyncio
from functools import partial
import uuid
from aio_pika.abc import AbstractIncomingMessage
from aio_pika import RobustChannel, Message, connect_robust
from fastapi import HTTPException

from src.core.db_helper import db
from src.core.config import settings
from src.hospitals.dao import HospitalDAO, HospitalModel
from src.rabbit_mq.client import rabbit_mq_client

import json 

async def check_hospital_room(
    message: AbstractIncomingMessage, 
    channel: RobustChannel
):
    async with message.process():
        body: dict = json.loads(message.body.decode())
        hospital_id = body.get('hospital_id')
        query_room = body.get('room')
        async with db.session() as session:
            try:
                rooms = await HospitalDAO.get_rooms(session, HospitalModel.id == hospital_id)
                room = next((room.name for room in rooms if room.name == query_room), None)
                if room:
                    response = b'\x01'
                else:
                    response = 'Room not found.'.encode()
            except HTTPException:
                response = 'Hospital not found.'.encode()
        if message.reply_to:
            await rabbit_mq_client.publish_message(
                channel=channel,
                body=response,
                correlation_id=message.correlation_id,
                routing_key=message.reply_to
            )
            # await channel.default_exchange.publish(
            #     aio_pika.Message(
            #         body=response,
            #         correlation_id=message.correlation_id
            #     ),
            #     routing_key=message.reply_to
            # )


async def check_hospital(
    message: AbstractIncomingMessage, 
    channel: RobustChannel
):
    async with message.process():
        print(f"hospital 1")
        hospital_id = message.body.decode()
        try:
            async with db.session_factory as session:
                print(f"hospital 2")
                room = await HospitalDAO.find_one_or_none(session, HospitalModel.id == hospital_id)
                if room:
                    response = b'\x01'
                else:
                    response = b'\x00'
            
            print(f"hospital 3")
            if message.reply_to:
                await rabbit_mq_client.publish_message(
                    channel=channel,
                    body=response,
                    correlation_id=message.correlation_id,
                    routing_key=message.reply_to
                )
        except Exception as e:
            print(e)
            # await channel.default_exchange.publish(
            #     aio_pika.Message(
            #         body=response,
            #         correlation_id=message.correlation_id
            #     ),
            #     routing_key=message.reply_to
            # )


async def consume_rabbitmq():
    while True:
        try:
            # connection = await aio_pika.connect_robust(f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}/')
            # channel = await connection.channel()
            await rabbit_mq_client.connect()
            channel: RobustChannel = await rabbit_mq_client.create_channel()

            hospital_room_queue = await channel.declare_queue(
                'check_hospital_room', auto_delete=True
            )

            await hospital_room_queue.consume(partial(check_hospital_room, channel=channel))

            hospital_queue = await channel.declare_queue(
                'check_hospital', auto_delete=True
            )

            await hospital_queue.consume(partial(check_hospital, channel=channel))
            print('Успешное подключение к RabbitMQ')
            break

        except Exception as e:
            print(f'Ошибка подключения к RabbitMQ: {e}. Переподключение через 5 секунд...')
            await asyncio.sleep(5)