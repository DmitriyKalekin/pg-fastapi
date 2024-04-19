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
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res

@router.get("/", response_model=ProjectList, status_code=200)
async def get_all_projects(uc: AProjectUC):
    prjlist: ProjectList = await uc.get_all_project()
    return prjlist

@router.get("/{project_key}", response_model=Project, status_code=200)
async def get_project(uc: AProjectUC, project_key: str = Path(...)):
    try:
        prj: Project = await uc.get_project(project_key)
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return prj

@router.patch("/{project_key}", status_code=200)
async def patch_project(
    uc: AProjectUC, project_key: str, project: UpdateProject = Body(...)
):
    try:
        res = await uc.patch_project(project_key, project)
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res

@router.put("/{project_key}", status_code=200)
async def put_project(
    uc: AProjectUC,
    project_key: str = Path(...),
    name: str = Query(...),
    manager_id: str = Query(...),
    status_id: int = Query(...)
):
    req = {
        "name": name,
        "manager_id": manager_id,
        "status_id": status_id
    }
    try:
        res = await uc.put_project(project_key, req)
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res

@router.delete("/{project_key}", status_code=200)
async def delete_project(uc: AProjectUC, project_key: str = Path(...)):
    try:
        res = await uc.delete_project(project_key)
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return {"status": "OK" if res == True else "Deleted"}
    
