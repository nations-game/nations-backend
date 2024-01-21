from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from dataclasses import dataclass

from .base import Base

@dataclass
class NationFactory(Base):
    __tablename__  = "nation_factories"

    id: Mapped[int] = mapped_column(primary_key=True)

    nation_id: Mapped[int] = mapped_column(Integer, ForeignKey("nations.id"))
    factory_id: Mapped[int] = mapped_column(Integer, ForeignKey("factory_types.id"))

    # nation_obj = relationship("Nation", backref="nation_factories", foreign_keys="NationFactory.nation_id")
    # factory_type = relationship("FactoryType", backref="nation_factories", foreign_keys="NationFactory.factory_id")