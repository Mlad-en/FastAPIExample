from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.routers import entities
from src.db.session import create_all_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=entities.router)
