from uuid import UUID


class IRepAccount:  # pragma: no cover
    async def create_account(self, acc: dict) -> UUID:
        raise NotImplementedError
