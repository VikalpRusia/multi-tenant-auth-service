from fastapi import APIRouter
from .user_api import router as user_router
from .organization_api import router as organization_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(user_router)
v1_router.include_router(organization_router)
