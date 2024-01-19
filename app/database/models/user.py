from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .nation import Nation


class User(Base):
    __table__ = "users"
    
    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String)
    hashed: Mapped[str] = Column(String)
    salt: Mapped[str] = Column(String)
    email: Mapped[str] = Column(String)
    nation: Mapped["Nation"] = relationship(back_populates="leader")