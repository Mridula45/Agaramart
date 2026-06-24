from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    status = Column(
        String(50),
        default="Pending"
    )

    payment_status = Column(
        String(50),
        default="Pending"
    )

    payment_order_id = Column(
        String(255),
        nullable=True
    )

    payment_id = Column(
    String(255),
    nullable=True
)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )