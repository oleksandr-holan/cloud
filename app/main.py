from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI PostgreSQL CRUD API")

# CORS налаштування
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Отримання URL бази даних з змінних середовища
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    logger.warning("DATABASE_URL not found, using default PostgreSQL URL")
    DATABASE_URL = "postgresql://cloud:postgres@localhost/cloud"

# Створення підключення до бази даних
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database connection established")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    raise


# Модель SQLAlchemy для Item
class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)


# Створення таблиць
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    raise


# Pydantic моделі
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
        from_attributes = True


# Dependency для отримання сесії бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD операції
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        db_item = ItemModel(
            name=item.name, description=item.description, price=item.price
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        items = db.query(ItemModel).offset(skip).limit(limit).all()
        return items
    except Exception as e:
        logger.error(f"Error reading items: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading item {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemBase, db: Session = Depends(get_db)):
    try:
        db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        # Оновлення атрибутів
        db_item.name = item.name
        db_item.description = item.description
        db_item.price = item.price

        db.commit()
        db.refresh(db_item)
        return db_item
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating item {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        db.delete(item)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting item {item_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI PostgreSQL CRUD API"}


# Обробка помилок
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return {"detail": "An unexpected error occurred"}


# Для локального запуску та деплою на Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
