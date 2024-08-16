from fastapi import APIRouter
from .user_api import router as user_router
from .organization_api import router as organization_router
from .member_api import router as member_router
from .role_api import router as role_router
from .stats import router as stats_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(user_router)
v1_router.include_router(organization_router)
v1_router.include_router(member_router)
v1_router.include_router(stats_router)
