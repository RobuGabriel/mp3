from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID

from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app=FastAPI()

models.Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost:5500",  # Add your frontend's URL here
    "http://192.168.0.150:5500/index.html",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict this to specific HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can restrict this to specific headers if needed
)

def get_bd():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

class Product(BaseModel):
    id: UUID
    name: str = Field(min_length=1)
    price: str=Field(min_length=1)
    category: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=150)
    images: str = Field(min_length=1, max_length=100)

PRODUCTS=[]

@app.get("/api/product")
def read_api(db: Session=Depends(get_bd)):
    return db.query(models.Products).all()

@app.post("/")
def create_product(product:Product, db: SessionLocal = Depends(get_bd)):
    product_model=models.Products()
    product_model.name=product.name
    product_model.price=product.price
    product_model.category = product.category
    product_model.description = product.description
    product_model.images = product.images

    db.add(product_model)
    db.commit()

    return product

@app.delete("/")
def delete(product_id:int, db: Session=Depends(get_bd)):
    product_model = db.query(models.Products).filter(models.Products.id == product_id).first()

    if product_model is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.query(models.Products).filter(models.Products.id == product_id).delete()
    db.commit()
    return product_model

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
