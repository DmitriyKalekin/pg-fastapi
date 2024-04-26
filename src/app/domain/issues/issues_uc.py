from .dto import *
from .issues_irep import IrepIssue

# --- Exceptions ---

class IssuesUseCase:
    def __init__(self, repo: IrepIssue):
        self._repo = repo

    # TODO: functions