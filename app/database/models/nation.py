from enum import Enum

from sqlalchemy import Integer, String, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, relationship, mapped_column

from dataclasses import dataclass

from .base import Base

nation_factory_association = Table(
    "nation_factory_association",
    Base.metadata,
    Column("nation_id", Integer, ForeignKey("nations.id")),
    Column("factory_id", Integer, ForeignKey("factory_types.id")),
    Column("quantity", Integer, default=1),
)

@dataclass
class Nation(Base):
    __tablename__  = "nations"
    
    # Basic info
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    system: Mapped[int] = mapped_column(Integer) # 0 = capitalism, 1 = socialism, 2 = dictatorship
    population: Mapped[int] = mapped_column(Integer, default=50_000)
    happiness: Mapped[int] = mapped_column(Integer, default=75) # min 0, max 100
    flag: Mapped[str] = mapped_column(String, nullable=True) # link to flag, will be implemented later
    
    # Commodities
    money: Mapped[int] = mapped_column(Integer, default=100_000)
    food: Mapped[int] = mapped_column(Integer, default=100_000)
    power: Mapped[int] = mapped_column(Integer, default=10_000)
    building_materials: Mapped[int] = mapped_column(Integer, default=1_000)
    metal: Mapped[int] = mapped_column(Integer, default=1_000)
    consumer_goods: Mapped[int] = mapped_column(Integer, default=10_000)

    # Factories
    factories = relationship("FactoryType", secondary=nation_factory_association)

    # Leader info
    leader_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    leader_user = relationship("User", backref="nation", foreign_keys="Nation.leader_id")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "system": self.system,
            "leader_id": self.leader_id,

            # Commodities
            "money": self.money,
            "food": self.food,
            "power": self.power,
            "building_materials": self.building_materials,
            "metal": self.metal
        }


class NationSystem(Enum):
    CAPITALISM = 0
    SOCIALISM = 1
    DICTATORSHIP = 2