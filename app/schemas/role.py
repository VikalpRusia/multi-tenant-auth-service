from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    model_config = ConfigDict(from_attributes=True)


class Role(RoleBase):
    id: int
    model_config: ConfigDict = ConfigDict(from_attributes=True)
