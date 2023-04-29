from app.crud.base import CRUDBase
from app.models.item_pedido import ItemPedido
from app.schemas.item_pedido import ItemPedidoCreate, ItemPedidoUpdate


class CRUDItemPedido(CRUDBase[ItemPedido, ItemPedidoCreate, ItemPedidoUpdate]):
    ...


item_pedido = CRUDItemPedido(ItemPedido)