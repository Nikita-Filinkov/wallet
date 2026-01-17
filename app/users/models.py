from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__: str = "users"
    __table_args__ = (Index("ix_email", "email"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str]

    wallets = relationship(
        "Wallets",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Wallets.created_at.desc()",
    )

    def __str__(self) -> str:
        return f"Пользователь: {self.email}"
