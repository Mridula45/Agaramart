from pydantic import BaseModel  # type: ignore[import]

class PlaceOrderRequest(BaseModel):
    address_id: int