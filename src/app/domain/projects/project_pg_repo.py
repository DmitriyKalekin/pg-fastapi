from .project_irep import IRepProject
from pydantic_settings import BaseSettings
import asyncpg
from contextlib import asynccontextmanager


class ProjectPgRepo(IRepProject):  # pragma: no cover

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

    async def create_project(self, req: tuple) -> list:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                INSERT INTO projects (
                    project_key
                    , name
                    , manager_id
                )
                VALUES ($1, $2, $3)
                RETURNING (
                    SELECT (
                        uid
                        , name
                    )
                    FROM accounts 
                    WHERE uid=($3)
                )
            """
            try:
                res = await conn.fetchval(q, *req)
            except asyncpg.exceptions.ForeignKeyViolationError:
                raise KeyError("uid not found")
            return res

    async def get_all_project(self) -> list:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT 
                    p.project_key
                    , p.name
                    , a.uid
                    , a.name
                FROM projects AS p, accounts AS a
                WHERE a.uid = p.manager_id
                LIMIT 100
            """
            projects = await conn.fetch(q)
            return projects

    async def get_project(self, project_key: str) -> list:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT 
                    p.project_key
                    , p.name
                    , a.uid
                    , a.name
                FROM projects AS p, accounts AS a
                WHERE p.project_key=($1) AND a.uid = p.manager_id
            """
            project = await conn.fetchrow(q, project_key)
            if project is None:
                raise ValueError("key not found")
            return project

    async def update_project(self, project_key: str, req: tuple) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = f"""
                UPDATE projects
                SET (
                    name
                    , manager_id
                ) = ($2, $3)
                WHERE id in (
                    SELECT id
                    FROM projects
                    WHERE project_key=($1)
                    LIMIT 1
                )
                RETURNING (
                    SELECT (
                        uid
                        , name
                    )
                    FROM accounts
                    WHERE uid=($3)
                )
            """

            if await self.get_project(project_key) != None:
                try:
                    res = await conn.fetchval(q, project_key, *req)
                    return res
                except asyncpg.exceptions.ForeignKeyViolationError:
                    raise KeyError("uid not found")

    async def delete_project(self, project_key: str) -> bool:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = f"""
                DELETE 
                FROM projects 
                WHERE id in (
                    SELECT id
                    FROM projects
                    WHERE project_key=($1)
                    LIMIT 1
                )
            """

            res = await conn.execute(q, project_key)
            if res == "DELETE 0":
                raise KeyError("key not found")
            else:
                return {"message": "project deleted"}
