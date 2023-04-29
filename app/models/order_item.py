from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class OrderItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=True, unique=False)
    order = relationship(
        "Order",
        back_populates="order_items",
        uselist=False, # We set this to False because we want to only allow one order
    )

    product_id = Column(Integer, ForeignKey("product.id"), nullable=True, unique=False)
    product = relationship(
        "Product",
        back_populates="order_items",
        uselist=False, # We set this to False because we want to only allow one product
    )