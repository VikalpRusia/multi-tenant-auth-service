from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrganizationBase(BaseModel):
    name: str
    status: int = 0
    personal: Optional[bool] = False
    settings: Optional[dict] = {}


class Organization(OrganizationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OrganizationCreate(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)
