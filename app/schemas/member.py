from typing import Optional

from pydantic import BaseModel, ConfigDict


class MemberBase(BaseModel):
    org_id: int
    user_id: int
    role_id: int
    status: int = 0
    settings: Optional[dict] = {}


class Member(MemberBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MemberCreate(MemberBase):
    model_config = ConfigDict(from_attributes=True)
