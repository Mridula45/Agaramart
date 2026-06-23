# app/models/cart_item.py

from sqlalchemy import Column, Integer, ForeignKey
from app.database.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    cart_item_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    cart_id = Column(
        Integer,
        ForeignKey("carts.cart_id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id")
    )

    quantity = Column(Integer, default=1)