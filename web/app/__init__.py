from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from web import errors
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
    await db_pool_shared.init_db(app)


@app.on_event("shutdown")
async def shutdown():
    await db_pool_shared.close_db(app)


@app.exception_handler(errors.DuplicateUser)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)