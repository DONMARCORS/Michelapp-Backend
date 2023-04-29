from app.crud.base import CRUDBase
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoUpdate


class CRUDPedido(CRUDBase[Pedido, PedidoCreate, PedidoUpdate]):
    ...


pedido = CRUDPedido(Pedido)