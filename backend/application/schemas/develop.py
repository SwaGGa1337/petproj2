from typing import Optional
from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile, File


class SDevelopAdd(BaseModel):
    firstName: str
    lastName: Optional[str] = None
    aboutDevelop: Optional[str] = None
    description: Optional[str] = None


class SDevelop(SDevelopAdd):
    id: int

    photo: Optional[UploadFile] = File(None)
    model_config = ConfigDict(from_attributes=True)


class SDevelopId(BaseModel):
    ok: bool = True
    develop_id: int
