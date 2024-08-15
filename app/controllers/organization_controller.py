import time

from sqlalchemy.ext.asyncio import AsyncSession

from models import Organization
from schemas.organization import OrganizationCreate


class OrganizationController:
    @staticmethod
    async def save_org(org: OrganizationCreate, db: AsyncSession) -> Organization:
        epoch_time = int(time.time())
        org_model = Organization(
            **org.model_dump(), created_at=epoch_time, updated_at=epoch_time
        )
        db.add(org_model)
        await db.flush()
        await db.refresh(org_model)
        return org_model
