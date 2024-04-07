from uuid import UUID


class IRepAccount:  # pragma: no cover
    async def create_account(self, acc: dict) -> UUID:
        raise NotImplementedError

    async def get_all_account(self) -> dict:
        raise NotImplementedError

    async def get_account(self, uid: UUID) -> dict:
        raise NotImplementedError

    async def update_account(self, uid: UUID, acc: dict) -> dict:
        raise NotImplementedError

    async def delete_account(self, uid: UUID) -> bool:
        raise NotImplementedError
