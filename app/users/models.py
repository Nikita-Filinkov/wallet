from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Users(Base):
    __tablename__: str = "users"
    __table_args__ = (Index("ix_email", "email"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str]

    def __str__(self) -> str:
        return f"Пользователь: {self.email}"
