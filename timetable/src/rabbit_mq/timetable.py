import uuid

from src.rabbit_mq.base import ROUTING_KEY_CHECK_DOCTOR, ROUTING_KEY_CHECK_HOSPITAL
from src.rabbit_mq.client import RabbitMqClient, rabbit_mq_client




class TimetableRabbitClient(RabbitMqClient):
    @classmethod
    async def check_hospital(cls, hospital_id: uuid.UUID):
        return await rabbit_mq_client.send_message("hospital_check_queue", "hospital_response_queue", str(hospital_id))
        # print(f'in TimetableRabbitClient check_hospital')
        # connect = await rabbit_mq_client.connect()
        # channel = await connect.channel()

        # queue = await channel.declare_queue('client_check_queue', durable=True)

        # message = Message(body=str(hospital_id).encode(), delivery_mode=DeliveryMode.PERSISTENT)
        # await channel.default_exchange.publish(message, routing_key=ROUTING_KEY_CHECK_HOSPITAL)

        # print(f"Sent request for {hospital_id} to {ROUTING_KEY_CHECK_HOSPITAL}")

        # response = await wait_for_response(response_queue)
        # return CheckResponse(exists=response)

        # .call_and_wait_for_response(
        #     body=str(hospital_id),
        #     correlation_id=str(uuid.uuid4()),
        #     routing_key=ROUTING_KEY_CHECK_HOSPITAL,
        # )


    @classmethod
    async def check_hospital_room(cls):
        pass


    @classmethod
    async def check_doctor(cls):
        pass