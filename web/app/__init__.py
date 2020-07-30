from fastapi import FastAPI

from web.app.config import config
from web.app.logger import create_logger
from web.api.v1 import v1_router
from web.app.pg import db_pool_shared


def create_app():
    create_logger()
    app = FastAPI(title=config.APP_NAME)
    app.include_router(v1_router, prefix='/v1')
    return app


app = create_app()


@app.on_event("startup")
async def startup():
    db_pool_shared.init_db


@app.on_event("shutdown")
async def shutdown():
    db_pool_shared.close_db
