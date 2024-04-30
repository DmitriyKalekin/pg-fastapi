from fastapi import APIRouter, FastAPI, Path, Body, Query
from fastapi.responses import JSONResponse
from .deps import (
    AAccountUC,
    EmailBusyException,
    InvalidUidException,
    AccountNotFoundException,
)
from .dto import (
    AccountCreate,
    Account,
    Error,
    AccountList,
    UpdateAccount,
    DeleteAccount,
)

prefix = "/api/v1/accounts"
router = APIRouter(prefix=prefix, tags=["accounts"])


@router.post("/", response_model=Account, responses={400: {"model": Error}})
async def create_account(uc: AAccountUC, req: AccountCreate):
    try:
        acc: Account = await uc.create_account(req)
    except EmailBusyException as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    return acc


@router.get("/", response_model=AccountList)
async def get_all_accounts(uc: AAccountUC):
    acclist: AccountList = await uc.get_all_account()
    return acclist


@router.get(
    "/{uid}",
    response_model=Account,
    responses={404: {"model": Error}, 422: {"model": Error}},
)
async def get_account(uc: AAccountUC, uid: str = Path(...)):
    try:
        acc: Account = await uc.get_account(uid)
    except InvalidUidException as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    except AccountNotFoundException as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return acc


@router.patch(
    "/{uid}",
    response_model=UpdateAccount,
    responses={404: {"model": Error}, 422: {"model": Error}},
)
async def patch_account(
    uc: AAccountUC, uid: str = Path(...), req: AccountCreate = Body(...)
):
    try:
        res = await uc.patch_account(uid, req)
    except InvalidUidException as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    except AccountNotFoundException as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res


@router.put(
    "/{uid}",
    response_model=UpdateAccount,
    responses={404: {"model": Error}, 422: {"model": Error}},
)
async def put_account(
    uc: AAccountUC, uid: str = Path(...), req: AccountCreate = Body(...)
):
    try:
        res = await uc.put_account(uid, req)
    except InvalidUidException as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    except AccountNotFoundException as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res


@router.delete(
    "/{uid}",
    response_model=DeleteAccount,
    responses={404: {"model": Error}, 422: {"model": Error}},
)
async def delete_account(uc: AAccountUC, uid: str = Path(...)):
    try:
        res: bool = await uc.delete_account(uid)
    except InvalidUidException as e:
        return JSONResponse({"error": str(e)}, status_code=422)
    return res
