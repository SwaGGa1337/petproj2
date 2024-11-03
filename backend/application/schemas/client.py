from typing import Any
import re

from fastapi import HTTPException
from pydantic import BaseModel, validator, ConfigDict


class SClientAdd(BaseModel):
    name: str
    email: str

    @validator("email")
    def validate_email(cls, value: str) -> Any:
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value):
            return value
        else:
            raise HTTPException(
                status_code=400, detail="Неверный формат адреса электронной почты"
            )


class SClient(SClientAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SClientId(BaseModel):
    ok: bool = True
    client_id: int
