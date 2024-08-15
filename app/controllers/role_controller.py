import time

from sqlalchemy.ext.asyncio import AsyncSession

from models import Role
from schemas.role import RoleCreate


class RoleController:
    @staticmethod
    async def save_role(role: RoleCreate, db: AsyncSession) -> Role:
        epoch_time = int(time.time())
        role_model = Role(
            **role.model_dump(), created_at=epoch_time, updated_at=epoch_time
        )
        db.add(role_model)
        await db.flush()
        await db.refresh(role_model)
        return role_model
