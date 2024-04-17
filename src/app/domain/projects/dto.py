from pydantic import BaseModel, UUID4

class Error(BaseModel):
    error: str

class ProjectCreate(BaseModel):
    name: str

class Project(ProjectCreate):
    uid: UUID4

class ProjectList(BaseModel):
    count: int
    items: list[Project] = []

class UpdateProject(ProjectCreate):
    pass

class DeleteProject(Project):
    pass