from fastapi import APIRouter, Depends

from src.celery_app import send_task as celery_send_task
from src.models import User
from src.routers.auth import get_current_user


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/")
async def create_note(user: User = Depends(get_current_user)):
    task_msg = await celery_send_task("src.tasks.do_something", ["my text its realy works! wow"])\
    
    task_msg.update({"user_id": user.id, "user_email": user.email})

    return task_msg

