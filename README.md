# Тестовое задание!

Дано:
Файл text.txt

Создать асинхронное приложение FastAPI на основе шаблона:

```python
import uvicorn
from fastapi import FastAPI

def create_app():
    app = FastAPI(docs_url='/')

    @app.on_event("startup")
    async def startup_event():
        ...

    return app

def main():
    uvicorn.run(
        f"{name}:create_app",
        host='0.0.0.0', port=8888,
        debug=True,
    )

if name == 'main':
    main()
```

## Приложение:
1. предоставляет эндроинт загрузки и отправки построчно в топик брокера сообщений исходных данных вида {"datetime": "15.11.2023 15:00:25.001", "title": "Very fun book", "text": "...Rofl...lol../n..ololo..." } с интервалом 3с;
    1. получает исходных данные из топика брокера сообщений;
    2. вычисляет количество вхождений буквы "Х" в строках текста из поля "text";
    3. сохраняет результат в БД;

2. предоставляет эндроинт для получения результата из БД в виде [{"datetime": "15.11.2023 15:00:25.001", "title": "Very fun book", "x_avg_count_in_line": 0.012}, {"datetime": "18.01.2023 12:00:25.001", "title": "Other very fun book", "x_avg_count_in_line": 0.032} ] где x_avg_count_in_line -- среднее значение количества вхождений по каждому из загруженых текстов

## Требования:
1. применить asyncio
2. использовать любую БД
3. использовать брокер сообщений (я использовал Apache Kafka)
4. использовать Pydantic для верификации и парсинга данных
5. Обернуть приложение в Docker