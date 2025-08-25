from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os

# Ruta de DB (por defecto en /data dentro del contenedor, fácil de persistir con volumen)
DB_DIR = os.getenv("DB_DIR", "./data")
DB_NAME = os.path.join(DB_DIR, "items.db")

app = FastAPI(  
    title="Items API (FastAPI + SQLite)",
    description="CRUD simple de items con FastAPI y SQLite",
    version="1.0.0"
)

# --------- DB init ----------
def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --------- Schemas ----------
class ItemIn(BaseModel):
    name: str
    description: Optional[str] = ""

class ItemOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""

# --------- Helpers ----------
def row_to_item(row) -> ItemOut:
    return ItemOut(id=row[0], name=row[1], description=row[2])

# --------- Endpoints ----------
@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemIn):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, description) VALUES (?, ?)",
        (item.name, item.description or "")
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return ItemOut(id=item_id, name=item.name, description=item.description or "")

@app.get("/items", response_model=List[ItemOut])
def get_items():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [row_to_item(r) for r in rows]

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items WHERE id=?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return row_to_item(row)

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemIn):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET name=?, description=? WHERE id=?",
        (item.name, item.description or "", item_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return ItemOut(id=item_id, name=item.name, description=item.description or "")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return {"message": "Item eliminado"}
