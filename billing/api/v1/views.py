from uuid import uuid4
import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List

from billing.app.config import config
from billing.api.v1.controllers.users import get_users, create_user
from billing.api.v1.controllers.tasks import payment_task
from billing.api.v1.serializers import UserSchema, UserWalletSchema, PaymentBaseSchema, TransferSchema

v1_router = APIRouter()
logger = logging.getLogger(config.APP_NAME)


@v1_router.get("/users", response_model=List[UserWalletSchema])
async def get_users_view():
    users = await get_users()
    return users


@v1_router.post("/users")
async def add_users_view(user: UserSchema):
    await create_user(**dict(user))
    return JSONResponse(status_code=201)


@v1_router.post("/wallets/transfer")
async def transfer_money_view(payment: TransferSchema, correlation_id=Depends(uuid4)):
    await payment_task(correlation_id=str(correlation_id), reason_code="TRANSFER", **dict(payment))
    return JSONResponse(dict(operation_id=str(correlation_id)), status_code=200)


@v1_router.post("/wallets/topUp")
async def top_up_money_view(payment: PaymentBaseSchema, correlation_id=Depends(uuid4)):
    await payment_task(correlation_id=str(correlation_id), reason_code="TOPUP", **dict(payment))
    return JSONResponse(dict(operation_id=str(correlation_id)), status_code=200)
