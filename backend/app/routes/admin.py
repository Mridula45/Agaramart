# app/routes/admin.py

from fastapi import APIRouter
from razorpay import Order
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends

from app.database.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.category import Category

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):
    users_count = db.query(User).count()

    products_count = db.query(Product).count()

    orders_count = db.query(Order).count()

    revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    return {
        "users": users_count,
        "products": products_count,
        "orders": orders_count,
        "revenue": revenue or 0
    }