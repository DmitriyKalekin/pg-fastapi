from pydantic import BaseModel, UUID4

class Error(BaseModel):
    error: str

class ProjectCreate(BaseModel):
    name: str
    manager_id: UUID4
    status_id: int = 1

class Project(ProjectCreate):
    project_key: str

class ProjectList(BaseModel):
    count: int
    items: list[Project] = []

class UpdateProject(ProjectCreate):
    pass

class DeleteProject(BaseModel):
    pass