from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DECIMAL,
    Boolean,
    TIMESTAMP
)

from sqlalchemy.sql import func
from app.database.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vendor_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id")
    )

    product_name = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    price = Column(
        DECIMAL(10,2),
        nullable=False
    )

    stock_quantity = Column(
        Integer,
        default=0
    )

    image_url = Column(Text)

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )