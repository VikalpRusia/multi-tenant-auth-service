import time

from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.users import UserCreate


class UserController:

    @staticmethod
    def save_user(user: UserCreate, db: AsyncSession):
        epoch_time = int(time.time())
        user_model = User(**user.model_dump(show_password=True), created_at=epoch_time, updated_at=epoch_time)
        db.add(user_model)
        return user_model
