from fastapi import FastAPI, APIRouter, Path, Body
from fastapi.responses import JSONResponse
from .deps import AIssuesUC, ProjectNotFound, AccountNotFound, IssueNotFound
from .dto import (
    Error,
    Issue,
    IssueList,
    CreateIssue,
    DeleteIssue,
    UpdateIssue,
)

prefix = "/api/v1/issues"
router = APIRouter(prefix=prefix, tags=["issues"])


@router.post(
    "/", response_model=Issue, responses={422: {"model": Error}, 404: {"model": Error}}
)
async def create_issue(uc: AIssuesUC, req: CreateIssue = Body(...)):
    try:
        res: Issue = await uc.create_issue(req)
    except AccountNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    except ProjectNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res


@router.get("/", response_model=IssueList)
async def get_all_issues(uc: AIssuesUC):
    islist: IssueList = await uc.get_all_issues()
    return islist


@router.get("/{task_id}", response_model=Issue, responses={404: {"model": Error}})
async def get_issue_by_id(uc: AIssuesUC, task_id: str = Path(...)):
    try:
        res: Issue = await uc.get_issue_by_id(task_id)
    except IssueNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res


@router.get("/project/{project_key}", responses={404: {"model": Error}})
async def get_issue_by_project(uc: AIssuesUC, project_key: str = Path(...)):
    try:
        res = await uc.get_issue_by_project(project_key)
    except ProjectNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res


@router.put("/{task_id}", responses={404: {"model": Error}})
async def put_issue(
    uc: AIssuesUC, task_id: str = Path(...), req: CreateIssue = Body(...)
):
    try:
        res = await uc.put_issue(task_id, req)
    except IssueNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    except AccountNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    except ProjectNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res


@router.patch("/{task_id}", responses={404: {"model": Error}})
async def patch_issue(
    uc: AIssuesUC, task_id: str = Path(...), req: CreateIssue = Body(...)
):
    try:
        res = await uc.patch_issue(task_id, req)
    except IssueNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    except AccountNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    except ProjectNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res


@router.delete(
    "/{task_id}", response_model=DeleteIssue, responses={404: {"model": Error}}
)
async def delete_issue(uc: AIssuesUC, task_id: str = Path(...)):
    try:
        res = await uc.delete_issue(task_id)
    except IssueNotFound as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res
