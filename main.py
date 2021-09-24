# uvicorn main:app --reload
# http://127.0.0.1:8000/

from os import name
from fastapi import FastAPI, HTTPException, Query, Path
from random import randint
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json

pt_json = None
with open('../plan_time_campaign.json', 'r') as outfile:
    pt_json = json.load(outfile)

class PlanTime(BaseModel):
    aniocampana: str
    codpais: str
    plantime: Optional[int] = None

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0

app = FastAPI()

# Root path service
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Basic GET
@app.get("/items/{item_name}")
async def read_item_id(item_name):
    return {item_name: randint(100000, 999999)}

# Order matters (PATH PARAMETER)
@app.get("/items/airpods")
async def read_airpods_id():
    return {"item_id": 666}

# Path parameters & automatic validations
@app.get("/products/{product_id}")
async def read_product_id(product_id: int):
    # product_id: int = Path(..., gt=5, lt=10)):
    return {"product_id": product_id}

# Query parameters with auto-validation
@app.get("/query_params/{product_name}")
async def read_items(product_name: str,
                     q: str):
                     #q: Optional[str] = Query(None, min_length=3, max_length=10)):
    results = {"product_id_1": "product_name_1", "product_id_2": "product_name_2"}

    results.update({'path_param': product_name})

    if q:
        results.update({"query_param": q})
    return results

# POST method with self-designed objects
@app.post("/product/")
async def create_item(product: Product):
    product.name = product.name.capitalize()
    return product

# POST method with path parameters
@app.post("/product/{product_id}")
async def create_product(product_id: int, product: Product):
    response = vars(product)
    response.update({'product_id': product_id})
    return response

# Belcorp example
@app.get("/plantime/{aniocampana}/{codpais}")
async def get_plantime(aniocampana: str, codpais: str):
    print("*********")
    print(pt_json)
    print("*********")
    codpais = codpais.upper()

    response = PlanTime(aniocampana=aniocampana, codpais=codpais)
    
    pt = -1 
    try:
        pt = pt_json[aniocampana][codpais]
    except:
        print(pt_json.keys())
        raise HTTPException(status_code=404, detail=f"Plantime not found for {aniocampana} and {codpais}.")

    response.plantime = pt
    
    return response
