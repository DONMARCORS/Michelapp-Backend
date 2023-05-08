from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(256), nullable=False)
    order_items = relationship(
        "OrderItem",
        cascade="all,delete-orphan",
        back_populates="order",
        uselist=True, # We set this to True because we want to have a list of order_items
    )
    created_at = Column(String(256), nullable=False)

    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=False)
    owner = relationship(
        "User", 
        back_populates="orders",
    )