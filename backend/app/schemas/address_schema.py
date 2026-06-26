from pydantic import BaseModel

class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line: str
    city: str
    state: str
    pincode: str
    is_default: bool = False