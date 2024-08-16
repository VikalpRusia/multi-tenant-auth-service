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
    role_id: int = 1
    model_config = ConfigDict(from_attributes=True)


class UpdateMember(BaseModel):
    org_id: Optional[int]
    user_id: Optional[int]
    role_id: Optional[int]
    status: Optional[int]
    settings: Optional[dict]
