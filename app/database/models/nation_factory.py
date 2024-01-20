from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

# Production calculation:
# production * (current level * level multiplier)
class NationFactory(Base):
    __tablename__  = "nation_factories"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[int] = mapped_column(Integer, ForeignKey("factory_types.id"))
    nation: Mapped[int] = mapped_column(Integer, ForeignKey("nations.id"))