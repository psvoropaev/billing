from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    pasport_data: str


class UserWalletSchema(UserSchema):
    bill_number: str
    balance: float


class PaymentBaseSchema(BaseModel):
    bill_number: str
    amount: float


class TransferSchema(PaymentBaseSchema):
    bill_number_sender: str
