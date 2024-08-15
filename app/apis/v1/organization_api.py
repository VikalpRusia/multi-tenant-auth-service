from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from controllers.organization_controller import OrganizationController
from db.database import get_db_session
from schemas.organization import Organization, OrganizationCreate

router = APIRouter(prefix="/organization", tags=["organization"])

@cbv(router)
class OrganizationAPI:

    def __init__(self):
        self.controller = OrganizationController()
    @router.post("/")
    async def sign_up(self, org: OrganizationCreate, db=Depends(get_db_session)) -> Organization:
        return await self.controller.save_org(org, db)

