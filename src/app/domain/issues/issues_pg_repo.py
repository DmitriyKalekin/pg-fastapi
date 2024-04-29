from .issues_irep import IRepIssue
from pydantic_settings import BaseSettings
from uuid import uuid4
import asyncpg
from contextlib import asynccontextmanager


class IssuesPgRepo(IRepIssue):  # pragma: no cover
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

    async def create_issue(self, req: tuple) -> list:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                INSERT INTO tasks (
                    summary
                    , description
                    , assignee_id
                    , status_id
                    , project_key
                    , project_id
                    , task_id
                )
                VALUES (
                    $1, $2, $3, $4, $5::text
                    , (
                        SELECT 
                            p.id
                        FROM projects as p
                        WHERE p.project_key=$5::text
                    )
                    , $6
                )
                RETURNING (
                    (SELECT uid FROM accounts WHERE uid=$3)
                    , (SELECT name FROM accounts WHERE uid=$3)
                    , (SELECT id FROM lib_status WHERE id=$4)
                    , (SELECT status FROM lib_status WHERE id=$4)
                    , task_id
                    , (SELECT project_key FROM projects WHERE project_key=$5::text)
                    , (SELECT name FROM projects WHERE project_key=$5::text)    
                )
            """
            his = """
                INSERT INTO tasks_history (
                    task_id
                    , project_key
                )
                SELECT 
                    task_id
                    , project_key
                FROM tasks
                WHERE task_id=$1
            """

            try:
                res = await conn.fetchval(q, *req, int(uuid4()) >> 92)
                if res != None:
                    await conn.execute(his, res[4])
            except asyncpg.exceptions.NotNullViolationError:
                raise ValueError("project not found")
            except asyncpg.exceptions.ForeignKeyViolationError:
                raise KeyError("account not found")
            return res

    async def get_all_issues(self) -> list[dict]:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT
                    (SELECT uid FROM accounts WHERE uid=t.assignee_id)
                    , (SELECT name FROM accounts WHERE uid=t.assignee_id)
                    , (SELECT id FROM lib_status WHERE id=t.status_id)
                    , (SELECT status FROM lib_status WHERE id=t.status_id)
                    , t.task_id
                    , (SELECT project_key FROM projects WHERE id=t.project_id)
                    , (SELECT name FROM projects WHERE id=t.project_id)
                    , t.summary
                    , t.description
                FROM tasks as t
                LIMIT 100
            """
            res = await conn.fetch(q)
            return res

    async def get_issue_by_id(self, req: int) -> list:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT 
                    (SELECT uid FROM accounts WHERE uid=t.assignee_id)
                    , (SELECT name FROM accounts WHERE uid=t.assignee_id)
                    , (SELECT id FROM lib_status WHERE id=t.status_id)
                    , (SELECT status FROM lib_status WHERE id=t.status_id)
                    , t.task_id
                    , (SELECT project_key FROM projects WHERE id=t.project_id)
                    , (SELECT name FROM projects WHERE id=t.project_id)
                    , t.summary
                    , t.description
                FROM tasks as t
                WHERE t.task_id=$1
                LIMIT 1
            """
            res = await conn.fetchrow(q, req)
            if res == None:
                raise KeyError("issue not found")
            return res

    async def get_issue_by_project(self, req: str) -> list:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                SELECT 
                    task_id
                FROM tasks_history
                WHERE project_key=$1
                LIMIT 1
            """
            res = await conn.fetchval(q, req)
            if res == None:
                raise KeyError("project not found")
            return await self.get_issue_by_id(res)

    async def update_issue(self, task_id: int, req: tuple) -> list:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                UPDATE tasks
                SET (
                    summary
                    , description
                    , assignee_id
                    , status_id
                    , project_key
                    , project_id
                ) = (
                    $1, $2, $3, $4, $5::text
                    , (
                        SELECT 
                            p.id
                        FROM projects as p
                        WHERE p.project_key=$5::text
                    )
                )
                WHERE id IN (
                    SELECT id
                    FROM tasks
                    WHERE task_id=$6
                    LIMIT 1
                )
                RETURNING (
                    (SELECT uid FROM accounts WHERE uid=$3)
                    , (SELECT name FROM accounts WHERE uid=$3)
                    , (SELECT id FROM lib_status WHERE id=$4)
                    , (SELECT status FROM lib_status WHERE id=$4)
                    , task_id
                    , (SELECT project_key FROM projects WHERE project_key=$5::text)
                    , (SELECT name FROM projects WHERE project_key=$5::text)   
                )
            """
            his = """
                INSERT INTO tasks_history (
                    task_id
                    , project_key
                )
                SELECT 
                    task_id
                    , project_key
                FROM tasks
                WHERE task_id=$1
            """

            try:
                res = await conn.fetchval(q, *req, task_id)
                if res == None:
                    raise KeyError("issue not found")
            except asyncpg.exceptions.NotNullViolationError:
                raise ValueError("project not found")
            except asyncpg.exceptions.ForeignKeyViolationError:
                raise KeyError("account not found")

            if res != None:
                await conn.execute(his, task_id)
            return res

    async def delete_issue(self, req: int) -> dict:
        async with self.pool as p, p.acquire() as cn:
            conn: asyncpg.Connection = cn
            q = """
                DELETE FROM tasks
                WHERE id = (
                    SELECT id
                    FROM tasks
                    WHERE task_id=$1
                    LIMIT 1
                )
            """
            his = """
                DELETE FROM tasks_history
                WHERE task_id=$1
            """
            res = await conn.execute(q, req)

            if res == "DELETE 0":
                raise KeyError("issue not found")
            else:
                await conn.execute(his, req)
                return {"message": "issue deleted"}
