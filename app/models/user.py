from sqlalchemy import Integer, String, Column, Boolean, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False)
    birthday = Column(Date, nullable=False)
    privilege = Column(Integer, default=False, nullable=False) # 1: ADMIN, 2: VENDEDOR, 3: CLIENTE
    pedidos = relationship(
        "Pedido",
        cascade="all,delete-orphan",
        back_populates="owner",
        uselist=True, # We set this to True because we want to have a list of pedidos
    )

    hashed_password = Column(String(256), nullable=True)