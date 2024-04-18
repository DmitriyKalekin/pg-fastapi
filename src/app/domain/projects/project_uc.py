from .dto import ProjectCreate, Project, DeleteProject, ProjectList, UpdateProject
from .project_irep import IRepProject

class ProjectUseCase:

    def __init__(self, repo: IRepProject):
        self._repo = repo

    async def create_project(self, req: ProjectCreate) -> Project: 
        req_dict = req.model_dump()
        project_key = f"{req_dict["name"]}-1"
        # try:
        res = await self._repo.create_project(project_key ,req_dict)
        # except KeyError:
        #     raise KeyError("key busy")
        return res

    async def get_all_project(self) -> ProjectList: 
        projects = await self._repo.get_all_project()
        items = [Project(**el) for el in projects]
        return ProjectList(count=len(projects), items=items)

    async def get_project(self, project_id: int) -> Project: pass

    async def update_project(self, project: Project) -> UpdateProject: pass

    async def delete_project(self, project_id: int) -> DeleteProject: pass