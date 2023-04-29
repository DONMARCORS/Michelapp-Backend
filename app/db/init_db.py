from datetime import date
import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base
from app.core.config import settings

logger = logging.getLogger(__name__)

PEDIDOS = [
    {
        "id": 1,
        "status": "EN PROGRESO",
        "owner_id": 1,
    },
]

ITEMS_PEDIDO = [
    {
        "id": 1,
        "cantidad": 2,
        "product_id": 1000,
        "owner_id": 1,
    },
]

# Por el momento no existe tabla productos por lo que no se utiliza
PRODUCTOS = [
    {
        "id": 1000,
        "nombre": "MICHELADA",
        "precio": 1000,
        "cantidad": 10,
    },
]



# Make sure all SQL Alchemy models are imported (app.db.base) before initializing,
# otherwise Alembic might fail to initialize realtionships property
# for more details see:https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

def init_db(db: Session) -> None:
    # Tables should be created with Alebix migrations
    # But if you dont want to use migrations, create
    # The tables uncommenting the following lines
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email= settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                first_name="INITIAL super firstname", 
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                #birthday is a Date object
                birthday=date(1990, 1, 1),
                privilege=1, # 1: ADMIN, 2: VENDEDOR, 3: CLIENTE
            )
            user = crud.user.create(db, obj_in=user_in)

        else:
            logger.warning(
                "Superuser already exists in the database. Skipping creation."
                f"Email: {settings.FIRST_SUPERUSER} already exists in the database."
            )
        if not user.pedidos:
            for pedido in PEDIDOS:
                pedido_in = schemas.PedidoCreate(
                    status=pedido["status"],
                    owner_id=user.id,
                )
                crud.pedido.create(db, obj_in=pedido_in)

    else:
        logger.warning(
            "No superuser defined in the environment. Skipping creation."
            
            "Need to be created manually."
            "eg. of env FIRST_SUPERUSER=admin@email.com"
        )