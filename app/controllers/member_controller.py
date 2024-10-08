import time

import jwt
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.constants import SECRET_KEY, ALGORITHM
from models import Member
from schemas.member import MemberCreate, UpdateMember
from schemas.user_invite import UserInvite


class MemberController:
    @staticmethod
    async def save_member(member: MemberCreate, db: AsyncSession) -> Member:
        epoch_time = int(time.time())
        member_model = Member(
            **member.model_dump(), created_at=epoch_time, updated_at=epoch_time
        )
        db.add(member_model)
        await db.flush()
        await db.refresh(member_model)
        return member_model

    @staticmethod
    async def delete_member(member_id: int, db: AsyncSession):
        result = await db.execute(delete(Member).where(member_id == Member.id))
        return result.rowcount == 1

    @staticmethod
    async def update_member(
            member_id: int, update_member_data: UpdateMember, db: AsyncSession
    ):
        member = await db.scalar(select(Member).where(member_id == Member.id))
        if member:
            for key, value in update_member_data.model_dump().items():
                member[key] = value
            await db.flush()
            return True
        return False

    @staticmethod
    async def invite_member(member_invite: UserInvite, db: AsyncSession):
        decoded_token = jwt.decode(member_invite.token.get_secret_value(), SECRET_KEY, ALGORITHM)
        member = Member(**member_invite.model_dump())
        db.add(member)
        await db.flush()
        await db.refresh(member)
        return member
