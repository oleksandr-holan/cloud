from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime

app = FastAPI(title="Simple CRUD API")

# Simple in-memory database
fake_db = {}
item_id_counter = 1

# Item model
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    
class ItemCreate(ItemBase):
    pass
    
class Item(ItemBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# CRUD operations
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    global item_id_counter
    
    new_item = Item(
        id=item_id_counter,
        name=item.name,
        description=item.description,
        price=item.price,
        created_at=datetime.now()
    )
    
    fake_db[item_id_counter] = new_item
    item_id_counter += 1
    
    return new_item

@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10):
    return list(fake_db.values())[skip : skip + limit]

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemBase):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update item while preserving id and created_at
    stored_item = fake_db[item_id]
    update_data = item.dict(exclude_unset=True)
    
    # Preserve id and created_at
    update_data["id"] = stored_item.id
    update_data["created_at"] = stored_item.created_at
    
    # Update the item
    fake_db[item_id] = Item(**update_data)
    return fake_db[item_id]

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del fake_db[item_id]
    return None

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Simple CRUD API"}

# For Heroku deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)