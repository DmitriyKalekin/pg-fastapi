from pydantic import BaseModel, EmailStr, UUID4
from pydantic.fields import Field
from typing import Optional


class Error(BaseModel):
    error: str


class Success(BaseModel):
    message: str


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


class PatchAccount(AccountCreate):
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class DeleteAccount(Account):
    pass
