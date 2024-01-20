from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .user import User


class Nation(Base):
    __table__ = "nations"
    
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    money: Mapped[int] = Column(Integer)
    leader: Mapped["User"] = relationship(back_populates="nation")
