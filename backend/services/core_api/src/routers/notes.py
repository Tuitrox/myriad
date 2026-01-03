from fastapi import APIRouter
from src.celery_app import send_task as celery_send_task

router = APIRouter(prefix="/api/notes", tags=["Notes"])


@router.get("/")
async def create_note():  
    return await celery_send_task("src.tasks.do_something", ["my text its realy works! wow"])