import re

from bcrypt import gensalt, hashpw
from pydantic import BaseModel, Field, SecretStr, field_validator


class ResetPassword(BaseModel):
    email: str = Field(pattern=r".+@.+\.com$", examples=["example@gmail.com"])


class RestPasswordConfirm(BaseModel):
    token: SecretStr
    new_password: SecretStr

    @field_validator("new_password")
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
