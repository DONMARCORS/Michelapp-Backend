from datetime import date
import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base
from app.core.config import settings
from app.db.initial_data.initial_products import PRODUCTS
from app.db.initial_data.initial_clients import CLIENTS
from app.db.initial_data.initial_vendors import VENDORS
from app.db.initial_data.initial_orders import ORDERS

logger = logging.getLogger(__name__)



REPORTS = [
    {
        "id": 1000,
        "notas": "Declaracion pal SAT",
        "owner_id":3,
        "total": 1000,
        "rfc": "ALALLALALALAB"
    },
    {
        "id": 2000,
        "notas": "Lavaremos dinero con esta",
        "owner_id":3,
        "total": 2000,
        "rfc": "BCBCBCBCBCBCB"
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
                first_name="ADMINISTRADOR", 
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
    if CLIENTS:
        for client in CLIENTS:
            user = crud.user.get_by_email(db, email= client["email"])
            if not user:
                user_in = schemas.UserCreate(
                    first_name=client["first_name"],
                    last_name=client["last_name"],
                    email=client["email"],
                    password=client["password"],
                    birthday=client["birthday"],
                    privilege=client["privilege"] # 1: ADMIN, 2: VENDEDOR, 3: CLIENTE
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
    if REPORTS:
        for report in REPORTS:
          if crud.report.get(db, id=report["id"]):
              logger.warning(
                  f"The product with id {report['id']} already exists in the database. Skipping creation."
              )
              continue

          report_in = schemas.report.ReportCreate(
              id=report["id"],
              notas=report["notas"],
              total=report["total"],
              rfc=report["rfc"],
              owner_id=user.id,
          )
          crud.report.create(db, obj_in=report_in)
    

    if VENDORS:
        for vendor in VENDORS:
            user = crud.user.get_by_email(db, email= vendor["email"])

            if not user:
                user_in = schemas.UserCreate(
                    first_name=vendor["first_name"],
                    last_name=vendor["last_name"],
                    email=vendor["email"],
                    password=vendor["password"],
                    birthday=vendor["birthday"],
                    privilege= vendor["privilege"] # 1: ADMIN, 2: VENDEDOR, 3: CLIENTE
                )
                user = crud.user.create(db, obj_in=user_in)
            else:
                logger.warning(
                    "Vendedor already exists in the database. Skipping creation."
                    f"Email: {settings.FIRST_CLIENT} already exists in the database."
                )
            logger.debug(f"Created client {user.id}")
