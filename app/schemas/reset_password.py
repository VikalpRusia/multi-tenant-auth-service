from pydantic import BaseModel, Field


class ResetPassword(BaseModel):
    email: str = Field(pattern=r".+@.+\.com$", examples=["example@gmail.com"])
