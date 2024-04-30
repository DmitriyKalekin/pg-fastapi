# do not remove
from app.domain.accounts.account_api import router as account_api
from app.domain.projects.project_api import router as project_api
from app.domain.issues.issues_api import router as issue_api

routers = [account_api, project_api, issue_api]


__all__ = [
    routers,
]
