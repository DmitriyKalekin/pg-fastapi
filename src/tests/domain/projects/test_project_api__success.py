import pytest
from app.domain.projects.deps import deps_pg, ProjectUseCase
from mock_pg_repo.mockrepo import MockRepo

pytestmark = pytest.mark.asyncio





async def deps_pg_override__success():
    repo = MockRepo()
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
