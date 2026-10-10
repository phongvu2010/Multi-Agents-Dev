from pydantic import BaseModel

class CatalogItemResponse(BaseModel):
    id: str
    name: str
    price: float
    stock_quantity: int
    is_active: bool

    class Config:
        from_attributes = True
