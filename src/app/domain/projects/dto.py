from pydantic import BaseModel, UUID4


class Error(BaseModel):
    error: str


class Success(BaseModel):
    message: str


class ProjectCreate(BaseModel):
    project_key: str = "name-num"
    manager_id: UUID4
    status: int = 1


class ProjectCreateSuccess(BaseModel):
    project_key: str
    name: str
    manager_id: UUID4
    status: int


class Project(BaseModel):
    project_key: str
    name: str
    manager_id: UUID4
    status: str


class ProjectList(BaseModel):
    count: int
    items: list[Project] = []


class UpdateProject(BaseModel):
    name: str
    manager_id: UUID4
    status: int = 1
