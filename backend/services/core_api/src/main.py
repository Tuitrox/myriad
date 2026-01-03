from fastapi import FastAPI
from src.routers import notes, auth
from contextlib import asynccontextmanager
from src.rabbit import rabbit
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit.connect()
    yield
    await rabbit.close()

app = FastAPI(lifespan=lifespan)

app.include_router(notes.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/api")
async def main():
    return {"message": "its api"}