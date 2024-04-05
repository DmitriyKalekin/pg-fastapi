from fastapi import APIRouter, FastAPI, Path
from fastapi.responses import JSONResponse
from .deps import AAccountUC, EmailBusyException
from .dto import AccountCreate, Account, Error, AccountList

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
    

#
# @router.get("/{uid}")
# async def get_account(uid: str = Path(...)):
#     return {"uid": "123"}
#
#
# @router.delete("/{uid}")
# async def delete_account(uid: str = Path(...)):
#     return {"uid": "123"}
#
#
# @router.patch("/{uid}")
# async def patch_account(uid: str = Path(...)):
#     return {"uid": "123"}
#
#
# @router.put("/{uid}")
# async def update_account(uid: str = Path(...)):
#     return {"uid": "123"}
