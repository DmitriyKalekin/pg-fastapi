from app.domain.projects.project_irep import IRepProject


class MockRepo(IRepProject):
    async def create_project(self, req: tuple) -> list:
        return ["56986558-57f9-4117-a26f-05fa0cffe8ee", "my_name"]

    async def get_all_project(self) -> dict:
        return [["g-1", "g", "56986558-57f9-4117-a26f-05fa0cffe8ee", "my_name"]]

    async def get_project(self, _: str) -> list:
        return [
            "g-1",
            "g",
            "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "my_name",
        ]

    async def update_project(self, _: str, req: tuple) -> list:
        return ["56986558-57f9-4117-a26f-05fa0cffe8ee", "my_name"]

    async def delete_project(self, _: str) -> dict:
        return {"message": "project deleted"}


class MockRepoError(IRepProject):
    async def create_project(self, _: dict) -> dict:
        raise KeyError("uid not found")

    async def get_project(self, _: str) -> dict:
        raise ValueError("key not found")

    async def update_project(self, key: str, req: dict) -> str:
        if key == "g-1":
            raise KeyError("uid not found")
        raise ValueError("key not found")

    async def delete_project(self, _: str) -> str:
        raise KeyError("key not found")
