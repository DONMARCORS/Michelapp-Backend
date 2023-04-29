from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(256), nullable=False)
    order_items = relationship(
        "OrderItem",
        cascade="all,delete-orphan",
        back_populates="product",
        uselist=True, # We set this to True because we want to have a list of order_items
    )