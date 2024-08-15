from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from controllers.user_controller import UserController
from db.database import get_db_session
from schemas.users import UserCreate, UserBase

router = APIRouter(prefix="/users", tags=["users"])

@cbv(router)
class UserAPI:

    def __init__(self):
        self.controller = UserController()
    @router.post("/")
    def sign_up(self, user: UserCreate, db = Depends(get_db_session)) -> UserBase:
        return self.controller.save_user(user, db)

