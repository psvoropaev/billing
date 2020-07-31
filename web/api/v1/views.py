from uuid import uuid4, UUID
import logging
from fastapi import APIRouter, Depends

from web.app import config

v1_router = APIRouter()
logger = logging.getLogger(config.APP_NAME)


@v1_router.get("/users")
async def get_users_view():
    return {"Hello": "World"}


@v1_router.post("/users")
async def add_users_view(uid: UUID = Depends(uuid4)):
    return {"Hello": "World"}


