import pytest
from app.domain.issues.deps import deps_pg, IssuesUseCase, IssueNotFound, AccountNotFound, ProjectNotFound
from .mock_pg_repo.mockrepo import MockRepoError

pytestmark = pytest.mark.asyncio

async def deps_pg_override__error():
    repo = MockRepoError()
    return IssuesUseCase(repo)

async def test_create_issue__account_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    req = {
        "summary": "title", 
        "description": "description",
        "assignee_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
        "status_id": 1,
        "project_key": "g-1",
    }
    res = await testclient.post("/api/v1/issues/", json=req)
    assert res.status_code == 422
    assert res.json() == {"error": "account not found"}

async def test_create_issue__project_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    req = {
        "summary": "title", 
        "description": "description",
        "assignee_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status_id": 1,
        "project_key": "1234124",
    }
    res = await testclient.post("/api/v1/issues/", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "project not found"}

async def test_get_issue_by_id__issue_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    issue_id = 1234124
    res = await testclient.get(f"/api/v1/issues/{issue_id}")
    assert res.status_code == 404
    assert res.json() == {"error": "issue not found"}

async def test_get_issue_by_project__project_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    project_key = "1234124"
    res = await testclient.get(f"/api/v1/issues/project/{project_key}")
    assert res.status_code == 404
    assert res.json() == {"error": "project not found"}

async def test_put_issue__issue_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    issue_id = 1234124
    req = {
        "summary": "title", 
        "description": "description",
        "assignee_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status_id": 1,
        "project_key": "g-1",
    }
    res = await testclient.put(f"/api/v1/issues/{issue_id}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "issue not found"}

async def test_put_issue__project_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    issue_id = 124564
    req = {
        "summary": "title", 
        "description": "description",
        "assignee_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status_id": 1,
        "project_key": "1234124",
    }
    res = await testclient.put(f"/api/v1/issues/{issue_id}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "project not found"}

async def test_put_issue__account_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    issue_id = 124564
    req = {
        "summary": "title", 
        "description": "description",
        "assignee_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
        "status_id": 1,
        "project_key": "g-1",
    }
    res = await testclient.put(f"/api/v1/issues/{issue_id}", json=req)
    assert res.status_code == 422
    assert res.json() == {"error": "account not found"}


async def test_patch_issue__issue_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    issue_id = 1234124
    req = {
        "summary": "title", 
        "description": "description",
        "assignee_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status_id": 1,
        "project_key": "g-1",
    }
    res = await testclient.patch(f"/api/v1/issues/{issue_id}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "issue not found"}

async def test_patch_issue__project_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    issue_id = 124564
    req = {
        "summary": "title", 
        "description": "description",
        "assignee_id": "56986558-57f9-4117-a26f-05fa0cffe8ee",
        "status_id": 1,
        "project_key": "1234124",
    }
    res = await testclient.patch(f"/api/v1/issues/{issue_id}", json=req)
    assert res.status_code == 404
    assert res.json() == {"error": "project not found"}

async def test_patch_issue__account_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    issue_id = 124564
    req = {
        "summary": "title", 
        "description": "description",
        "assignee_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
        "status_id": 1,
        "project_key": "g-1",
    }
    res = await testclient.patch(f"/api/v1/issues/{issue_id}", json=req)
    assert res.status_code == 422
    assert res.json() == {"error": "account not found"}

async def test_delete_issue__issue_not_found(testclient, api_app):
    api_app.dependency_overrides[deps_pg] = deps_pg_override__error
    issue_id = 1234124
    res = await testclient.delete(f"/api/v1/issues/{issue_id}")
    assert res.status_code == 404
    assert res.json() == {"error": "issue not found"}