from uuid import UUID
from .dto import AccountCreate, Account, UpdateAccount, Success, AccountList
from .account_irep import IRepAccount


class EmailBusyException(Exception):
    pass


class AccountUseCase:
    def __init__(self, repo: IRepAccount):
        self._repo = repo

    async def create_account(self, req: AccountCreate) -> Account:
        req_dict = req.model_dump()
        try:
            uid = await self._repo.create_account(req_dict)
        except KeyError:
            raise EmailBusyException("email busy")
        return Account(uid=uid, **req_dict)

    async def get_all_account(self) -> AccountList:
        accounts = await self._repo.get_all_account()
        items = [Account(**el) for el in accounts]
        return AccountList(count=len(accounts), items=items)

    async def get_account(self, uid: UUID) -> Account:
        try:
            account = await self._repo.get_account(uid)
        except KeyError:
            raise KeyError("invalid uid")
        return Account(**account)

    async def patch_account(self, uid: UUID, req: UpdateAccount) -> bool:
        req_dict = req.model_dump()

        try:
            res = await self._repo.update_account(uid, req_dict)
        except KeyError:
            raise KeyError("invalid uid")
        return Success(message=res)

    async def put_account(self, uid: UUID, req: dict) -> bool:
        try:
            res = await self._repo.update_account(uid, req)
        except KeyError:
            raise KeyError("invalid uid")
        return Success(message=res)

    async def delete_account(self, uid: UUID) -> bool:
        try:
            res = await self._repo.delete_account(uid)
        except KeyError:
            raise KeyError("invalid uid")
        return Success(message=res)
