from app.domain.projects.project_irep import IRepProject

class sample: 
    async def create_project(self, req: tuple) -> list:
        return ["56986558-57f9-4117-a26f-05fa0cffe8ee", "my_name"]

    async def get_all_project(self) -> dict:
        return [
            {
                "project_key": "g-1",
                "name": "g",
                "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
                "name": "my_name",
            }
        ]

    async def get_project(self, _: str) -> list:
        return [
            {
                "project_key": "g-1",
                "name": "g",
                "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
                "name": "my_name",
            }
        ]

    async def update_project(self, _: str, req: tuple) -> list:
        return ["56986558-57f9-4117-a26f-05fa0cffe8ee", "my_name"]

    async def delete_project(self, _: str) -> dict:
        return {"message": "project deleted"}

class MockRepo(IRepProject):
    async def create_project(self, req: dict) -> dict:
        return ["56986558-57f9-4117-a26f-05fa0cffe8ee", "my_name"]

    # async def get_all_project(self) -> dict:
    #     raise NotImplementedError

    # async def get_project(self, project_key: str) -> dict:
    #     raise NotImplementedError

    # async def update_project(self, project_key: str, req: dict) -> dict:
    #     raise NotImplementedError

    # async def delete_project(self, project_key: str) -> dict:
    #     raise NotImplementedError

    


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
