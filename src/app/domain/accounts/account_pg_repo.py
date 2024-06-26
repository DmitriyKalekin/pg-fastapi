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
                self.dsn, min_size=1, max_size=2, max_inactive_connection_lifetime=500.0
            )
        yield self._pool

    async def create_account(self, acc: tuple) -> UUID:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                INSERT INTO accounts (
                    email
                    , name
                )
                VALUES ($1, $2)
                RETURNING uid;
            """
            try:
                uid = await conn.fetchval(q, *acc)
            except asyncpg.exceptions.UniqueViolationError:
                raise KeyError("email busy")
            return uid

    async def get_all_account(self) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT 
                    a.uid
                    , a.email
                    , a.name
                FROM accounts AS a
                LIMIT 100
            """
            accounts = await conn.fetch(q)
            return accounts

    async def get_account(self, uid: UUID) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT 
                    a.uid
                    , a.email
                    , a.name     
                FROM accounts AS a
                WHERE a.uid=($1)
            """

            try:
                account = await conn.fetchrow(q, uid)
            except asyncpg.exceptions.DataError:
                raise KeyError("invalid uid")

            if account is None:
                raise ValueError("account not found")

            return account

    async def delete_account(self, uid: UUID) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                DELETE
                FROM accounts AS a 
                WHERE a.uid=($1)
            """

            try:
                res = await conn.execute(q, uid)
            except asyncpg.exceptions.DataError:
                raise KeyError("invalid uid")

            if res == "DELETE 0":
                return {"message": "account not found"}
            else:
                return {"message": "account deleted"}

    async def update_account(self, uid: UUID, acc: tuple) -> UUID:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = f"""
                UPDATE accounts 
                SET (
                    email
                    , name
                ) = ($2, $3)
                WHERE uid=($1)
                RETURNING uid;
            """

            try:
                res = await conn.fetchval(q, uid, *acc)
            except asyncpg.exceptions.DataError:
                raise KeyError("invalid uid")

            if res is None:
                raise ValueError("account not found")

            return res
