import logging
from fastapi import APIRouter

from web.app import config

v1_router = APIRouter()
logger = logging.getLogger(config.APP_NAME)


@v1_router.get("/wallets")
def read_root():
    return {"Hello": "World"}


