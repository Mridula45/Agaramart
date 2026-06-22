from pydantic import BaseModel

class ProductCreate(BaseModel):
    category_id: int
    product_name: str
    description: str
    price: float
    stock_quantity: int
    image_url: str