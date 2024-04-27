import pytest
from app.domain.projects.deps import deps_pg, ProjectUseCase, KeyNotFound, UidNotFound
from .mock_pg_repo.mockrepo import MockRepoError

pytestmark = pytest.mark.asyncio


async def deps_pg_override__error():
    repo = MockRepoError()
    return ProjectUseCase(repo)


async def test_create_project__uid_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    req = {
        "name": "g",
        "manager_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
        "status": 1,
    }
    res = await testclient.post("/api/v1/projects/", json=req)
    assert res.status_code == 422
    assert res.json() == {"error": "uid not found"}


async def test_get_project__key_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "123"
    res = await testclient.get(f"/api/v1/projects/{project_key}")
    assert res.status_code == 404
    assert res.json() == {"error": "key not found"}


async def test_patch_project__key_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "123"
    req = {
        "name": "b",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": 1,
    }
    res = await testclient.patch(f"/api/v1/projects/{project_key}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "key not found"}

async def test_patch_project__uid_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "g-1"
    req = {
        "name": "b",
        "manager_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
        "status": 1,
    }
    res = await testclient.patch(f"/api/v1/projects/{project_key}", json=req)
    assert res.status_code == 422
    assert res.json() == {"error": "uid not found"}



async def test_put_project__key_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "123"
    req = {
        "name": "b",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": 1,
    }
    res = await testclient.put(f"/api/v1/projects/{project_key}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "key not found"}

async def test_put_project__uid_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "g-1"
    req = {
        "name": "b",
        "manager_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
        "status": 1,
    }
    res = await testclient.put(f"/api/v1/projects/{project_key}", json=req)
    assert res.status_code == 422
    assert res.json() == {"error": "uid not found"}


async def test_delete_project__key_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "123"
    res = await testclient.delete(f"/api/v1/projects/{project_key}")
    assert res.status_code == 404
    assert res.json() == {"error": "key not found"}
