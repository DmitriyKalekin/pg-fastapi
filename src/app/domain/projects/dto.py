from pydantic import BaseModel, UUID4, ConfigDict


def convert_uuid_to_str(uuid) -> str:  # pragma: no cover
    return str(uuid)


class Error(BaseModel):
    error: str

    model_config = ConfigDict(json_schema_extra={"example": {"error": "some error"}})


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


class ProjectCreate(BaseModel):
    project_key: str = "name-num"
    name: str
    manager_id: UUID4

    model_config = ConfigDict(
        json_encoders={
            UUID4: convert_uuid_to_str,
        },
        json_schema_extra={
            "example": {
                "project_key": "name-num",
                "name": "name",
                "manager_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
            }
        },
    )


class Project(BaseModel):
    project_key: str
    name: str
    manager_id: Account = {}

    model_config = ConfigDict(
        json_encoders={
            UUID4: convert_uuid_to_str,
        },
        json_schema_extra={
            "example": {
                "project_key": "name-num",
                "name": "name",
                "manager_id": {
                    "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                    "name": "username",
                },
            }
        },
    )


class ProjectList(BaseModel):
    count: int
    items: list[Project] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 2,
                "items": [
                    {
                        "project_key": "name-num",
                        "name": "name",
                        "manager_id": {
                            "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                            "name": "username",
                        },
                    },
                    {
                        "project_key": "name-num",
                        "name": "name",
                        "manager_id": {
                            "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                            "name": "username",
                        },
                    },
                ],
            }
        }
    )


class UpdateProject(BaseModel):
    name: str
    manager_id: UUID4

    model_config = ConfigDict(
        json_encoders={UUID4: convert_uuid_to_str},
        json_schema_extra={
            "example": {
                "name": "name",
                "manager_id": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
            }
        },
    )


class UpdatedProject(BaseModel):
    message: str
    new_data: Project = {}

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "updated",
                "new_data": {
                    "project_key": "name-num",
                    "name": "name",
                    "manager_id": {
                        "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                        "name": "username",
                    },
                },
            }
        }
    )


class DeleteProject(BaseModel):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "deleted",
            }
        }
    )
