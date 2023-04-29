from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Pedido(Base):
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(256), nullable=False)
    items_pedido = relationship(
        "ItemPedido",
        cascade="all,delete-orphan",
        back_populates="pedido",
        uselist=True, # We set this to True because we want to have a list of items_pedido
    )

    owner_id = Column(Integer, ForeignKey("user.id"), nullable=True, unique=True)
    owner = relationship("User", back_populates="pedidos")