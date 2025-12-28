from celery import Celery
from src.config import settings


RABBITMQ_URL = settings.RABBITMQ_URL
REDIS_URL = settings.REDIS_URL


app = Celery(
    'ai_worker_tasks',
    broker=RABBITMQ_URL,
    backend=REDIS_URL,
    include=['src.tasks']
)


app.conf.update(
    task_track_started=True,
)