
# import all models so that base has them before being
# imported by Alembic

from app.db.base_class import Base
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.report import Report