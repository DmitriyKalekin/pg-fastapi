from .dto import AccountCreate, Account, UpdateAccount, DeleteAccount
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

    async def get_all_account(self) -> Account:
        account = await self._repo.get_all_account()
        return account
        
    
    # async def get_account(self, uid):
    #     print("created")
    #
    # async def delete_account(self, uid):
    #     print("created")
    #
    # async def update_account(self, uid):
    #     print("created")
    #
    # async def patch_account(self, uid):
    #     print("created")
