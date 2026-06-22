from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.product_schema import ProductCreate

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
        "message": "Product created",
        "product_id": new_product.product_id
    }

@router.get("/")
def get_products(
    db: Session = Depends(get_db)
):
    return db.query(Product).all()