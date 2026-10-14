import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

def get_db():
    cfg = dict(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "student_db"),
    )
    if os.getenv("DB_SSL_CA"):
        cfg["ssl_ca"] = os.getenv("DB_SSL_CA")
    return mysql.connector.connect(**cfg)

def run(sql, params=(), fetch=False):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        if fetch:
            return cur.fetchall()
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

@app.get("/api/students")                         # Read
def list_students():
    return jsonify(run(
        "SELECT studentID, name, major, CAST(gpa AS DOUBLE) AS gpa FROM students",
        fetch=True))

@app.post("/api/students")                        # Create
def create_student():
    d = request.get_json()
    new_id = run("INSERT INTO students (name, major, gpa) VALUES (%s, %s, %s)",
                 (d["name"], d["major"], d["gpa"]))
    return jsonify({"studentID": new_id}), 201

@app.put("/api/students/<int:student_id>")        # Update
def update_student(student_id):
    d = request.get_json()
    run("UPDATE students SET name=%s, major=%s, gpa=%s WHERE studentID=%s",
        (d["name"], d["major"], d["gpa"], student_id))
    return jsonify({"updated": student_id})

@app.delete("/api/students/<int:student_id>")     # Delete
def delete_student(student_id):
    run("DELETE FROM students WHERE studentID=%s", (student_id,))
    return jsonify({"deleted": student_id})

if __name__ == "__main__":
    app.run(port=5001, debug=True)