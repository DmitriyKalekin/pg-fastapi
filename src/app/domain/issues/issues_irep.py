class IRepIssue:  # pragma: no cover
    async def create_issue(self, req: dict) -> dict:
        raise NotImplementedError

    async def get_all_issues(self) -> dict:
        raise NotImplementedError

    async def get_issue_by_id(self, req: int) -> dict:
        raise NotImplementedError

    async def get_issue_by_project(self, req: str) -> dict:
        raise NotImplementedError

    async def update_issue(self, task_id: int, req: dict) -> dict:
        raise NotImplementedError

    async def delete_issue(self, req: int) -> dict:
        raise NotImplementedError
