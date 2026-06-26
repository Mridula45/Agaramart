from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.address_schema import AddressCreate

from app.models.address import Address
from app.models.user import User

from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/api/address",
    tags=["Address"]
)


@router.post("/")
def add_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if address.is_default:

        db.query(Address).filter(
            Address.user_id == current_user.user_id
        ).update(
            {"is_default": False}
        )

    new_address = Address(

        user_id=current_user.user_id,

        full_name=address.full_name,

        phone=address.phone,

        address_line=address.address_line,

        city=address.city,

        state=address.state,

        pincode=address.pincode,

        is_default=address.is_default

    )

    db.add(new_address)

    db.commit()

    db.refresh(new_address)

    return {
        "message": "Address Added",
        "address_id": new_address.address_id
    }


@router.get("/")
def get_addresses(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    return db.query(Address).filter(
        Address.user_id == current_user.user_id
    ).all()


@router.delete("/{address_id}")
def delete_address(

    address_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    address = db.query(Address).filter(
        Address.address_id == address_id,
        Address.user_id == current_user.user_id
    ).first()

    if not address:

        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    db.delete(address)

    db.commit()

    return {
        "message": "Address Deleted"
    }