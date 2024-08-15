from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from controllers.role_controller import RoleController
from db.database import get_db_session
from schemas.role import RoleCreate, Role

router = APIRouter(prefix="/roles", tags=["roles"])


@cbv(router)
class RoleApi:
    def __init__(self):
        self.role_controller = RoleController()

    @router.post("/")
    async def create_role(self, role: RoleCreate, db=Depends(get_db_session)) -> Role:
        return await self.role_controller.save_role(role, db)
