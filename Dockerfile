FROM python:3.10.11

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR src

#CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

EXPOSE 8000


CMD uvicorn main:create_app --host 127.0.0.1

