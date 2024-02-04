import asyncio
import json
import time
from datetime import datetime

import uvicorn
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import FastAPI, BackgroundTasks, UploadFile
from sqlalchemy import select, insert, Integer, func

from config import loop, settings
from database import async_engine, sync_engine, async_session_factory
from models import metadata, parstext

app = FastAPI(docs_url='/')



@app.on_event("startup")
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
# async def startup_event():
#     metadata.drop_all(sync_engine)
#     metadata.create_all(sync_engine)

async def process_file_content(file, file_name):
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    try:
        date_now = str(datetime.utcnow())
        for line in file.split("\n"):
            if line := line.strip():
                # print(f"Посылаем в топик сообщение: {line}")
                x_count = line.count('х')
                val_json = json.dumps(
                    {"datetime": date_now, "title": file_name, "text": line, "count_x": x_count}).encode('utf-8')
                await producer.send("my_topic", value=val_json)
                await asyncio.sleep(3)
    finally:
        print('Завершение продюсера')
        await producer.stop()

@app.post('/')
async def send_messages(file: UploadFile, background_tasks: BackgroundTasks):
    file_name = file.filename
    content = file.file.read().decode()
    background_tasks.add_task(process_file_content, content, file_name)


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
        async with async_engine.connect() as conn:
            async for msg in consumer:
                val_json = json.loads(msg.value.decode('utf-8'))
                print("consumed: ", val_json)
                stmt = insert(parstext).values(**val_json)
                await conn.execute(stmt)
                await conn.commit()
                # await asyncio.sleep(3)
    finally:
        print("Завершение консюмера")
        await consumer.stop()

asyncio.create_task(consume())

@app.get('/avd_x')
async def get_avg_x():
    async with async_session_factory() as session:
        query = (
            select(parstext.c.datetime, parstext.c.title,
            func.avg(parstext.c.count_x).label("x_avg_count_in_line"))
            .group_by(parstext.c.datetime, parstext.c.title)
        )
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
