import pytest
from app.domain.issues.deps import deps_pg, IssuesUseCase
from .mock_pg_repo.mockrepo import MockRepo

pytestmark = pytest.mark.asyncio


async def deps_pg_override__success():
    repo = MockRepo()
    return IssuesUseCase(repo)


async def test_create_issue__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    req = {
        "summary": "title",
        "description": "description",
        "assignee_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status_id": 1,
        "project_key": "g-1",
    }
    res = await testclient.post("/api/v1/issues/", json=req)
    assert res.status_code == 200
    assert res.json() == {
        "summary": "title",
        "description": "description",
        "assignee": {
            "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "name": "my_name",
        },
        "status": {
            "id": 1,
            "status": "TODO",
        },
        "task_id": 1042382357,
        "project": {
            "project_key": "g-1",
            "name": "g",
        },
    }


async def test_get_all_issue__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    res = await testclient.get("/api/v1/issues/")
    assert res.status_code == 200
    assert res.json() == {
        "count": 1,
        "items": [
            {
                "summary": "title",
                "description": "description",
                "assignee": {
                    "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
                    "name": "my_name",
                },
                "status": {
                    "id": 1,
                    "status": "TODO",
                },
                "task_id": 1042382357,
                "project": {
                    "project_key": "g-1",
                    "name": "g",
                },
            }
        ],
    }


async def test_get_issue_by_id__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    issue_id = 1042382357
    res = await testclient.get(f"/api/v1/issues/{issue_id}")
    assert res.status_code == 200
    assert res.json() == {
        "summary": "title",
        "description": "description",
        "assignee": {
            "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "name": "my_name",
        },
        "status": {
            "id": 1,
            "status": "TODO",
        },
        "task_id": 1042382357,
        "project": {
            "project_key": "g-1",
            "name": "g",
        },
    }


async def test_get_issue_by_project__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    project_key = "g-1"
    res = await testclient.get(f"/api/v1/issues/project/{project_key}")
    assert res.status_code == 200
    assert res.json() == {
        "summary": "title",
        "description": "description",
        "assignee": {
            "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "name": "my_name",
        },
        "status": {
            "id": 1,
            "status": "TODO",
        },
        "task_id": 1042382357,
        "project": {
            "project_key": "g-1",
            "name": "g",
        },
    }


async def test_put_issue__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    issue_id = 1042382357
    req = {
        "summary": "title",
        "description": "description",
        "assignee_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status_id": 2,
        "project_key": "g-1",
    }
    res = await testclient.put(f"/api/v1/issues/{issue_id}", json=req)
    assert res.status_code == 200
    assert res.json() == {
        "message": "updated",
        "new_data": {
            "summary": "title",
            "description": "description",
            "assignee": {
                "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
                "name": "my_name",
            },
            "status": {
                "id": 2,
                "status": "InProgress",
            },
            "task_id": 1042382357,
            "project": {
                "project_key": "g-1",
                "name": "g",
            },
        },
    }


async def test_patch_issue__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    issue_id = 1042382357
    req = {
        "summary": "title",
        "description": "description",
        "assignee_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status_id": 2,
        "project_key": "g-1",
    }
    res = await testclient.patch(f"/api/v1/issues/{issue_id}", json=req)
    assert res.status_code == 200
    assert res.json() == {
        "message": "updated",
        "new_data": {
            "summary": "title",
            "description": "description",
            "assignee": {
                "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
                "name": "my_name",
            },
            "status": {
                "id": 2,
                "status": "InProgress",
            },
            "task_id": 1042382357,
            "project": {
                "project_key": "g-1",
                "name": "g",
            },
        },
    }


async def test_delete_issue__success(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__success
    issue_id = 1042382357
    res = await testclient.delete(f"/api/v1/issues/{issue_id}")
    assert res.status_code == 200
    assert res.json() == {"message": "issue deleted"}
