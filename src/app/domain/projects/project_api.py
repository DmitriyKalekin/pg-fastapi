from fastapi import FastAPI, APIRouter, Path, Body, Query
from fastapi.responses import JSONResponse
from .deps import AProjectUC
from .dto import ProjectCreate, Project, DeleteProject, ProjectList, UpdateProject, Error

prefix = "/api/v1/projects"
router = APIRouter(prefix=prefix, tags=["projects"])

@router.post("/", response_model=ProjectCreate, status_code=200)
async def create_project(uc: AProjectUC, req: ProjectCreate = Body(...)):
    try:
        res = await uc.create_project(req)
    except KeyError:
        return JSONResponse(status_code=400, content=Error(message="key busy"))
    return res

@router.get("/", response_model=ProjectList, status_code=200)
async def get_all_projects(uc: AProjectUC):
    prjlist: ProjectList = await uc.get_all_project()
    return prjlist

# @router.get("/{project_id}", response_model=Project, status_code=200)
# async def get_project(project_id: int):
#     return await AProjectUC.get_project(project_id)

# @router.patch("/{project_id}", response_model=UpdateProject, status_code=200)
# async def patch_project(project_id: int, project: UpdateProject = Body(...)):
#     return await AProjectUC.update_project(project_id, project)

# @router.put("/{project_id}", response_model=UpdateProject, status_code=200)
# async def put_project(project_id: int, project: UpdateProject = Body(...)):
#     return await AProjectUC.update_project(project_id, project)

# @router.delete("/{project_id}", response_model=DeleteProject, status_code=200)
# async def delete_project(project_id: int):
#     return await AProjectUC.delete_project(project_id)
