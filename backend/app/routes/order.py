from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.user import User

from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


@router.post("/place")
def place_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_items = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total_amount = 0

    for item in cart_items:

        product = db.query(Product).filter(
            Product.product_id == item.product_id
        ).first()

        total_amount += (
            product.price * item.quantity
        )

    order = Order(
        user_id=current_user.user_id,
        total_amount=total_amount,
        status="Pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:

        product = db.query(Product).filter(
            Product.product_id == item.product_id
        ).first()

        order_item = OrderItem(
            order_id=order.order_id,
            product_id=product.product_id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

    db.commit()

    for item in cart_items:
        db.delete(item)

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": order.order_id
    }


@router.get("/my-orders")
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    orders = db.query(Order).filter(
        Order.user_id == current_user.user_id
    ).all()

    return orders


@router.get("/{order_id}")
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = db.query(Order).filter(
        Order.order_id == order_id,
        Order.user_id == current_user.user_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order_items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).all()

    return {
        "order": order,
        "items": order_items
    }