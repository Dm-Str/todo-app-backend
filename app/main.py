from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router
from app.models.task import TaskORM
from app.models.category import CategoryORM


# @asynccontextmanager
# async def lifespan(_: FastAPI):
#
#
#
#     yield


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(task_router)
app.include_router(category_router)
