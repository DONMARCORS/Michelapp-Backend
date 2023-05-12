from datetime import date
import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base
from app.core.config import settings

logger = logging.getLogger(__name__)

ORDERS = [
    {
        "status": "proceso",
        "owner_id": 2,
        "order_items": [
            {
                "quantity": 1,
                "product_id": 1000
            },
            {
                "quantity": 2,
                "product_id": 1001
            }
        ]
    },
]



# Por el momento no existe tabla products por lo que no se utiliza
PRODUCTS = [
    {
        "id": 1000,
        "name": "Michelada",
        "quantity": 10,
        "price": 100,
        "description": "Bebida",

    },
    {
        "id": 1001,
        "name": "Michelada con clamato",
        "quantity": 10,
        "price": 100,
        "description": "Bebida con clamato",

    },
    {
        "id": 1002,
        "name": "Michelada con mango",
        "quantity": 10,
        "price": 100,
        "description": "Bebida con mango",

    },
    {
        "id": 1003,
        "name": "Michelada con mango y chamoy",
        "quantity": 10,
        "price": 100,
        "description": "Bebida con mango y chamoy",

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
            crud.user.create(db, obj_in=user_in)

        else:
            logger.warning(
                "Superuser already exists in the database. Skipping creation."
                f"Email: {settings.FIRST_SUPERUSER} already exists in the database."
            )
        
    else:
        logger.warning(
            "No superuser defined in the environment. Skipping creation."
            
            "Need to be created manually."
            "eg. of env FIRST_SUPERUSER=admin@email.com"
        )
    # Create initial products

    for product in PRODUCTS:
        if crud.product.get(db, id=product["id"]):
            logger.warning(
                f"The product with id {product['id']} already exists in the database. Skipping creation."
            )
            continue

        product_in = schemas.ProductCreate(
            id=product["id"],
            name=product["name"],
            quantity=product["quantity"],
            price=product["price"],
            description=product["description"],
        )
        crud.product.create(db, obj_in=product_in)

    # Create initial client with orders
    if settings.FIRST_CLIENT:
        user = crud.user.get_by_email(db, email= settings.FIRST_CLIENT)
        if not user:
            user_in = schemas.UserCreate(
                first_name="Pepe", 
                last_name="Perez",
                email=settings.FIRST_CLIENT,
                password=settings.FIRST_CLIENT_PASSWORD,
                #birthday is a Date object
                birthday=date(1990, 1, 1),
                privilege=3, # 1: ADMIN, 2: VENDEDOR, 3: CLIENTE
            )
            user = crud.user.create(db, obj_in=user_in)
            
        else:
            logger.warning(
                "Client already exists in the database. Skipping creation."
                f"Email: {settings.FIRST_CLIENT} already exists in the database."
            )
        logger.debug(f"Created client {user.id}")
        for order in ORDERS:
            logger.debug(f"Creating order {order}")
            order_in = schemas.OrderCreate(
                status=order["status"],
                owner_id=user.id,
                order_items=order["order_items"],
            )
            crud.order.create(db=db, order_in=order_in)
    
    if settings.FIRST_VENDOR:
        user = crud.user.get_by_email(db, email= settings.FIRST_VENDOR)

        if not user:
            user_in = schemas.UserCreate(
                first_name="Vendedor", 
                last_name="Hernandez",
                email=settings.FIRST_VENDOR,
                password=settings.FIRST_VENDOR_PASSWORD,
                #birthday is a Date object
                birthday=date(1990, 1, 1),
                privilege=2, # 1: ADMIN, 2: VENDEDOR, 3: CLIENTE
            )
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.warning(
                "Client already exists in the database. Skipping creation."
                f"Email: {settings.FIRST_CLIENT} already exists in the database."
            )
        logger.debug(f"Created client {user.id}")
