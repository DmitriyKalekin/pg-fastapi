from fastapi import FastAPI, APIRouter, Path, Body, Query
from fastapi.responses import JSONResponse
from .deps import AProjectUC, UidNotFound, KeyNotFound
from .dto import (
    ProjectCreate,
    Project,
    ProjectList,
    UpdateProject,
    UpdatedProject,
    DeleteProject,
    Error,
)

prefix = "/api/v1/projects"
router = APIRouter(prefix=prefix, tags=["projects"])


@router.post("/", response_model=Project, responses={422: {"model": Error}})
async def create_project(uc: AProjectUC, req: ProjectCreate = Body(...)):
    try:
        res: Project = await uc.create_project(req)
    except UidNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    return res


@router.get("/", response_model=ProjectList)
async def get_all_projects(uc: AProjectUC):
    prjlist: ProjectList = await uc.get_all_project()
    return prjlist


@router.get("/{project_key}", response_model=Project, responses={404: {"model": Error}})
async def get_project(uc: AProjectUC, project_key: str = Path(...)):
    try:
        prj: Project = await uc.get_project(project_key)
    except KeyNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return prj


@router.patch(
    "/{project_key}",
    response_model=UpdatedProject,
    responses={404: {"model": Error}, 422: {"model": Error}},
)
async def patch_project(
    uc: AProjectUC, project_key: str, project: UpdateProject = Body(...)
):
    try:
        res = await uc.patch_project(project_key, project)
    except KeyNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)

    except UidNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    return res


@router.put(
    "/{project_key}",
    response_model=UpdatedProject,
    responses={404: {"model": Error}, 422: {"model": Error}},
)
async def put_project(
    uc: AProjectUC,
    project_key: str = Path(...),
    req: UpdateProject = Body(...),
):
    try:
        res = await uc.put_project(project_key, req)
    except KeyNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)

    except UidNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    return res


@router.delete(
    "/{project_key}", response_model=DeleteProject, responses={404: {"model": Error}}
)
async def delete_project(uc: AProjectUC, project_key: str = Path(...)):
    try:
        res = await uc.delete_project(project_key)
    except KeyNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res
