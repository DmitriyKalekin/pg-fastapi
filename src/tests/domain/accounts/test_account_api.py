from uuid import UUID
import pytest
from app.domain.accounts.deps import (
    create_account_uc,
    AccountUseCase,
    EmailBusyException,
)
from app.domain.accounts.account_irep import IRepAccount

pytestmark = pytest.mark.asyncio


class MockRepo(IRepAccount):
    async def create_account(self, _: dict):
        return "56986558-57f9-4117-a26f-05fa0cffe8ee"

    async def get_all_account(self):
        return [
            {
                "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
                "email": "aaa@dot.com",
                "name": "my_name",
            }
        ]

    async def get_account(self, _: str):
        return {
            "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "email": "aaa@dot.com",
            "name": "my_name",
        }

    async def delete_account(self, _: str):
        return {"status: OK"} if True else {"status: Doesn't exist"}

    async def update_account(self, _: UUID, req: dict):
        return "UPDATE 1"


class MockRepoError(IRepAccount):
    async def create_account(self, _: dict):
        raise KeyError("email busy")

    async def get_account(self, _: str):
        raise KeyError("invalid uid")

    async def delete_account(self, _: str):
        raise KeyError("invalid uid")

    async def update_account(self, _: UUID, req: dict):
        raise KeyError("invalid uid")


async def create_account_uc_override__success():
    repo = MockRepo()
    return AccountUseCase(repo)


async def create_account_uc_override__error():
    repo = MockRepoError()
    return AccountUseCase(repo)


async def test_create_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = (
        create_account_uc_override__success
    )
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.post("/api/v1/accounts/", json=req)
    assert res.status_code == 200
    assert res.json() == {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee", **req}


async def test_get_all_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = (
        create_account_uc_override__success
    )
    res = await testclient.get("/api/v1/accounts/")
    req = [
        {
            "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "email": "aaa@dot.com",
            "name": "my_name",
        }
    ]
    assert res.status_code == 200
    assert res.json() == {"count": len(req), "items": req}


async def test_get_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = (
        create_account_uc_override__success
    )
    uid = {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee"}
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.get(f"/api/v1/accounts/{uid}")
    assert res.status_code == 200
    assert res.json() == {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee", **req}


async def test_delete_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = (
        create_account_uc_override__success
    )
    uid = {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee"}
    res = await testclient.delete(f"/api/v1/accounts/{uid}")
    assert res.status_code == 200
    assert (
        res.json() == {"status": "OK"} if res == True else {"status": "Doesn't exist"}
    )


async def test_patch_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = (
        create_account_uc_override__success
    )
    uid = {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee"}
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.patch(f"/api/v1/accounts/{uid}", json=req)
    assert res.status_code == 200
    assert res.json() == "UPDATE 1"


async def test_put_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = (
        create_account_uc_override__success
    )
    uid = {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee"}
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.put(
        f"/api/v1/accounts/{uid}?email={req['email']}&name={req['name']}"
    )
    assert res.status_code == 200
    assert res.json() == "UPDATE 1"


async def test_create_account__email_busy(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.post("/api/v1/accounts/", json=req)
    assert res.status_code == 400
    assert res.json() == {"error": "email busy"}


async def test_get_account__invalid_uid(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "1234124"
    res = await testclient.get(f"/api/v1/accounts/{uid}")
    assert res.status_code == 404
    assert res.json() == {"error": "'invalid uid'"}


async def test_delete_account__invalid_uid(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "1234124"
    res = await testclient.delete(f"/api/v1/accounts/{uid}")
    assert res.status_code == 404
    assert res.json() == {"error": "'invalid uid'"}


async def test_putch_account__invalid_uid(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "1234124"
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.patch(f"/api/v1/accounts/{uid}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "'invalid uid'"}


async def test_put_account__invalid_uid(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "1234124"
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.put(
        f"/api/v1/accounts/{uid}?email={req['email']}&name={req['name']}"
    )
    assert res.status_code == 404
    assert res.json() == {"error": "'invalid uid'"}
