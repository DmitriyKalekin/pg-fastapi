from .dto import (
    ProjectCreate,
    Project,
    ProjectList,
    UpdateProject,
    Success,
    ProjectCreateSuccess,
)
from .project_irep import IRepProject


class ProjectUseCase:

    def __init__(self, repo: IRepProject):
        self._repo = repo

    async def create_project(self, req: ProjectCreate) -> ProjectCreateSuccess:
        req_dict = req.model_dump()
        try:
            res = await self._repo.create_project(req_dict)
        except KeyError:
            raise KeyError("key busy")
        return ProjectCreateSuccess(name=res, **req_dict)

    async def get_all_project(self) -> ProjectList:
        projects = await self._repo.get_all_project()
        items = [Project(**el) for el in projects]
        return ProjectList(count=len(projects), items=items)

    async def get_project(self, project_key: str) -> Project:
        try:
            res = await self._repo.get_project(project_key)
        except KeyError:
            raise KeyError("key not found")
        return Project(**res)

    async def patch_project(self, project_key: str, req: UpdateProject) -> bool:
        req_dict = req.model_dump()

        try:
            res = await self._repo.update_project(project_key, req_dict)
        except KeyError:
            raise KeyError("key not found")
        return Success(message=res)

    async def put_project(self, project_key: str, req: dict) -> bool:
        try:
            res = await self._repo.update_project(project_key, req)
        except KeyError:
            raise KeyError("key not found")
        return Success(message=res)

    async def delete_project(self, project_key: str) -> bool:
        try:
            res = await self._repo.delete_project(project_key)
        except KeyError:
            raise KeyError("invalid key")
        return Success(message=res)
