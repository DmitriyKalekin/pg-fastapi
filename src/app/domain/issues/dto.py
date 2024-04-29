from pydantic import BaseModel, UUID4, ConfigDict


def convert_uuid_to_str(uuid) -> str:  # pragma: no cover
    return str(uuid)


class Error(BaseModel):
    error: str

    model_config = ConfigDict(json_schema_extra={"example": {"error": "some error"}})


class Project(BaseModel):
    name: str
    project_key: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "name",
                "project_key": "name-num",
            }
        }
    )


class Account(BaseModel):
    uid: UUID4
    name: str

    model_config = ConfigDict(
        json_encoders={
            UUID4: convert_uuid_to_str,
        },
        json_schema_extra={
            "example": {
                "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                "name": "username",
            }
        },
    )


class Status(BaseModel):
    id: int
    status: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"id": 1, "status": "TODO"}}
    )


class CreateIssue(BaseModel):
    summary: str
    description: str
    assignee_id: UUID4
    status_id: int = 1
    project_key: str

    model_config = ConfigDict(
        json_encoders={
            UUID4: convert_uuid_to_str,
        },
        json_schema_extra={
            "example": {
                "summary": "title",
                "description": "description" or "",
                "assignee_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                "status_id": 1,
                "project_key": "name-num",
            }
        },
    )


class Issue(BaseModel):
    summary: str
    description: str
    assignee: Account = {}
    status: Status = {}
    task_id: int
    project: Project = {}

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "summary": "title",
                "description": "description" or "",
                "assignee": {
                    "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                    "name": "username",
                },
                "status": {"id": 1, "status": "TODO"},
                "task_id": 1,
                "project": {"project_key": "name-num", "name": "name"},
            }
        }
    )


class IssueList(BaseModel):
    count: int
    items: list[Issue] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 1,
                "items": [
                    {
                        "summary": "title",
                        "description": "description" or "",
                        "assignee": {
                            "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                            "name": "username",
                        },
                        "status": {"id": 1, "status": "TODO"},
                        "task_id": 1,
                        "project": {"project_key": "name-num", "name": "name"},
                    }
                ],
            }
        }
    )


class UpdateIssue(BaseModel):
    message: str
    new_data: Issue = {}

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "updated",
                "new_data": {
                    "summary": "title",
                    "description": "description" or "",
                    "assignee": {
                        "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                        "name": "username",
                    },
                    "status": {"id": 1, "status": "TODO"},
                    "task_id": 1,
                    "project": {"project_key": "name-num", "name": "name"},
                },
            }
        }
    )


class DeleteIssue(BaseModel):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "deleted",
            }
        }
    )
