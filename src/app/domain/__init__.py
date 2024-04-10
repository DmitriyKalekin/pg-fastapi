# do not remove 
from app.domain.accounts.account_api import router as account_api
from app.domain.projects.projects_api import router as project_api

routers = [
   account_api,
   project_api
]


__all__ = [
  routers,
]

