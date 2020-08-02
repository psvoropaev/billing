from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from billing import errors
from billing.app.config import config
from billing.app.logger import create_logger
from billing.api.v1 import v1_router
from billing.api.v1.controllers.tasks import payment_task
from billing.app.pg import db_pool_shared
from billing.app.redis import run_errors_payments


def create_app():
    create_logger()
    app = FastAPI(title=config.APP_NAME)
    app.include_router(v1_router, prefix='/v1')
    return app


app = create_app()


@app.on_event("startup")
async def startup():
    await db_pool_shared.init_db()
    await run_errors_payments(payment_task)


@app.on_event("shutdown")
async def shutdown():
    await db_pool_shared.close_db()


@app.exception_handler(errors.BaseException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=exc.http_code)
