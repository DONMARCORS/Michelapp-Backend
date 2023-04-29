
# import all models so that base has them before being
# imported by Alembic

from app.db.base_class import Base
from app.models.user import User
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.producto import Producto