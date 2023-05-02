from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, order, product, clientes, reporte_venta, vendedores
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(order.router, prefix="/order", tags=["order"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
api_router.include_router(reporte_venta.router, prefix="/reporte-venta", tags=["reporte-venta"])
api_router.include_router(vendedores.router, prefix="/vendedores", tags=["vendedores"])