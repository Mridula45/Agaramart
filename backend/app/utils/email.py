from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig
)

from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True
)

async def send_test_email(email: str):

    message = MessageSchema(
        subject="AgaraMart Email Test",
        recipients=[email],
        body="""
        Congratulations!

        Email configuration is working successfully.
        """,
        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(message)

async def send_reset_email(
    email: str,
    otp: str
):

    message = MessageSchema(
        subject="AgaraMart Password Reset OTP",
        recipients=[email],
        body=f"""
Your OTP is:

{otp}

This OTP is valid for 10 minutes.
        """,
        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(message)