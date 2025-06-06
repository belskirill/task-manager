from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean, func

from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    login: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    number_phone: Mapped[str] = mapped_column(String(200), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    is_verification: Mapped[bool] = mapped_column(Boolean, default=False)

