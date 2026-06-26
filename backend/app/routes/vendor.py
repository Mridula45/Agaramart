from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/api/vendor",
    tags=["Vendor"]
)


@router.get("/dashboard")
def vendor_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Vendor only
    if current_user.role_id != 2:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    total_products = db.query(Product).filter(
        Product.vendor_id == current_user.user_id
    ).count()

    order_items = db.query(OrderItem).join(
        Product,
        Product.product_id == OrderItem.product_id
    ).filter(
        Product.vendor_id == current_user.user_id
    ).all()

    total_orders = len(order_items)

    revenue = 0

    for item in order_items:
        revenue += float(item.price) * item.quantity

    pending_orders = db.query(OrderItem).join(
        Product,
        Product.product_id == OrderItem.product_id
    ).join(
        Order,
        Order.order_id == OrderItem.order_id
    ).filter(
        Product.vendor_id == current_user.user_id,
        Order.status == "Pending"
    ).count()

    return {
        "vendor_name": current_user.name,
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "revenue": revenue
    }


@router.get("/orders")
def vendor_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role_id != 2:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    orders = db.query(
        Order,
        OrderItem,
        Product
    ).join(
        OrderItem,
        Order.order_id == OrderItem.order_id
    ).join(
        Product,
        Product.product_id == OrderItem.product_id
    ).filter(
        Product.vendor_id == current_user.user_id
    ).all()

    response = []

    for order, item, product in orders:

        response.append({
            "order_id": order.order_id,
            "product_name": product.product_name,
            "quantity": item.quantity,
            "price": float(item.price),
            "status": order.status,
            "payment_status": order.payment_status
        })

    return response