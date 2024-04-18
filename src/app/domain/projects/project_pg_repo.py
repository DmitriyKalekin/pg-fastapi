from .project_irep import IRepProject
from uuid import uuid4, UUID
from pydantic_settings import BaseSettings
import asyncpg
from contextlib import asynccontextmanager

class ProjectPgRepo(IRepProject): #pragma: no cover

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

    async def create_project(self, project_key: str, req: dict) -> dict: 
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                INSERT INTO projects (project_key, name, manager_id, status_id)
                VALUES ($1, $2, $3, $4)
                RETURNING project_key
            """
            res = await conn.fetchval(q, project_key, req["name"], req["manager_id"], req["status_id"])
            return res

    async def get_all_project(self) -> dict: 
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT *
                FROM projects
            """
            projects = await conn.fetch(q)
            return projects

    async def get_project(self, req: dict) -> dict: 
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT * FROM projects WHERE project_key=($1)
            """

            try:
                project = await conn.fetchrow(q, req["project_key"])
            except asyncpg.exceptions.DataError:
                raise KeyError("invalid key")
            return project

    async def update_project(self, req: dict) -> dict: 
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = f"""
                UPDATE projects
                SET name=($2), manager_id=($3)
                WHERE project_key=($1)
            """

            try:
                res = await conn.execute(q, req["project_key"], req["name"], req["manager_id"])
            except asyncpg.exceptions.DataError:
                raise KeyError("invalid key")
            return res

    async def delete_project(self, req: dict) -> bool: 
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = f"""
                DELETE FROM projects WHERE project_key=($1)
            """

            try:
                res = await conn.execute(q, req["project_key"])
            except asyncpg.exceptions.DataError:
                raise KeyError("invalid key")
            return res