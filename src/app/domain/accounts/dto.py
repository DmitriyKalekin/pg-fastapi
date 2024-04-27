from pydantic import BaseModel, EmailStr, UUID4, ConfigDict
from pydantic.fields import Field

def convert_uuid_to_str(uuid) -> str: # pragma: no cover
    return str(uuid)

class Error(BaseModel):
    error: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "some error"
            }
        }
    )

class AccountCreate(BaseModel):
    email: EmailStr
    name: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "aaa@example.com",
                "name": "username"
            }
        }
    )

class Account(AccountCreate):
    uid: UUID4

    model_config = ConfigDict(
        json_encoders={
            UUID4: convert_uuid_to_str,
        },
        json_schema_extra={
            "example": {
                "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                "email": "aaa@example.com",
                "name": "username"
            }
        }
    )

class AccountList(BaseModel):
    count: int
    items: list[Account] = []

    model_config = ConfigDict(
        json_encoders={
            UUID4: convert_uuid_to_str,
        },
        json_schema_extra={
            "example": {
                "count": 2,
                "items": [
                    {
                        "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                        "email": "aaa@example.com",
                        "name": "username"
                    },
                    {
                        "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                        "email": "aaa@example.com",
                        "name": "username"
                    }
                ]
            }
        }

    )

class UpdateAccount(BaseModel):
    message: str
    new_data: Account = {}

    model_config = ConfigDict(
        json_encoders={
            UUID4: convert_uuid_to_str
        },
        json_schema_extra={
            "example": {
                "message": "updated",
                "new_data": {
                    "uid": "dcaf7bbd-35f6-4ea6-bd2a-c1be8d8ab218",
                    "email": "aaa@example.com",
                    "name": "username"
                }
            }
        }
    )

class DeleteAccount(BaseModel):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "deleted",
            }
        }
    )