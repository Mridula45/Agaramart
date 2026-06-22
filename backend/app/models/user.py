from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    phone = Column(String(15))

    role_id = Column(Integer, ForeignKey("roles.role_id"))

    is_verified = Column(Boolean, default=False)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )