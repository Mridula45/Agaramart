# app/routes/admin.py

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.category import Category

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    total_users = db.query(User).count()
    total_products = db.query(Product).count()
    total_categories = db.query(Category).count()

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_categories": total_categories
    }