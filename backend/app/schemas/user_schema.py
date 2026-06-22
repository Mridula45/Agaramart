from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "client"


class UserLogin(BaseModel):
    email: EmailStr
    password: str