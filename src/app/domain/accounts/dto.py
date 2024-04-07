from pydantic import BaseModel, EmailStr, UUID4
from pydantic.fields import Field


class Error(BaseModel):
    error: str

class AccountCreate(BaseModel):
    email: EmailStr
    name: str


class Account(AccountCreate):
    uid: UUID4

class AccountList(BaseModel):
    count: int
    items: list[Account] = []

class UpdateAccount(AccountCreate):
    pass

class DeleteAccount(Account):
    pass
