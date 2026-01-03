from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import notes, auth
from contextlib import asynccontextmanager

from src.rabbit import rabbit
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit.connect()
    yield
    await rabbit.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    root_path=settings.ROOT_PATH,
    lifespan=lifespan
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/api")
async def main():
    return {"message": "its api"}