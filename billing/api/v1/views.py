from uuid import uuid4

import logging
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from billing.app import config
from billing.api.v1.controllers.users import get_users, create_user
from billing.api.v1.controllers.tasks import payment_task
from billing.api.v1.serializers import UserSchema, UserWalletSchema, PaymentBaseSchema, TransferSchema

v1_router = APIRouter()
logger = logging.getLogger(config.APP_NAME)


@v1_router.get("/users")
async def get_users_view():
    users = await get_users()
    return users


@v1_router.post("/users")
async def add_users_view(user: UserSchema):
    await create_user(**dict(user))
    return PlainTextResponse(status_code=201)


@v1_router.post("/wallets/transfer")
async def transfer_money_view(payment: TransferSchema, correlation_id=Depends(uuid4)):
    await payment_task.delay(correlation_id=str(correlation_id), reason_code="TRANSFER", **dict(payment))
    return PlainTextResponse(status_code=204)


@v1_router.post("/wallets/accrual")
async def transfer_money_view(payment: PaymentBaseSchema, correlation_id=Depends(uuid4)):
    await payment_task.delay(correlation_id=str(correlation_id), reason_code="ACCRUAL", **dict(payment))
    return PlainTextResponse(status_code=204)
