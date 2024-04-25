import pytest
from app.domain.accounts.deps import (
    create_account_uc,
    AccountUseCase,
)
from mock_pg_repo.mockrepo import MockRepo


pytestmark = pytest.mark.asyncio


async def create_account_uc_override__success():
    repo = MockRepo()
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
        res.json() == {"message": "account deleted"}
    )


async def test_patch_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = (
        create_account_uc_override__success
    )
    uid = {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee"}
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.patch(f"/api/v1/accounts/{uid}", json=req)
    assert res.status_code == 200
    assert res.json() == {
        "message": "updated",
        "new_data": {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee", **req}
    }


async def test_put_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = (
        create_account_uc_override__success
    )
    uid = {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee"}
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.put(f"/api/v1/accounts/{uid}", json=req)
    assert res.status_code == 200
    assert res.json() == {
        "message": "updated",
        "new_data": {"uid": "56986558-57f9-4117-a26f-05fa0cffe8ee", **req}
    }