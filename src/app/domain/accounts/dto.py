from pydantic import BaseModel, EmailStr, UUID4
from pydantic.fields import Field


class Error(BaseModel):
    error: str

class AccountCreate(BaseModel):
    email: EmailStr
    name: str


class Account(AccountCreate):
    uid: UUID4

class UpdateAccount(Account):
    pass

class DeleteAccount(Account):
    pass
