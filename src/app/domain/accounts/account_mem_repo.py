from .account_irep import IRepAccount
from uuid import uuid4, UUID


class AccountMemRepo(IRepAccount):  # pragma: no cover
    def __init__(self):
        self._mem = {}

    async def create_account(self, acc: dict) -> UUID:
        print("mem repo works")
        uid = uuid4()
        self._mem[uid] = {"uid": uid, **acc}
        return uid
