from uuid import UUID
from .dto import AccountCreate, Account, UpdateAccount, AccountList
from .account_irep import IRepAccount


class EmailBusyException(Exception):
    pass


class InvalidUidException(Exception):
    pass


class AccountNotFoundException(Exception):
    pass


class AccountUseCase:
    def __init__(self, repo: IRepAccount):
        self._repo = repo

    async def create_account(self, req: AccountCreate) -> Account:
        req_dict = req.model_dump()
        try:
            uid = await self._repo.create_account(tuple(req_dict.values()))
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
            raise InvalidUidException("invalid uid")
        except ValueError:
            raise AccountNotFoundException("account not found")
        return Account(**account)

    async def patch_account(self, uid: UUID, req: AccountCreate) -> UpdateAccount:
        req_dict = req.model_dump()

        try:
            res = await self._repo.update_account(uid, tuple(req_dict.values()))
        except KeyError:
            raise InvalidUidException("invalid uid")
        except ValueError:
            raise AccountNotFoundException("account not found")
        return UpdateAccount(message="updated", new_data=Account(uid=res, **req_dict))

    async def put_account(self, uid: UUID, req: AccountCreate) -> UpdateAccount:
        req_dict = req.model_dump()

        try:
            res = await self._repo.update_account(uid, tuple(req_dict.values()))
        except KeyError:
            raise InvalidUidException("invalid uid")
        except ValueError:
            raise AccountNotFoundException("account not found")
        return UpdateAccount(message="updated", new_data=Account(uid=res, **req_dict))

    async def delete_account(self, uid: UUID) -> dict:
        try:
            res = await self._repo.delete_account(uid)
        except KeyError:
            raise InvalidUidException("invalid uid")
        return res
