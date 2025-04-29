from fastapi import APIRouter
from api.api import router as docker_router

api_router = APIRouter()

# 注册所有API路由
api_router.include_router(docker_router)
