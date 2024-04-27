import pytest
from app.domain.projects.deps import deps_pg, ProjectUseCase
from app.domain.projects.project_irep import IRepProject

pytestmark = pytest.mark.asyncio


class MockRepo(IRepProject):
    async def create_project(self, _: dict) -> dict:
        return "g"

    async def get_all_project(self) -> list[dict]:
        return [
            {
                "project_key": "g-1",
                "name": "g",
                "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
                "status": "TODO",
            }
        ]

    async def get_project(self, _: str) -> dict:
        return {
            "project_key": "g-1",
            "name": "g",
            "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "status": "TODO",
        }

    async def update_project(self, _: str, req: dict) -> dict:
        return "UPDATE 1"

    async def delete_project(self, _: str) -> dict:
        return "DELETE 1"


class MockRepoError(IRepProject):
    async def create_project(self, _: dict) -> dict:
        raise KeyError("key busy")

    async def get_project(self, _: str) -> dict:
        raise KeyError("key not found")

    async def update_project(self, _: str, req: dict) -> str:
        raise KeyError("key not found")

    async def delete_project(self, _: str) -> str:
        raise KeyError("invalid key")


async def deps_pg_override__success():
    repo = MockRepo()
    return ProjectUseCase(repo)


async def deps_pg_override__error():
    repo = MockRepoError()
    return ProjectUseCase(repo)


async def test_create_project__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    req = {
        "project_key": "g-1",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": 1,
    }
    res = await testclient.post("/api/v1/projects/", json=req)
    assert res.status_code == 200
    assert res.json() == {
        "project_key": "g-1",
        "name": "g",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": 1,
    }


async def test_get_all_project__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    res = await testclient.get("/api/v1/projects/")
    req = [
        {
            "project_key": "g-1",
            "name": "g",
            "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "status": "TODO",
        }
    ]
    assert res.status_code == 200
    assert res.json() == {"count": len(req), "items": req}


async def test_get_project__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    project_key = "g-1"
    res = await testclient.get(f"/api/v1/projects/{project_key}")
    assert res.status_code == 200
    assert res.json() == {
        "project_key": "g-1",
        "name": "g",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": "TODO",
    }


async def test_patch_project__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    project_key = "g-1"
    req = {
        "name": "b",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": 1,
    }
    res = await testclient.patch(f"/api/v1/projects/{project_key}", json=req)
    assert res.status_code == 200
    assert res.json() == {"message": "UPDATE 1"}


async def test_put_project__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    project_key = "g-1"
    req = {
        "name": "b",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": 1,
    }
    res = await testclient.put(
        f"/api/v1/projects/{project_key}?name={req['name']}&manager_id={req['manager_id']}&status_id={req['status']}"
    )
    assert res.status_code == 200
    assert res.json() == {"message": "UPDATE 1"}


async def test_delete_project__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    project_key = "g-1"
    res = await testclient.delete(f"/api/v1/projects/{project_key}")
    assert res.status_code == 200
    assert res.json() == {"message": "DELETE 1"}


async def test_create_project__key_busy(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    req = {
        "name": "g",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": 1,
    }
    res = await testclient.post("/api/v1/projects/", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "'key busy'"}


async def test_get_project__key_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "123"
    res = await testclient.get(f"/api/v1/projects/{project_key}")
    assert res.status_code == 404
    assert res.json() == {"error": "'key not found'"}


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
    assert res.json() == {"error": "'key not found'"}


async def test_put_project__key_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "123"
    req = {
        "name": "b",
        "manager_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status": 1,
    }
    res = await testclient.put(
        f"/api/v1/projects/{project_key}?name={req['name']}&manager_id={req['manager_id']}&status_id={req['status']}"
    )
    assert res.status_code == 404
    assert res.json() == {"error": "'key not found'"}


async def test_delete_project__invalid_key(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "123"
    res = await testclient.delete(f"/api/v1/projects/{project_key}")
    assert res.status_code == 404
    assert res.json() == {"error": "'invalid key'"}
