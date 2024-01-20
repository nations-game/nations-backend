from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .user import User


class Nation(Base):
    __table__ = "nations"
    
    # Basic info
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    leader: Mapped["User"] = relationship(back_populates="nation")
    system: Mapped[int] = Column(Integer) # 0 = capitalism, 1 = socialism, 2 = dictatorship
    
    # Commodities
    money: Mapped[int] = Column(Integer)
    food: Mapped[int] = Column(Integer)
    power: Mapped[int] = Column(Integer)
    building__materials: Mapped[int] = Column(Integer)
    metal: Mapped[int] = Column(Integer)
