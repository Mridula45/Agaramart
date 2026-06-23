from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.user import User

from app.schemas.cart_schema import AddToCart

from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/api/cart",
    tags=["Cart"]
)

@router.post("/add")
def add_to_cart(
    item: AddToCart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    product = db.query(Product).filter(
        Product.product_id == item.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id
    ).first()

    if not cart:
        cart = Cart(
            user_id=current_user.user_id
        )

        db.add(cart)
        db.commit()
        db.refresh(cart)

    cart_item = CartItem(
        cart_id=cart.cart_id,
        product_id=item.product_id,
        quantity=item.quantity
    )

    db.add(cart_item)
    db.commit()

    return {
        "message": "Product added to cart"
    }

@router.get("/")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id
    ).first()

    if not cart:
        return []

    return db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).all()

@router.put("/update/{cart_item_id}")
def update_cart_quantity(
    cart_item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    item = db.query(CartItem).filter(
        CartItem.cart_item_id == cart_item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    item.quantity = quantity

    db.commit()

    return {
        "message": "Quantity updated"
    }

@router.delete("/remove/{cart_item_id}")
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    item = db.query(CartItem).filter(
        CartItem.cart_item_id == cart_item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Item removed from cart"
    }