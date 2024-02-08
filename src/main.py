import asyncio
import json
from datetime import datetime

import uvicorn
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import FastAPI, BackgroundTasks, UploadFile
from sqlalchemy import select, insert, func

from config import settings
from database import async_engine, async_session_factory
from models import metadata, parstext
from schemas import Get_Avg_X

# app = FastAPI(docs_url='/')
#
# loop = asyncio.get_running_loop()
#
# @app.on_event("startup")
# async def create_tables():
#     async with async_engine.begin() as conn:
#         # await conn.run_sync(metadata.drop_all)
#         await conn.run_sync(metadata.create_all)
#
#
# async def process_file_content(file, file_name):
#     # Initialize Kafka producer
#     producer = AIOKafkaProducer(
#         # loop=loop,
#         # bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
#     )
#     await producer.start()
#
#     try:
#         date_now = str(datetime.utcnow())
#         for line in file.split("\n"):
#             if line := line.strip():
#                 # print(f"Посылаем в топик сообщение: {line}")
#                 x_count = line.count('х')
#                 val_json = (
#                     json.dumps({"datetime": date_now, "title": file_name, "count_x": x_count})
#                     .encode('utf-8')
#                 )
#                 await producer.send("my_topic", value=val_json)
#                 await asyncio.sleep(3)
#     finally:
#         print('Завершение продюсера')
#         await producer.stop()
#
# @app.post('/send_text')
# async def send_messages(file: UploadFile, background_tasks: BackgroundTasks):
#     file_name = file.filename
#     content = file.file.read().decode()
#     background_tasks.add_task(process_file_content, content, file_name)
#
#
# # Initialize Kafka consumer
# async def consume():
#     consumer = AIOKafkaConsumer(
#         "my_topic",
#         # loop=loop,
#         # bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
#         # group_id=settings.KAFKA_CONSUMER_GROUP
#     )
#     print("Подключение к консюмеру")
#     await consumer.start()
#     try:
#         # Consume messages
#         async with async_engine.connect() as conn:
#             async for msg in consumer:
#                 val_json = json.loads(msg.value.decode('utf-8'))
#                 print("consumed: ", val_json)
#                 stmt = insert(parstext).values(**val_json)
#                 await conn.execute(stmt)
#                 await conn.commit()
#     finally:
#         print("Завершение консюмера")
#         await consumer.stop()
#
#
# @app.get('/avg_x')
# async def get_avg_x() -> list[Get_Avg_X]:
#     async with async_session_factory() as session:
#         query = (
#             select(parstext.c.datetime, parstext.c.title,
#             func.avg(parstext.c.count_x).label("x_avg_count_in_line"))
#             .group_by(parstext.c.datetime, parstext.c.title)
#         )
#         result = await session.execute(query)
#     return result.mappings().all()
#
# loop.create_task(consume())
#
# @app.get("/ping")
# async def ping():
#     return {"Status": "Success"}




def create_app():
    app = FastAPI(docs_url='/')

    loop = asyncio.get_running_loop()

    @app.on_event("startup")
    async def create_tables():
        async with async_engine.begin() as conn:
            # await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)

    async def process_file_content(file, file_name):
        # Initialize Kafka producer
        producer = AIOKafkaProducer(
            # loop=loop,
            # bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
        )
        await producer.start()

        try:
            date_now = str(datetime.utcnow())
            for line in file.split("\n"):
                if line := line.strip():
                    # print(f"Посылаем в топик сообщение: {line}")
                    x_count = line.count('х')
                    val_json = (
                        json.dumps({"datetime": date_now, "title": file_name, "count_x": x_count})
                        .encode('utf-8')
                    )
                    await producer.send("my_topic", value=val_json)
                    await asyncio.sleep(3)
        finally:
            print('Завершение продюсера')
            await producer.stop()

    @app.post('/send_text')
    async def send_messages(file: UploadFile, background_tasks: BackgroundTasks):
        file_name = file.filename
        content = file.file.read().decode()
        background_tasks.add_task(process_file_content, content, file_name)

    # Initialize Kafka consumer
    async def consume():
        consumer = AIOKafkaConsumer(
            "my_topic",
            # loop=loop,
            # bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            # group_id=settings.KAFKA_CONSUMER_GROUP
        )
        print("Подключение к консюмеру")
        await consumer.start()
        try:
            # Consume messages
            async with async_engine.connect() as conn:
                async for msg in consumer:
                    val_json = json.loads(msg.value.decode('utf-8'))
                    print("consumed: ", val_json)
                    stmt = insert(parstext).values(**val_json)
                    await conn.execute(stmt)
                    await conn.commit()
        finally:
            print("Завершение консюмера")
            await consumer.stop()

    @app.get('/avg_x')
    async def get_avg_x() -> list[Get_Avg_X]:
        async with async_session_factory() as session:
            query = (
                select(parstext.c.datetime, parstext.c.title,
                       func.avg(parstext.c.count_x).label("x_avg_count_in_line"))
                .group_by(parstext.c.datetime, parstext.c.title)
            )
            result = await session.execute(query)
        return result.mappings().all()

    loop.create_task(consume())

    @app.get("/ping")
    async def ping():
        return {"Status": "Success"}

    return app

def main():
    uvicorn.run(
        f"{__name__}:create_app",
        host='127.0.0.1', port=8001,
        reload=True
    )

if __name__ == '__main__':
    main()
