from fastapi import APIRouter
from .user_api import router as user_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(user_router)
