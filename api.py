from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "items.db"

# Crear la tabla si no existe
def init_db():
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

# Crear un ítem
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": item_id, "name": name, "description": description}), 201

# Leer todos los ítems
@app.route("/items", methods=["GET"])
def get_items():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    conn.close()
    items = [{"id": r[0], "name": r[1], "description": r[2]} for r in rows]
    return jsonify(items)

# Leer un ítem específico
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE id=?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"id": row[0], "name": row[1], "description": row[2]})
    else:
        return jsonify({"error": "Item no encontrado"}), 404

# Actualizar un ítem
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name=?, description=? WHERE id=?", (name, description, item_id))
    conn.commit()
    conn.close()
    return jsonify({"id": item_id, "name": name, "description": description})

# Borrar un ítem
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item eliminado"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)