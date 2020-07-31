from pydantic import BaseModel


class User(BaseModel):
    name: str
    pasport_data: str


class UserWallet(User):
    bill_number: str