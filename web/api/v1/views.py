import logging
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from web.app import config
from web.api.v1.controllers.users import create_user, get_users
from web.api.v1.serializers import UserRequest, UserWallet

v1_router = APIRouter()
logger = logging.getLogger(config.APP_NAME)


@v1_router.get("/users")
async def get_users_view():
    users = await get_users()
    return users


@v1_router.post("/users")
async def add_users_view(user: UserRequest):
    await create_user(**dict(user))
    return PlainTextResponse(status_code=201)
