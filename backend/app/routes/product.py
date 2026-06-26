from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
from app.database.database import get_db
from app.schemas.product_schema import ProductCreate
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.product import Product
from app.models.user import User

from app.utils.auth import get_current_user
router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Only Vendor, Admin, SuperAdmin
    if current_user.role_id not in [2, 3, 4]:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    new_product = Product(
        vendor_id=current_user.user_id,
        category_id=product.category_id,
        product_name=product.product_name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        image_url=product.image_url
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product created successfully",
        "product_id": new_product.product_id
    }


@router.get("/")
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(9, ge=1),
    db: Session = Depends(get_db)
):

    skip = (page - 1) * limit

    total_products = db.query(Product).count()

    products = (
        db.query(Product)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total_products,
        "total_pages": (
            total_products + limit - 1
        ) // limit,
        "products": products
    }

@router.get("/my-products")
def get_my_products(
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1),
    search: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    skip = (page - 1) * limit

    query = db.query(Product).filter(
        Product.vendor_id == current_user.user_id
    )

    if search.strip():
        query = query.filter(
            Product.product_name.ilike(f"%{search}%")
        )

    total = query.count()

    products = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "products": products,
        "page": page,
        "total": total,
        "total_pages": (total + limit - 1) // limit
    }

   


@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Client cannot update
    if current_user.role_id == 1:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    existing_product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not existing_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Vendor can update only own products
    if current_user.role_id == 2:
        if existing_product.vendor_id != current_user.user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    existing_product.product_name = product.product_name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.stock_quantity = product.stock_quantity
    existing_product.category_id = product.category_id
    existing_product.image_url = product.image_url

    db.commit()

    return {
        "message": "Product updated successfully"
    }


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Client cannot delete
    if current_user.role_id == 1:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Vendor can delete only own products
    if current_user.role_id == 2:
        if product.vendor_id != current_user.user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }