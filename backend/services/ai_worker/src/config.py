from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MODE: str = "DEV"

    # RabbitMQ
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672

    # Redis
    REDIS_HOST: str
    REDIS_AI_DB: str = 1
    REDIS_PORT: int = 5672

    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_AI_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()