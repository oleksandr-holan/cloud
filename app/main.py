from fastapi import FastAPI, HTTPException, status
from .models import Item
from typing import List
from uuid import uuid4, UUID

app = FastAPI(title="CRUD API Demo")

# In-memory database
items_db = []


@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD API Demo"}


# Create operation
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    item.id = uuid4()
    items_db.append(item)
    return item


# Read all operation
@app.get("/items/", response_model=List[Item])
def read_items():
    return items_db


# Read one operation
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: UUID):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


# Update operation
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: UUID, updated_item: Item):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            updated_item.id = item_id
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")


# Delete operation
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: UUID):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
