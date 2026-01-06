import aio_pika
import json
from src.config import settings


RABBITMQ_URL = settings.RABBITMQ_URL

class RabbitClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        """Подключаемся к RabbitMQ при старте приложения"""
        self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()
        
        await self.channel.declare_queue("notes_queue", durable=True)
        print("[RabbitMQ] Connected and queue declared")

    async def close(self):
        """Закрываем соединение при выключении"""
        if self.connection:
            await self.connection.close()
            print("[RabbitMQ] Connection closed")

    async def send_task(self, message_data: dict, queue_name: str = "notes_queue"):
        """Отправка сообщения в очередь"""
        if not self.channel:
            await self.connect()

        body = json.dumps(message_data).encode()
        message = aio_pika.Message(
            body=body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await self.channel.default_exchange.publish(
            message,
            routing_key=queue_name
        )
        print(f"[RabbitMQ] Sent: {message_data}")


rabbit = RabbitClient()