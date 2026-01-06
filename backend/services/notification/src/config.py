from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


ENV_PATH = Path(__file__).parent
while ENV_PATH.name != "myriad":
    if str(ENV_PATH) == str(ENV_PATH.root):
        ENV_PATH = ".env"
        break

    ENV_PATH = ENV_PATH.parent
else:
    ENV_PATH = ENV_PATH / ".env"


class Settings(BaseSettings):
    SECRET_KEY: str
    DOMAIN_NAME: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    # RabbitMQ
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672


    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    class Config:
        env_file = ".env"

settings = Settings()