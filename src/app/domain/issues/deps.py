from fastapi import Depends
from typing import Annotated
from .issues_uc import IssuesUseCase, ProjectNotFound, AccountNotFound, IssueNotFound

from .issues_pg_repo import IssuesPgRepo
from .config import Config, get_config

async def deps_pg(): # pragma: no cover
    cfg = get_config()
    repo = IssuesPgRepo(cfg)
    return IssuesUseCase(repo)

AIssuesUC = Annotated[IssuesUseCase, Depends(deps_pg)]