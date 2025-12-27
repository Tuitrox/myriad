from fastapi import FastAPI
from src.routers import notes
from contextlib import asynccontextmanager
# from src.rabbit import rabbit_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await rabbit_client.connect()
    yield
    # await rabbit_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])


@app.get("/api")
async def main():
    return {"message": "its api"}