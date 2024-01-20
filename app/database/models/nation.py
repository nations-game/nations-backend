from enum import Enum

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base


class Nation(Base):
    __tablename__  = "nations"
    
    # Basic info
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    system: Mapped[int] = mapped_column(Integer) # 0 = capitalism, 1 = socialism, 2 = dictatorship
    
    # Commodities
    money: Mapped[int] = mapped_column(Integer)
    food: Mapped[int] = mapped_column(Integer)
    power: Mapped[int] = mapped_column(Integer)
    building__materials: Mapped[int] = mapped_column(Integer)
    metal: Mapped[int] = mapped_column(Integer)

    # Leader info
    leader_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    leader_user = relationship("User", backref="nation", foreign_keys="Nation.leader_id")


class NationSystem(Enum):
    CAPITALISM = 0
    SOCIALISM = 1
    DICTATORSHIP = 2