import asyncio
import json
import logging
from aio_pika import connect_robust, IncomingMessage
from src.email_sender import send_verification_email
from src.config import settings


async def process_message(message: IncomingMessage):
    async with message.process():
        body = json.loads(message.body.decode())
        print(f"Received task: {body['type']} for {body.get('email')}")
        
        if body['type'] == 'email_verification':
            await send_verification_email(
                email=body['email'], 
                token=body['token']
            )
            print("Email sent!")
            
        elif body['type'] == 'telegram_notification':
            pass


async def main():
    connection = await connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    
    queue = await channel.declare_queue("notifications_queue", durable=True)
    
    print(" [*] Notification Service waiting for messages...")
    await queue.consume(process_message)
    
    await asyncio.Future()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())