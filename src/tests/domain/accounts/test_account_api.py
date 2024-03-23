import pytest
from app.domain.accounts.deps import create_account_uc, AccountUseCase, EmailBusyException
from app.domain.accounts.account_irep import IRepAccount

pytestmark = pytest.mark.asyncio


class MockRepo(IRepAccount):
    async def create_account(self, _: dict):
        return "56986558-57f9-4117-a26f-05fa0cffe8ee"


class MockRepoError(IRepAccount):
    async def create_account(self, _: dict):
        raise KeyError("email busy")


async def create_account_uc_override__success():
    repo = MockRepo()
    return AccountUseCase(repo)


async def create_account_uc_override__error():
    repo = MockRepoError()
    return AccountUseCase(repo)


async def test_create_account__success(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__success
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.post("/api/v1/accounts/", json=req)
    assert res.status_code == 200
    assert res.json() == {
        "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        **req
    }


async def test_create_account__email_busy(testclient, api_app):
    api_app.dependency_overrides[create_account_uc] = create_account_uc_override__error
    req = {"email": "aaa@dot.com", "name": "my_name"}
    res = await testclient.post("/api/v1/accounts/", json=req)
    assert res.status_code == 400
    assert res.json() == {
        "error": "email busy"
    }
