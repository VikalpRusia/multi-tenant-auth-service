from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from controllers.member_controller import MemberController
from db.database import get_db_session
from schemas.member import MemberCreate, Member

router = APIRouter(prefix="/member", tags=["Member"])


@cbv(router)
class MemberAPI:
    def __init__(self):
        self.member_controller = MemberController()

    @router.post("/")
    async def sign_up(self, member: MemberCreate, db=Depends(get_db_session)) -> Member:
        return await self.member_controller.save_member(member, db)
