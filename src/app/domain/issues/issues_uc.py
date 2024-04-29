from .dto import (
    Account,
    Project,
    Status,
    Issue,
    IssueList,
    CreateIssue,
    DeleteIssue,
    UpdateIssue,
)
from .issues_irep import IRepIssue

# --- Exceptions ---
class ProjectNotFound(Exception):
    pass

class AccountNotFound(Exception):
    pass

class IssueNotFound(Exception):
    pass

class IssuesUseCase:
    def __init__(self, repo: IRepIssue):
        self._repo = repo

    async def create_issue(self, req: CreateIssue) -> Issue:
        req_dict = req.model_dump()
        try:
            res = await self._repo.create_issue(tuple(req_dict.values()))
        except ValueError:
            raise ProjectNotFound("project not found")
        except KeyError:
            raise AccountNotFound("account not found")
             
        return Issue(
            summary=req_dict.get('summary'),
            description=req_dict.get('description'),
            assignee= Account(
                uid=res[0],
                name=res[1]
            ),
            status= Status(
                id=res[2],
                status=res[3]
            ),
            task_id=res[4],
            project= Project(
                project_key=res[5],
                name=res[6]
            )
        )
    
    async def get_all_issues(self) -> IssueList:
        issues = await self._repo.get_all_issues()
        items = [
            Issue(
                summary=el[7],
                description=el[8],
                assignee= Account(
                    uid=el[0],
                    name=el[1]
                ),
                status= Status(
                    id=el[2],
                    status=el[3]
                ),
                task_id=el[4],
                project= Project(
                    project_key=el[5],
                    name=el[6]
                )
            )
            for el in issues
        ]
        return IssueList(count=len(issues), items=items)

    async def get_issue_by_id(self, req: str) -> Issue:
        try:
            res = await self._repo.get_issue_by_id(int(req))
        except KeyError:
            raise IssueNotFound("issue not found")
        return Issue(
            summary=res[7],
            description=res[8],
            assignee= Account(
                uid=res[0],
                name=res[1]
            ),
            status= Status(
                id=res[2],
                status=res[3]
            ),
            task_id=res[4],
            project= Project(
                project_key=res[5],
                name=res[6]
            )
        )
    
    async def get_issue_by_project(self, req: str) -> Issue:
        try:
            res = await self._repo.get_issue_by_project(req)
        except KeyError:
            raise ProjectNotFound("project not found")
        return Issue(
            summary=res[7],
            description=res[8],
            assignee= Account(
                uid=res[0],
                name=res[1]
            ),
            status= Status(
                id=res[2],
                status=res[3]
            ),
            task_id=res[4],
            project= Project(
                project_key=res[5],
                name=res[6]
            )
        )
    
    async def put_issue(self, task_id: str, req: CreateIssue) -> Issue:
        req_dict = req.model_dump()
        try:
            res = await self._repo.update_issue(int(task_id), tuple(req_dict.values()))
        except ValueError:
            raise ProjectNotFound("project not found") 
        except KeyError as e:
            if str(e) == "'issue not found'":
                raise IssueNotFound("issue not found")
            raise AccountNotFound("account not found") 
        
        return UpdateIssue(
            message="updated",
            new_data= Issue(
                summary=req_dict.get('summary'),
                description=req_dict.get('description'),
                assignee= Account(
                    uid=res[0],
                    name=res[1]
                ),
                status= Status(
                    id=res[2],
                    status=res[3]
                ),
                task_id=res[4],
                project= Project(
                    project_key=res[5],
                    name=res[6]
                )
            )
        )

    async def patch_issue(self, task_id: str, req: CreateIssue) -> Issue:
        req_dict = req.model_dump()
        try:
            res = await self._repo.update_issue(int(task_id), tuple(req_dict.values()))
        except ValueError:
            raise ProjectNotFound("project not found") 
        except KeyError as e:
            if str(e) == "'issue not found'":
                raise IssueNotFound("issue not found")
            raise AccountNotFound("account not found") 
        
        return UpdateIssue(
            message="updated",
            new_data= Issue(
                summary=req_dict.get('summary'),
                description=req_dict.get('description'),
                assignee= Account(
                    uid=res[0],
                    name=res[1]
                ),
                status= Status(
                    id=res[2],
                    status=res[3]
                ),
                task_id=res[4],
                project= Project(
                    project_key=res[5],
                    name=res[6]
                )
            )
        )

    async def delete_issue(self, req: str) -> dict:
        try:
            res = await self._repo.delete_issue(int(req))
        except KeyError:
            raise IssueNotFound("issue not found")
        return DeleteIssue(**res)
    