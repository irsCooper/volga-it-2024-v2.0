from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractQueue
from aio_pika import connect_robust, Message

from src.core.config import settings

ROUTING_KEY_DELETE_TIMETABLE_DOCTOR = 'delete-timetable-doctor'
ROUTING_KEY_CHECK_TOKEN = 'check_token'

class RabbitMqBase:
    def __init__(self, rabbit_url=settings.rabbit_mq_url):
        self.rabbit_url = rabbit_url
        self.connection: AbstractConnection = None 
        self._channel: AbstractChannel | None = None


    async def connect(self) -> AbstractConnection:
        try:
            if self.connection is None or self.connection.is_closed:
                self.connection = await connect_robust(self.rabbit_url)
            return self.connection
        except Exception as e:
            print(f"Error connect to RabbitMQ: {e}")
            self.connection = None


    async def create_channel(self):
        channel = await self.connection.channel()
        return channel

    
    async def close(self) -> None:
        if self.connection is not None and not self.connection.is_closed:
            await self.connection.close()
