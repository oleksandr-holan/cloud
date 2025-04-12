from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


class Item(BaseModel):
    id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item",
                "price": 29.99,
            }
        }
