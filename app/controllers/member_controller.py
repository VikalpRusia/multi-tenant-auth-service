import time

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from models import Member
from schemas.member import MemberCreate


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
        return result.rowcount==1
