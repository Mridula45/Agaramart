# app/routes/admin.py

from fastapi import APIRouter, HTTPException
from razorpay import Order
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import Depends

from app.database.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.category import Category

from app.utils.auth import get_current_user
from app.utils.roles import (
    require_admin,
    require_superadmin
)

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    require_admin(current_user)

    return {
        "users": db.query(User).count(),
        "products": db.query(Product).count(),
        "orders": db.query(Order).count(),
        "revenue":
            db.query(
                func.sum(Order.total_amount)
            ).scalar() or 0
    }
# View Vendors

@router.get("/vendors")
def get_vendors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    require_admin(current_user)

    return db.query(User).filter(
        User.role_id == 2
    ).all()

# View Orders

@router.get("/orders")
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    require_admin(current_user)

    return db.query(Order).all()

# View Products

@router.get("/products")
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    require_admin(current_user)

    return db.query(Product).all()

    # Delete Vendor

@router.delete("/vendor/{vendor_id}")
def delete_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    require_superadmin(current_user)

    vendor = db.query(User).filter(
        User.user_id == vendor_id,
        User.role_id == 2
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    db.delete(vendor)
    db.commit()

    return {
        "message": "Vendor deleted"
    }


# View Admins

@router.get("/admins")
def get_admins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    require_superadmin(current_user)

    return db.query(User).filter(
        User.role_id == 3
    ).all()


# Delete Admin

@router.delete("/admin/{admin_id}")
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    require_superadmin(current_user)

    admin = db.query(User).filter(
        User.user_id == admin_id,
        User.role_id == 3
    ).first()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    db.delete(admin)
    db.commit()

    return {
        "message": "Admin deleted"
    }