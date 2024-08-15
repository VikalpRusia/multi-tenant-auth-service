import time
from datetime import timedelta, datetime, timezone

import jwt
from bcrypt import checkpw
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.token import Token
from schemas.user import UserCreate
from config.constants import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


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

    @staticmethod
    async def get_user(user_email, db: AsyncSession) -> User:
        user = await db.scalar(select(User).where(User.email == user_email))
        return user

    @staticmethod
    async def validate_user(
        user_email: str, user_password: str, db: AsyncSession
    ) -> bool:
        user_in_db = await UserController.get_user(user_email, db)
        if user_in_db is None:
            return False
        if not checkpw(
            password=user_password.encode("utf-8"),
            hashed_password=user_in_db.password.encode("utf-8"),
        ):
            return False
        return True

    @staticmethod
    async def create_token(
        data: dict,
        expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def login_for_access_token(
        email: str, password: str, db: AsyncSession
    ) -> Token:
        if not await UserController.validate_user(email, password, db):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token = await UserController.create_token(
            data={"sub": email, "type": "access_token"}
        )
        refresh_token = await UserController.create_token(
            data={"sub": email, "type": "refresh_token"},
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
