# app/models/cart.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database.database import Base

class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )