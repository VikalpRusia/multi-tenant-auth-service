from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_restful.cbv import cbv

from controllers.member_controller import MemberController
from db.database import get_db_session
from schemas.member import MemberCreate, Member, UpdateMember

router = APIRouter(prefix="/member", tags=["Member"])


@cbv(router)
class MemberAPI:
    def __init__(self):
        self.member_controller = MemberController()

    @router.post("/")
    async def sign_up(self, member: MemberCreate, db=Depends(get_db_session)) -> Member:
        return await self.member_controller.save_member(member, db)

    @router.delete("/{member_id}")
    async def delete_member(self, member_id: int, db=Depends(get_db_session)):
        if await self.member_controller.delete_member(member_id, db):
            return {"message": "deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member doesn't exist to be deleted")
