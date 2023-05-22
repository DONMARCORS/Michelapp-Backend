from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    notas = Column(String(256), nullable=False)
    total = Column(Integer, nullable=False)
    rfc = Column(String(13), nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=False)
    owner = relationship(
        "User", 
        #back_populates="orders",
    )
    