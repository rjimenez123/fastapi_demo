# uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from random import randint
from typing import Optional
from pydantic import BaseModel
import pandas as pd

# TODO plan times hardcodeados
plantime_df = pd.DataFrame()
plantime_df['aniocampana'] = ['202101', '202101', '202101']
plantime_df['codpais'] = ['PE', 'CO', 'PR']
plantime_df['plantime'] = [5, 4, 3]


class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0

class PlanTime(BaseModel):
    aniocampana: str
    codpais: str
    plantime: Optional[int] = -1

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

# Order matters (URL)
@app.get("/items/airpods")
async def read_airpods_id():
    return {"item_id": 2244}

# POST method with self-designed objects
@app.post("/product/")
async def create_item(product: Product):
    product.name = product.name.capitalize()
    return product

# Path parameters & request body
@app.post("/product/{product_id}")
async def create_product(product_id: int, product: Product):
    response = vars(product)
    response.update({'product_id': product_id})
    return response

# Belcorp example
@app.get("/plantime/{aniocampana}/{codpais}")
async def get_plantime(aniocampana: str, codpais: str):
    codpais = codpais.upper()

    response = dict()
    response['aniocampana'] = aniocampana
    response['codpais'] = codpais

    sub_df = plantime_df[(plantime_df['aniocampana']==aniocampana) & (plantime_df['codpais']==codpais)]
    if len(sub_df) == 0:
        raise HTTPException(status_code=404, detail=f"Plantime not found for {aniocampana} and {codpais}.")

    response['plantime'] = int(sub_df['plantime'].values[0])
    return response