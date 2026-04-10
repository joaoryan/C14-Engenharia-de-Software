from pydantic import BaseModel, ConfigDict

class DietBase(BaseModel):
    name: str
    description: str

class DietCreate(DietBase):
    pass

class DietUpdate(DietBase):
    pass

class DietResponse(DietBase):
    id: int

    model_config = ConfigDict(from_attributes=True)