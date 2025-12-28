from src.celery_app import app
import time


@app.task()
def do_something(text: str = "default"):
    print(text)

    time.sleep(3)

    return {"status": "success", "message": "im done!"}