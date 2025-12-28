from celery import Celery
from src.config import settings


RABBITMQ_URL = settings.RABBITMQ_URL
REDIS_URL = settings.REDIS_URL

celery_app = Celery(
    "core_api",
    broker=RABBITMQ_URL,
    backend=REDIS_URL
)


async def send_task(task_name, args = None, kwargs = None):
    try:
        task = celery_app.send_task(name=task_name, args=args, kwargs=kwargs)

        return {
            "status": "success",
            "message": "task in rabbit",
            "task_id": task.id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": "something wrong",
            "error": str(e)
        }