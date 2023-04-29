from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ItemPedido(Base):
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedido.id"), nullable=True, unique=True)
    pedido = relationship(
        "Pedido",
        back_populates="items_pedido",
        uselist=False, # We set this to False because we want to only allow one pedido
    )

    producto_id = Column(Integer, ForeignKey("producto.id"), nullable=True, unique=True)
    producto = relationship(
        "Producto",
        back_populates="items_pedido",
        uselist=False, # We set this to False because we want to only allow one product
    )