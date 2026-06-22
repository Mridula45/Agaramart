from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserRegister
from app.database.database import database
from app.utils.password import hash_password

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register_user(user: UserRegister):

    existing_user = await database.users.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(
            user.password
        ),
        "role": user.role,
        "is_verified": False
    }

    result = await database.users.insert_one(
        user_data
    )

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }