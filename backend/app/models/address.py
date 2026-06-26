from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP  # type: ignore[reportMissingImports]

from sqlalchemy.sql import func  # type: ignore[reportMissingImports]
from app.database.database import Base


class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(15),
        nullable=False
    )

    address_line = Column(
        String(255),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    state = Column(
        String(100),
        nullable=False
    )

    pincode = Column(
        String(10),
        nullable=False
    )

    is_default = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )