from fastapi import APIRouter, FastAPI, Path, Body, Query
from fastapi.responses import JSONResponse
from .deps import AAccountUC, EmailBusyException
from .dto import AccountCreate, Account, Error, AccountList, UpdateAccount

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

@router.get("/{uid}", response_model=Account, responses={404: {"model": Error}})
async def get_account(uc: AAccountUC, uid: str = Path(...)):
    try:
        acc: Account = await uc.get_account(uid)
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return acc

@router.delete("/{uid}", responses={404: {"model": Error}})
async def delete_account(uc: AAccountUC, uid: str = Path(...)):
    try: 
        res: bool = await uc.delete_account(uid)
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return {"status": "OK"} if res == True else {"status": "Doesn't exist"}

@router.patch("/{uid}", responses={404: {"model": Error}})
async def patch_account(uc: AAccountUC, uid: str = Path(...), req: UpdateAccount = Body(...)):
    try:
        res = await uc.patch_account(uid, req)
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res 


@router.put("/{uid}", responses={404: {"model": Error}})
async def put_account(
    uc: AAccountUC, 
    uid: str = Path(...), 
    email: str = Query(...), 
    name: str = Query(...)
   
):
    req = {
        "email": email,
        "name": name
    }   

    try:
        res = await uc.put_account(uid, req)
    except KeyError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return res
