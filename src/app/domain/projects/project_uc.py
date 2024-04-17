from .dto import ProjectCreate, Project, DeleteProject, ProjectList, UpdateProject
from .project_irep import IRepProject

class ProjectUseCase:

    def __init__(self, repo: IRepProject):
        self._repo = repo

    async def create_project(self, project: Project) -> ProjectCreate: pass

    async def get_projects(self) -> ProjectList: pass

    async def get_project(self, project_id: int) -> Project: pass

    async def update_project(self, project: Project) -> UpdateProject: pass

    async def delete_project(self, project_id: int) -> DeleteProject: pass