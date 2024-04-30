from app.domain.issues.issues_irep import IRepIssue


class MockRepo(IRepIssue):

    async def create_issue(self, req: dict) -> list:
        return [
            "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "my_name",
            1,
            "TODO",
            1042382357,
            "g-1",
            "g",
        ]

    async def get_all_issues(self) -> list[dict]:
        return [
            [
                "56986558-57f9-4117-a26f-05fa0cffe8ee",
                "my_name",
                1,
                "TODO",
                1042382357,
                "g-1",
                "g",
                "title",
                "description",
            ]
        ]

    async def get_issue_by_id(self, req: int) -> list:
        return [
            "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "my_name",
            1,
            "TODO",
            1042382357,
            "g-1",
            "g",
            "title",
            "description",
        ]

    async def get_issue_by_project(self, req: int) -> list:
        return [
            "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "my_name",
            1,
            "TODO",
            1042382357,
            "g-1",
            "g",
            "title",
            "description",
        ]

    async def update_issue(self, task_id: int, req: dict) -> list:
        return [
            "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "my_name",
            2,
            "InProgress",
            1042382357,
            "g-1",
            "g",
        ]

    async def delete_issue(self, req: int) -> dict:
        return {"message": "issue deleted"}


class MockRepoError(IRepIssue):
    async def create_issue(self, req: tuple) -> list:
        if req[4] == "1234124":
            raise ValueError("project not found")
        raise KeyError("account not found")

    async def get_issue_by_id(self, req: int) -> list:
        raise KeyError("issue not found")

    async def get_issue_by_project(self, req: int) -> list:
        raise KeyError("project not found")

    async def update_issue(self, task_id: int, req: dict) -> dict:
        if task_id == 1234124:
            raise KeyError("issue not found")
        if req[4] == "1234124":
            raise ValueError("project not found")
        raise KeyError("account not found")

    async def delete_issue(self, req: int) -> dict:
        raise KeyError("issue not found")
