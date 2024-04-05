from uuid import UUID


class IRepAccount:  # pragma: no cover
    async def create_account(self, acc: dict) -> UUID:
        raise NotImplementedError
    
    async def get_all_account(self, acc: dict) -> dict:
        raise NotImplementedError

    async def get_account_by_uid(self, acc: dict) -> dict:
        raise NotImplementedError
    
    async def update_account(self, acc: dict) -> dict:
        raise NotImplementedError
    
    async def delete_account(self, acc: dict) -> dict:
        raise NotImplementedError 