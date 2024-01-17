import asyncio
import json
import time
from datetime import datetime

import uvicorn
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import FastAPI
from sqlalchemy import select, insert

from config import loop, settings
from database import async_engine, sync_engine, async_session_factory
from models import metadata, parstext

app = FastAPI(docs_url='/')


def create_table():
    metadata.drop_all(sync_engine)
    metadata.create_all(sync_engine)


@app.on_event("startup")
async def startup_event():
    metadata.drop_all(sync_engine)
    metadata.create_all(sync_engine)


@app.post('/')
async def send_messages():
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    try:
        with open('O_Genri_Testovaya_20_vmeste (1).txt', encoding='utf-8') as file:
            for line in file:
                # print(f"Посылаем в топик сообщение: {line}")
                x_count = line.strip().count('х')
                val_json = json.dumps({"datetime": str(datetime.utcnow()), "title": "O_Genry", "count_x": x_count}).encode('utf-8')
                await producer.send("my_topic", value=val_json)
                await asyncio.sleep(3)
    finally:
        print('Завершение продюсера')
        await producer.stop()


async def insert_data(val_json):
    async with async_session_factory as session:
        stmt = insert(parstext).values(**val_json.model_dump())
        print("Запись в БД")
        await session.execute(stmt)
        await session.commit()
    return


# Initialize Kafka consumer
async def consume():
    consumer = AIOKafkaConsumer(
        "my_topic",
        loop=loop,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_CONSUMER_GROUP
    )
    print("Подключение к консюмеру")
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            val_json = json.loads(msg.value.decode('utf-8'))
            print("consumed: ", val_json)
            async with async_engine.connect() as conn:
                stmt = insert(parstext).values(**val_json)
                await conn.execute(stmt)
                await conn.commit()
    finally:
        print("Завершение консюмера")
        await consumer.stop()

asyncio.create_task(consume())

@app.get('/x')
async def get_avg_x():
    async with async_session_factory() as session:
        query = select(parstext)
        result = await session.execute(query)
    return result.mappings().all()



#
#
#
# def create_app():
#     app = FastAPI(docs_url='/')
#
#     @app.on_event("startup")
#     async def startup_event():
#         ...
#
#
#
#
#     @app.get('/pep')
#     def get_attr():
#         return {"ddd": 2}
#
#
#     @app.post("/")
#     async def add_pars_text(new_text: ParstxtCreate):
#         stmt = insert(parstext).values(**new_text.model_dump())
#         await connection.execute(stmt)
#         await connection.commit()
#         return {"status": "success"}
#
#
#
#     return app
# def main():
#     uvicorn.run(
#         f"{__name__}:app",
#         host='127.0.0.1', port=8000,
#         reload=True
#     )
#
# if __name__ == '__main__':
#     main()
