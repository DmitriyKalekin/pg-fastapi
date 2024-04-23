from .project_irep import IRepProject
from uuid import uuid4, UUID
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

    async def create_project(self, req: dict) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                INSERT INTO projects (project_key, name, manager_id, status_id)
                VALUES ($1, $2, $3, $4)
                RETURNING name
            """
            try:
                res = await conn.fetchval(
                    q,
                    req["project_key"],
                    req["project_key"][: req["project_key"].find("-")],
                    req["manager_id"],
                    req["status"],
                )
            except asyncpg.exceptions.UniqueViolationError:
                raise KeyError("key busy")
            return res

    async def get_all_project(self) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT 
                    projects.project_key,
                    projects.name,
                    projects.manager_id,
                    lib_status.status
                FROM projects
                INNER JOIN lib_status ON projects.status_id=lib_status.id
            """
            projects = await conn.fetch(q)
            return projects

    async def get_project(self, project_key: str) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT 
                    projects.project_key,
                    projects.name,
                    projects.manager_id,
                    lib_status.status
                FROM projects
                INNER JOIN lib_status ON projects.status_id=lib_status.id
                WHERE project_key=($1)
            """

            project = await conn.fetchrow(q, project_key)
            if project is None:
                raise KeyError("key not found")
            return project

    async def update_project(self, project_key: str, req: dict) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = f"""
                UPDATE projects
                SET name=($2), manager_id=($3), status_id=($4)
                WHERE project_key=($1)
            """

            if await self.get_project(project_key) is None:
                raise KeyError("key not found")
            else:
                res = await conn.execute(
                    q, project_key, req["name"], req["manager_id"], req["status"]
                )
                return res

    async def delete_project(self, project_key: str) -> bool:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = f"""
                DELETE FROM projects WHERE project_key=($1)
            """

            check = """
                SELECT * FROM projects WHERE project_key=($1)
            """
            try:
                if await conn.fetchval(check, project_key) is None:
                    raise KeyError("invalid key")
            finally:
                res = await conn.execute(q, project_key)
            return res
