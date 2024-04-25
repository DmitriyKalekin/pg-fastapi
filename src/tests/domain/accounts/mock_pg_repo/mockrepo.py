from uuid import UUID
from app.domain.accounts.account_irep import IRepAccount


class MockRepo(IRepAccount):
    async def create_account(self, _: dict):
        return "56986558-57f9-4117-a26f-05fa0cffe8ee"

    async def get_all_account(self):
        return [
            {
                "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
                "email": "aaa@dot.com",
                "name": "my_name",
            }
        ]

    async def get_account(self, _: str):
        return {
            "uid": "56986558-57f9-4117-a26f-05fa0cffe8ee",
            "email": "aaa@dot.com",
            "name": "my_name",
        }

    async def delete_account(self, _: str):
        return {"message": "account deleted"}

    async def update_account(self, _: UUID, req: tuple):
        return "56986558-57f9-4117-a26f-05fa0cffe8ee"


class MockRepoError(IRepAccount):
    async def create_account(self, _: dict):
        raise KeyError("email busy")

    async def get_account(self, uid: str):
        if uid == "1234124":
            raise KeyError("invalid uid")
        raise ValueError("account not found")

    async def delete_account(self, _: str):
        raise KeyError("invalid uid")

    async def update_account(self, uid: UUID, req: tuple):
        if uid == "1234124":
            raise KeyError("invalid uid")
        raise ValueError("account not found")
