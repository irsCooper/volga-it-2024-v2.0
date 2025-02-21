import asyncio
from aio_pika.abc import AbstractIncomingMessage, AbstractChannel, AbstractQueue
from aio_pika import Message

from fastapi.exceptions import HTTPException
from fastapi import status

from typing import Any, Callable

from src.rabbit_mq.base import RabbitMqBase


class RabbitMqClient(RabbitMqBase):
    async def publish_message(
        self, 
        channel: AbstractChannel,
        body: bytes,
        routing_key: str,
        correlation_id: str | None,
        reply_to: str | None
    ):
        await channel.default_exchange.publish(
            Message(
                body=body,
                correlation_id=correlation_id,
                reply_to=reply_to
            ),
            routing_key=routing_key
        )


    async def call(self, body: str, routing_key: str):
        await self.connect()
        async with self.connection:
            channel = await self.connection.channel()

            await self.publish_message(
                channel=channel,
                body=body.encode(),
                routing_key=routing_key
            )
        await self.close()


    async def wait_for_response(
        self,
        callback_queue: AbstractQueue,
        correlation_id: str,
        timeout: float = 5.0
    ):
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        async def on_responce(msg: AbstractIncomingMessage):
            async with msg.process():
                if msg.correlation_id == correlation_id:
                    future.set_result(msg.body)
        
        await callback_queue.consume(on_responce)

        try:
            response = await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"RabbitMQ": "No received with the timeout period"}
            )
        
        return response
    

    async def call_and_wait_for_response(
        self,
        body: str,
        routing_key: str,
        channel: AbstractChannel,
        callback_queue: AbstractQueue,
        correlation_id: str,
        timeout: float = 5.0
    ):
        await self.connect()
        async with self.connection:
            await self.publish_message(
                channel=channel,
                body=body.encode(),
                routing_key=routing_key,
                correlation_id=correlation_id,
                reply_to=callback_queue.name
            )

            response = await self.wait_for_response(
                callback_queue, correlation_id, timeout
            )

        await self.close()
        return True if response == b'\x01' else response.decode()
    
    
    async def create_queue(self, channel: AbstractChannel):
        callback_queue = await channel.declare_queue(auto_delete=True)
        return callback_queue

rabbit_mq_client = RabbitMqClient()