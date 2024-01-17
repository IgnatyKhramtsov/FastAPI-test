import json

from fastapi import APIRouter
from schemas import Message
from config import loop, settings
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer



route = APIRouter(
    prefix="/message",
    tags=["Operation"]
)


@route.post("/create_message")
async def send(message: Message):
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        print(f"Посылаем сообщение со значением: {message}")
        value_json = json.dumps(message.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=settings.KAFKA_TOPIC, value=value_json)
    finally:
        await producer.stop()


async def consume():
    consumer = AIOKafkaConsumer(settings.KAFKA_TOPIC,
                                loop=loop,
                                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=settings.KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f"Consumer msg: {msg}")
    finally:
        await consumer.stop()



