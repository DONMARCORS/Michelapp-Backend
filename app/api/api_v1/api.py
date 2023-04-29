from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, pedido
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(pedido.router, prefix="/pedido", tags=["pedido"])