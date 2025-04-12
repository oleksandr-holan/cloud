from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4, UUID


class Item(BaseModel):
    id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        schema_extra = {
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item",
                "price": 29.99,
            }
        }
