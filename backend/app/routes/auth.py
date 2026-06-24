from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserRegister, UserLogin
from app.database.database import get_db
from fastapi import Request
from app.core.limiter import limiter
from app.models.user import User
from app.models.role import Role

from app.utils.password import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import create_access_token
from app.utils.auth import get_current_user
from app.utils.roles import require_role
import random

from app.schemas.user_schema import (
    ForgotPasswordRequest
)

from app.utils.email import (
    send_reset_email
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    role = db.query(Role).filter(
        Role.role_name == user.role
    ).first()

    if not role:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(
            user.password
        ),
        role_id=role.role_id,
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.user_id
    }


@router.post("/login")
@limiter.limit("Try again later")
def login_user(
    request: Request,
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": db_user.user_id,
        "email": db_user.email,
        "role_id": db_user.role_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "user_id": current_user.user_id,
        "name": current_user.name,
        "email": current_user.email,
        "role_id": current_user.role_id,
        "is_verified": current_user.is_verified
    }


@router.get("/admin")
def admin_dashboard(
    current_user: User = Depends(get_current_user)
):

    require_role(3, 4)(current_user)

    return {
        "message": "Welcome Admin"
    }


@router.get("/vendor")
def vendor_dashboard(
    current_user: User = Depends(get_current_user)
):

    require_role(2, 3, 4)(current_user)

    return {
        "message": "Welcome Vendor"
    }


@router.get("/client")
def client_dashboard(
    current_user: User = Depends(get_current_user)
):

    require_role(1)(current_user)

    return {
        "message": "Welcome Client"
    }

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    otp = str(
        random.randint(
            100000,
            999999
        )
    )

    print(
        f"OTP for {request.email}: {otp}"
    )

    await send_reset_email(
        request.email,
        otp
    )

    return {
        "message": "OTP sent successfully"
    }