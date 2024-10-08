import re
from typing import Optional, override

from bcrypt import hashpw, gensalt
from pydantic import BaseModel, Field, field_validator, SecretStr, ConfigDict


class UserBase(BaseModel):
    email: str = Field(pattern=r".+@.+\.com$", examples=["example@gmail.com"])
    profile: dict = {}
    status: int = 0
    settings: Optional[dict] = {}


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: SecretStr

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, secret: SecretStr) -> SecretStr:
        plain_password = secret.get_secret_value()
        if len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", plain_password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", plain_password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", plain_password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", plain_password):
            raise ValueError("Password must contain at least one special character")
        salt = gensalt()
        return SecretStr(
            hashpw(password=plain_password.encode("utf-8"), salt=salt).decode("utf-8")
        )

    @override
    def model_dump(self, show_password=False, **kwargs) -> dict:
        result = super().model_dump(**kwargs)
        if show_password:
            result["password"] = self.password.get_secret_value()
        return result
