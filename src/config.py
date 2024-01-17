import asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict

loop = asyncio.get_event_loop()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: int
    DB_NAME: str

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str
    KAFKA_CONSUMER_GROUP: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:123@localhost:5432/parstxt
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        # postgresql+psycopg://postgres:123@localhost:5432/sa
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Если захочешь вызвать из IDE, а не из консоли. Используй - "E:\Python courses\sql_alchemy_cours\.env" или "..\.env"
    model_config = SettingsConfigDict(env_file='..\.env')


settings = Settings()