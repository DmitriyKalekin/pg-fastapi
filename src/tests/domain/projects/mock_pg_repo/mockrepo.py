from app.domain.projects.project_irep import IRepProject

class MockRepo(IRepProject):
    async def create_project(self, _: dict) -> dict:
        return "g"

    async def get_all_project(self) -> dict:
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