from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_restful.cbv import cbv

from controllers.user_controller import UserController
from db.database import get_db_session
from schemas.reset_password import ResetPassword
from schemas.token import Token
from schemas.user import UserCreate, User

router = APIRouter(prefix="/users", tags=["users"])


@cbv(router)
class UserAPI:
    def __init__(self):
        self.controller = UserController()

    @router.post("/")
    async def sign_up(self, user: UserCreate, db=Depends(get_db_session)) -> User:
        return await self.controller.save_user(user, db)

    @router.post("/token")
    async def login(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db=Depends(get_db_session),
    ) -> Token:
        return await self.controller.login_for_access_token(
            form_data.username, form_data.password, db=db
        )

    @router.post("/reset-password")
    async def reset_password(
        self, reset_password: ResetPassword, db=Depends(get_db_session)
    ) -> dict:
        await self.controller.reset_password(reset_password.email, db)
        return {"message": "Mail sent successfully"}
