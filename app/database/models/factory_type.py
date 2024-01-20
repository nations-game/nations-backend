from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, relationship, mapped_column

from dataclasses import dataclass

from .base import Base

# Production calculation:
# production * (current level * level multiplier)
@dataclass
class FactoryType(Base):
    __tablename__  = "factory_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(24))
    commodity: Mapped[str] = mapped_column(String(24))
    production: Mapped[int] = mapped_column(Integer, default=5)
    max_level: Mapped[int] = mapped_column(Integer, default=5)
    current_level: Mapped[float] = mapped_column(Integer, default=1)

    """
    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "commodity": self.commodity,
            "production": self.production,
            "max_level": self.max_level,
            "current_level": self.current_level
        }
    """