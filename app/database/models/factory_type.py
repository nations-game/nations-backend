from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

# Production calculation:
# production * (current level * level multiplier)
class FactoryType(Base):
    __tablename__  = "factory_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(24))
    commodity: Mapped[str] = mapped_column(String(24))
    production: Mapped[int] = mapped_column(Integer, default=5)
    max_level: Mapped[int] = mapped_column(Integer, default=5)
    level_multiplier: Mapped[float] = mapped_column(Float, default=1) # min 0.1, max 2