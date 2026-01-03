import sys
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_PATH = Path(__file__).parent
while ENV_PATH.name != "myriad":
    if str(ENV_PATH) == str(ENV_PATH.root):
        ENV_PATH = ".env"
        break

    ENV_PATH = ENV_PATH.parent
else:
    ENV_PATH = ENV_PATH / ".env"


class Settings(BaseSettings):
    MODE: str = "DEV"
    
    PROJECT_NAME: str = "Myriad Notes"
    
    # PostgreSQL
    POSTGRES_CORE_DB_USER: str
    POSTGRES_CORE_DB_PASS: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # RabbitMQ
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672

    # Redis
    REDIS_HOST: str
    REDIS_AI_DB: str = "1"
    REDIS_PORT: int = 5672

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_CORE_DB_USER}:{self.POSTGRES_CORE_DB_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_AI_DB}"

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH), 
        env_file_encoding='utf-8',
        extra="ignore"
    )

settings = Settings()