from aio_pika.abc import AbstractIncomingMessage, AbstractChannel, AbstractQueue
from aio_pika import Message, DeliveryMode, IncomingMessage
import asyncio

from fastapi.exceptions import HTTPException
from fastapi import status

from typing import Any, Callable

from src.rabbit_mq.base import RabbitMqBase, ROUTING_KEY_CHECK_HOSPITAL


class RabbitMqClient(RabbitMqBase):
    # async def publish_message(
    #     self, 
    #     channel: AbstractChannel,
    #     body: bytes,
    #     routing_key: str,
    #     correlation_id: str | None,
    #     reply_to: str | None
    # ):
    #     await channel.default_exchange.publish(
    #         Message(
    #             body=body,
    #             correlation_id=correlation_id,
    #             reply_to=reply_to
    #         ),
    #         routing_key=routing_key
    #     )


    # async def call(self, body: str, routing_key: str):
    #     await self.connect()
    #     async with self.connection:
    #         channel = await self.connection.channel()

    #         await self.publish_message(
    #             channel=channel,
    #             body=body.encode(),
    #             routing_key=routing_key
    #         )
    #     await self.close()


    # async def wait_for_response(
    #     self,
    #     callback_queue: AbstractQueue,
    #     correlation_id: str,
    #     timeout: float = 5.0
    # ):
    #     loop = asyncio.get_running_loop()
    #     future = loop.create_future()

    #     async def on_responce(msg: AbstractIncomingMessage):
    #         async with msg.process():
    #             if msg.correlation_id == correlation_id:
    #                 future.set_result(msg.body)
        
    #     await callback_queue.consume(on_responce)

    #     try:
    #         response = await asyncio.wait_for(future, timeout=timeout)
    #     except asyncio.TimeoutError:
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail={"RabbitMQ": "No received with the timeout period"}
    #         )
        
    #     return response
    

    # async def call_and_wait_for_response(
    #     self,
    #     body: str,
    #     routing_key: str,
    #     # channel: AbstractChannel,
    #     # callback_queue: AbstractQueue,
    #     correlation_id: str,
    #     timeout: float = 5.0
    # ):
    #     await self.connect()

    #     async with self.connection:
    #         channel: AbstractChannel = await self.create_channel()
    #         callback_queue: AbstractQueue = await self.create_queue(channel, ROUTING_KEY_CHECK_HOSPITAL)

    #         # channel.basic_consume(
    #         #     queue=callback_queue,
    #         #     on_message_callback=on_response,
    #         #     auto_ack=True
    #         # )

    #         await self.publish_message(
    #             channel=channel,
    #             body=body.encode(),
    #             routing_key=routing_key,
    #             correlation_id=correlation_id,
    #             reply_to=callback_queue.name
    #         )

    #         response = await self.wait_for_response(
    #             callback_queue, correlation_id, timeout
    #         )

    #     await self.close()
    #     return True if response == b'\x01' else response.decode()
    
    
    # async def create_queue(self, channel: AbstractChannel, name: str):
    #     callback_queue = await channel.declare_queue(name, auto_delete=True)
    #     return callback_queue


    @classmethod
    async def wait_for_response(self, response_queue: str):
        connection = await self.connect()
        channel = await connection.channel()
        queue = await channel.declare_queue(response_queue, durable=True)

        future = asyncio.Future()

        async def on_message(message: IncomingMessage):
            async with message.process():
                future.set_result(message.body.decode() == "True")

        await queue.consume(on_message)
        return await future
    
    @classmethod
    async def send_message(self, queue_name: str, response_queue: str, item_id: str):
        connection = await self.connect()
        channel = await connection.channel()

        # Отправляем запрос в нужную очередь
        message = Message(body=item_id.encode(), delivery_mode=DeliveryMode.PERSISTENT)
        await channel.default_exchange.publish(message, routing_key=queue_name)

        print(f"Sent request for {item_id} to {queue_name}")

        # Ожидаем ответ из соответствующей очереди
        response = await self.wait_for_response(response_queue)
        return response
    

    @classmethod
    async def process_message(self, message: IncomingMessage, response_queue: str, check_type: str):
        async with message.process():
            item_id = message.body.decode()
            print(f"Received {check_type} check request for ID: {item_id}")

            # Проверка в базе данных (в примере просто заглушка)
            exists = item_id in ["123", "456"]  # Допустим, эти ID существуют

            # Отправляем ответ в нужную очередь
            connection = await self.connect()
            channel = await connection.channel()
            response = Message(body=str(exists).encode(), delivery_mode=DeliveryMode.PERSISTENT)
            await channel.default_exchange.publish(response, routing_key=response_queue)

            print(f"Sent {check_type} check response: {exists}")

    @classmethod
    async def start_consumer(self, queue_name: str, response_queue: str, check_type: str):
        connection = await self.connect()
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        await queue.consume(lambda message: self.process_message(message, response_queue, check_type))





rabbit_mq_client = RabbitMqClient()