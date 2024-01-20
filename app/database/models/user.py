from sqlalchemy import Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from dataclasses import dataclass

from .base import Base

@dataclass
class User(Base):
    __tablename__  = "users"
    __table_args__ = (
        UniqueConstraint("username"),
        UniqueConstraint("email"),
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Basic account info
    username: Mapped[str] = mapped_column(String(24), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)

    # Password info
    hashed_password: Mapped[str] = mapped_column(String(100))
    salted_password: Mapped[str] = mapped_column(String(100))

    # Nation info
    nation_id: Mapped[int] = mapped_column(Integer, ForeignKey("nations.id"), nullable=True)
    nation_obj = relationship("Nation", backref="leader", foreign_keys="User.nation_id")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "nation_id": self.nation_id
        }