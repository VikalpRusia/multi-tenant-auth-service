from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Member, Role, Organization


class StatsController:
    def __init__(self):
        pass

    async def get_role_wise_user_count(self, db: AsyncSession):
        result = await db.execute(
            select(Role.id, Role.name, func.count(Member.user_id).label("user_count"))
            .join(Role, Member.role_id == Role.id)
            .group_by(Member.role_id)
        )
        return [dict(row) for row in result.mappings().all()]

    async def get_organization_wise_user_count(self, db: AsyncSession):
        result = await db.execute(
            select(
                Organization.id,
                Organization.name,
                func.count(Member.user_id).label("user_count"),
            )
            .join(Organization, Member.org_id == Organization.id)
            .group_by(Member.org_id)
        )
        return [dict(row) for row in result.mappings().all()]

    async def get_organization_wise_role_wise_user_count(self, db: AsyncSession):
        result = await db.execute(
            select(
                Organization.id,
                Organization.name,
                Role.id,
                Role.name,
                func.count(Member.user_id).label("user_count"),
            )
            .join(Organization, Member.org_id == Organization.id)
            .join(Role, Member.role_id == Role.id)
            .group_by(Member.org_id)
            .group_by(Member.role_id)
        )
        return [dict(row) for row in result.mappings().all()]
