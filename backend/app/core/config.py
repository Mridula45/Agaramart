from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    )

    RAZORPAY_KEY_ID = os.getenv(
        "RAZORPAY_KEY_ID"
    )

    RAZORPAY_KEY_SECRET = os.getenv(
        "RAZORPAY_KEY_SECRET"
    )

settings = Settings()

