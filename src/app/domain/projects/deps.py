from fastapi import Depends
from typing import Annotated
from .project_uc import ProjectUseCase
from .project_pg_repo import ProjectPgRepo
from .config import Config, get_config


async def deps_pg() -> ProjectUseCase:  # pragma: no cover
    cfg: Config = get_config()
    repo = ProjectPgRepo(cfg)
    return ProjectUseCase(repo)


AProjectUC = Annotated[ProjectUseCase, Depends(deps_pg)]
