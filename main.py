from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from src.routers import entities
from src.db.session import create_all_tables
from src.middleware import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=entities.router)

app.add_middleware(BaseHTTPMiddleware, dispatch=logging.log_error_response)
