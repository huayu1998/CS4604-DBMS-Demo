from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "Backend is running successfully :)\n"

@app.route("/api/students")
def students():
    return jsonify([{"studentID": 1, "name": "Alice", "major": "CS", "gpa": 3.8}])

if __name__ == "__main__":
    app.run(port=5001, debug=True)