import pytest
from app.domain.accounts.deps import (
    create_account_uc,
    AccountUseCase,
    EmailBusyException,
    InvalidUidException,
    AccountNotFoundException,
)
from mock_pg_repo.mockrepo import MockRepoError

pytestmark = pytest.mark.asyncio

async def create_account_uc_override__error():
    repo = MockRepoError()
    return AccountUseCase(repo)

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
    assert res.status_code == 422
    assert res.json() == {"error": "invalid uid"}


async def test_delete_account__invalid_uid(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "1234124"
    res = await testclient.delete(f"/api/v1/accounts/{uid}")
    assert res.status_code == 422
    assert res.json() == {"error": "invalid uid"}


async def test_putch_account__invalid_uid(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "1234124"
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.patch(f"/api/v1/accounts/{uid}", json=req)
    assert res.status_code == 422
    assert res.json() == {"error": "invalid uid"}


async def test_put_account__invalid_uid(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "1234124"
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.put(f"/api/v1/accounts/{uid}", json=req)
    assert res.status_code == 422
    assert res.json() == {"error": "invalid uid"}


async def test_get_account__account_not_found(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "da909063-1246-42ae-b4f1-4a64203eca2c"
    res = await testclient.get(f"/api/v1/accounts/{uid}")
    assert res.status_code == 404
    assert res.json() == {"error": "account not found"}

async def test_putch_account__account_not_found(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "da909063-1246-42ae-b4f1-4a64203eca2c"
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.patch(f"/api/v1/accounts/{uid}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "account not found"}


async def test_put_account__account_not_found(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    uid = "da909063-1246-42ae-b4f1-4a64203eca2c"
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.put(f"/api/v1/accounts/{uid}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "account not found"}
