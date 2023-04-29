from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Producto(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(256), nullable=False)
    items_pedido = relationship(
        "ItemPedido",
        cascade="all,delete-orphan",
        back_populates="producto",
        uselist=True, # We set this to True because we want to have a list of items_pedido
    )