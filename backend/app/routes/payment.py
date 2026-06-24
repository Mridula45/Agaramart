from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import razorpay

from app.database.database import get_db
from app.models.order import Order
from app.models.user import User

from app.utils.auth import get_current_user
from app.core.config import settings

router = APIRouter(
    prefix="/api/payment",
    tags=["Payments"]
)

client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)


@router.post("/create-order/{order_id}")
def create_payment_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Admin and SuperAdmin can access any order
    if current_user.role_id in [3, 4]:

        order = db.query(Order).filter(
            Order.order_id == order_id
        ).first()

    else:

        order = db.query(Order).filter(
            Order.order_id == order_id,
            Order.user_id == current_user.user_id
        ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    payment_order = client.order.create({
        "amount": int(float(order.total_amount) * 100),
        "currency": "INR",
        "receipt": f"order_{order.order_id}"
    })

    print("Razorpay Order ID:", payment_order["id"])

    order.payment_order_id = payment_order["id"]

    print("Before Commit:", order.payment_order_id)

    db.commit()
    db.refresh(order)

    print("After Commit:", order.payment_order_id)

    return {
        "razorpay_order_id": payment_order["id"],
        "amount": payment_order["amount"],
        "currency": payment_order["currency"]
    }


@router.post("/verify")
def verify_payment(
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
    db: Session = Depends(get_db)
):

    try:

        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        order = db.query(Order).filter(
            Order.payment_order_id == razorpay_order_id
        ).first()

        if order:
            order.payment_status = "Paid"
            db.commit()

        return {
            "message": "Payment verified successfully"
        }

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Payment verification failed"
        )