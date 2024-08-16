from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from controllers.stats_controller import StatsController
from db.database import get_db_session

router = APIRouter(prefix="/stats", tags=["stats"])


@cbv(router)
class Stats:
    def __init__(self):
        self.stats_controller = StatsController()

    @router.get("/role-wise-user-count")
    async def get_role_wise_user_count(self, db=Depends(get_db_session)):
        return await self.stats_controller.get_role_wise_user_count(db)

    @router.get("/organization-wise-user-count")
    async def get_organization_wise_user_count(self, db=Depends(get_db_session)):
        return await self.stats_controller.get_organization_wise_user_count(db)

    @router.get("/organization-wise-role-wise-user-count")
    async def get_organization_wise_role_wise_user_count(
        self, db=Depends(get_db_session)
    ):
        return await self.stats_controller.get_organization_wise_role_wise_user_count(
            db
        )
