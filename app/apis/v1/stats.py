from fastapi import APIRouter
from fastapi_restful.cbv import cbv

router = APIRouter(prefix="/stats")

@cbv(router)
class Stats:
    def __init__(self):
        pass

    @router.get("/users")
    async def get_users(self):
        pass
