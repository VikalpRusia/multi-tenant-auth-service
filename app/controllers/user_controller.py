import time

from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user import UserCreate


class UserController:
    @staticmethod
    async def save_user(user: UserCreate, db: AsyncSession) -> User:
        epoch_time = int(time.time())
        user_model = User(
            **user.model_dump(show_password=True),
            created_at=epoch_time,
            updated_at=epoch_time
        )
        db.add(user_model)
        await db.flush()
        await db.refresh(user_model)
        return user_model
