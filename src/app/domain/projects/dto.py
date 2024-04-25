from pydantic import BaseModel, UUID4


class Error(BaseModel):
    error: str


class Account(BaseModel):
    uid: UUID4
    name: str


class ProjectCreate(BaseModel):
    project_key: str = "name-num"
    name: str
    manager_id: UUID4


class Project(BaseModel):
    project_key: str
    name: str
    manager_id: Account = {}


class ProjectList(BaseModel):
    count: int
    items: list[Project] = []


class UpdateProject(BaseModel):
    name: str
    manager_id: UUID4


class UpdatedProject(BaseModel):
    message: str
    new_data: Project = {}


class DeleteProject(BaseModel):
    message: str
