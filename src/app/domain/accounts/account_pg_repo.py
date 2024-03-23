from .account_irep import IRepAccount
from uuid import uuid4, UUID
from pydantic_settings import BaseSettings
import asyncpg
from contextlib import asynccontextmanager


class AccountPgRepo(IRepAccount):  # pragma: no cover

    def __init__(self, cfg: BaseSettings):
        self.cfg = cfg
        self.dsn = "postgresql://{usr}:{pwd}@{host}:{port}/{db}".format(
            usr=self.cfg.POSTGRES_USER,
            pwd=self.cfg.POSTGRES_PASSWORD,
            host=self.cfg.POSTGRES_HOST,
            port=self.cfg.POSTGRES_PORT,
            db=self.cfg.POSTGRES_DBN,
        )
        self._pool = None

    @property
    @asynccontextmanager
    async def pool(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                self.dsn,
                min_size=1,
                max_size=2,
                max_inactive_connection_lifetime=500.0
            )
        yield self._pool

    async def create_account(self, acc: dict) -> UUID:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                INSERT INTO accounts (email, name)
                VALUES ($1, $2)
                RETURNING uid
            """
            try:
                uid = await conn.fetchval(q, acc["email"], acc["name"])
            except asyncpg.exceptions.UniqueViolationError:
                raise KeyError("email busy")
            return uid
