from sqlalchemy import Integer, String, Column, Boolean, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False)
    birthday = Column(Date, nullable=False)
    address = Column(String(256), index=True, nullable=True)
    privilege = Column(Integer, default=False, nullable=False) # 1: ADMIN, 2: VENDEDOR, 3: CLIENTE
    orders = relationship(
        "Order",
        cascade="all,delete",
        back_populates="owner",
        uselist=True, # We set this to True because we want to have a list of orders
    )

    hashed_password = Column(String(256), nullable=True)