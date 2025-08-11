from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

# Datos en memoria
items = []
counter = 1

# Modelo básico (diccionario simple)
# Normalmente usarías Pydantic, pero aquí lo haremos lo más simple posible.

@app.get("/items", response_model=List[dict])
def get_items():
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items")
def create_item(item: dict):
    global counter
    item["id"] = counter
    counter += 1
    items.append(item)
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, new_item: dict):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            new_item["id"] = item_id
            items[i] = new_item
            return new_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            del items[i]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
