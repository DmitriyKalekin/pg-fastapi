from .dto import (
    Account,
    ProjectCreate,
    Project,
    ProjectList,
    UpdateProject,
    UpdatedProject,
)

from .project_irep import IRepProject


class UidNotFound(Exception):
    pass


class KeyNotFound(Exception):
    pass


class ProjectUseCase:

    def __init__(self, repo: IRepProject):
        self._repo = repo

    async def create_project(self, req: ProjectCreate):
        req_dict = req.model_dump()
        try:
            res = await self._repo.create_project(tuple(req_dict.values()))
        except KeyError:
            raise UidNotFound("uid not found")
        return Project(
            project_key=req_dict["project_key"],
            name=req_dict["name"],
            manager_id=Account(uid=res[0], name=res[1]),
        )

    async def get_all_project(self) -> ProjectList:
        projects = await self._repo.get_all_project()
        items = [
            Project(
                project_key=el[0], name=el[1], manager_id=Account(uid=el[2], name=el[3])
            )
            for el in projects
        ]
        return ProjectList(count=len(projects), items=items)

    async def get_project(self, project_key: str) -> Project:
        try:
            res = await self._repo.get_project(project_key)
        except ValueError:
            raise KeyNotFound("key not found")
        return Project(
            project_key=res[0], name=res[1], manager_id=Account(uid=res[2], name=res[3])
        )

    async def patch_project(self, project_key: str, req: UpdateProject) -> dict:
        req_dict = req.model_dump()

        try:
            res = await self._repo.update_project(project_key, tuple(req_dict.values()))
        except ValueError:
            raise KeyNotFound("key not found")

        except KeyError:
            raise UidNotFound("uid not found")

        return UpdatedProject(
            message="updated",
            new_data=Project(
                project_key=project_key,
                name=req_dict["name"],
                manager_id=Account(uid=res[0], name=res[1]),
            ),
        )

    async def put_project(self, project_key: str, req: UpdateProject) -> dict:
        req_dict = req.model_dump()

        try:
            res = await self._repo.update_project(project_key, tuple(req_dict.values()))
        except ValueError:
            raise KeyNotFound("key not found")

        except KeyError:
            raise UidNotFound("uid not found")

        return UpdatedProject(
            message="updated",
            new_data=Project(
                project_key=project_key,
                name=req_dict["name"],
                manager_id=Account(uid=res[0], name=res[1]),
            ),
        )

    async def delete_project(self, project_key: str) -> dict:
        try:
            res = await self._repo.delete_project(project_key)
        except KeyError:
            raise KeyNotFound("key not found")
        return res
