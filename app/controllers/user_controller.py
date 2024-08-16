import time
from datetime import timedelta, datetime, timezone

import bcrypt
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
    DOMAIN,
)
from utils.email_service import send_email


class UserController:
    @staticmethod
    async def save_user(user: UserCreate, db: AsyncSession) -> User:
        epoch_time = int(time.time())
        user_model = User(
            **user.model_dump(show_password=True),
            created_at=epoch_time,
            updated_at=epoch_time,
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
    def create_token(
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
        access_token = UserController.create_token(
            data={"sub": email, "type": "access_token"}
        )
        refresh_token = UserController.create_token(
            data={"sub": email, "type": "refresh_token"},
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    @staticmethod
    async def reset_password(email: str, db: AsyncSession) -> None:
        user = await UserController.get_user(email, db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        token = UserController.create_token(
            {"sub": email, "type": "password_reset_token"},
            expires_delta=timedelta(hours=1),
        )
        reset_link = f"http://{DOMAIN}/reset-password?token={token}"
        html_content = f"""
        <html>
        <head>
            <style>
                .email-container {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    line-height: 1.5;
                }}
                .email-header {{
                    background-color: peachpuff;
                    padding: 10px;
                    text-align: center;
                }}
                .email-body {{
                    padding: 20px;
                }}
                .reset-link {{
                    display: inline-block;
                    padding: 10px 20px;
                    margin-top: 20px;
                    color: white;
                    background-color: #007bff;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                .reset-link:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h2>Password Reset Request</h2>
                </div>
                <div class="email-body">
                    <p>Hello,</p>
                    <p>We received a request to reset your password. Click the button below to reset your password:</p>
                    <a href="{reset_link}" class="reset-link">Reset Password</a>
                    <p>If you did not request a password reset, please ignore this email.</p>
                    <p>Thank you,</p>
                    <p>Alpha Beta Corp</p>
                </div>
            </div>
        </body>
        </html>
        """
        send_email("Password Reset Request", html_content, {"email": user.email})

    @staticmethod
    def extract_email_from_token(jwt_token: str, token_type: str = ""):
        data = jwt.decode(jwt_token, key=SECRET_KEY, algorithms=ALGORITHM)
        is_valid = True
        if token_type:
            is_valid = data.get("type", None) == token_type
        if is_valid:
            return data["sub"]
        raise jwt.exceptions.InvalidTokenError(
            f"Expected type: {token_type} and got {data.get('type',None)}"
        )

    @staticmethod
    async def validate_token_and_change_password(
        jwt_token: str, new_password, db: AsyncSession
    ):
        email = UserController.extract_email_from_token(
            jwt_token, token_type="password_reset_token"
        )
        await UserController.__change_password(email, new_password, db)

    @staticmethod
    async def __change_password(email: str, new_password: str, db: AsyncSession):
        user = await UserController.get_user(email, db)
        salt = bcrypt.gensalt()
        user.password = new_password
        await db.flush()
