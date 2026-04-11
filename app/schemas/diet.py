from typing import Optional

from pydantic import BaseModel, ConfigDict


class DietBase(BaseModel):
    name: str
    description: str


class DietCreate(DietBase):
    user_id: Optional[int] = None


class DietUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None


class DietResponse(DietBase):
    id: int
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)