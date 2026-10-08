from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    stock: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    stock: int
    is_available: bool

    class Config:
        from_attributes = True