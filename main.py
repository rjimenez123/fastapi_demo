from fastapi import FastAPI
from random import randint
from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/items/airpods")
# async def read_airpods_id():
#     return {"item_id": 2244}

@app.get("/items/{item_name}")
async def read_item_id(item_name):
    return {item_name: randint(100000, 999999)}

@app.get("/products/{product_id}")
async def read_product_id(product_id: int):
    return {"item_id": product_id}

@app.get("/items/airpods")
async def read_airpods_id():
    return {"item_id": 2244}

@app.post("/product/")
async def create_item(product: Product):
    return product