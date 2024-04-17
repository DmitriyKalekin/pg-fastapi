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

    async def create_project(self, project: dict) -> UUID: pass

    async def get_all_project(self) -> dict: pass

    async def get_project(self, project: dict) -> dict: pass

    async def update_project(self, project: dict) -> dict: pass

    async def delete_project(self, project: dict) -> bool: pass