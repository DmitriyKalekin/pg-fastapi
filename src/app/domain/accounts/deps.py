from fastapi import Depends
from typing import Annotated
from .account_uc import AccountUseCase, EmailBusyException, InvalidUidException, AccountNotFoundException
from .account_pg_repo import AccountPgRepo
from .config import Config, get_config


async def create_account_uc():  # pragma: no cover
    cfg = get_config()
    repo = AccountPgRepo(cfg)
    return AccountUseCase(repo)


AAccountUC = Annotated[AccountUseCase, Depends(create_account_uc)]
