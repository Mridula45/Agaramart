from fastapi import APIRouter
from app.utils.email import send_test_email
from app.utils import email

router = APIRouter(
    prefix="/api/email",
    tags=["Email"]
)

@router.get("/test")
async def test_email():

    await send_test_email(
        "mridulalakshmi86@gmail.com"
    )
    

    return {
        "message": "Email sent successfully"
    }