from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pickle

app = Flask(__name__)
CORS(app)

# Load trained model
model = pickle.load(open("model/model.pkl", "rb"))

# 🔹 Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    req = request.json

    data = req["features"]
    profession = req.get("profession", "employee")

    amount = data[1]
    time = data[0]

    # ML prediction
    prediction = model.predict([data])[0]

    # 🎯 Profession-based realistic logic
    if profession == "farmer":
        if amount > 20000 or (amount > 15000 and time < 6):
            prediction = 1

    elif profession == "business":
        if amount > 150000 or (amount > 100000 and time < 6):
            prediction = 1

    elif profession == "student":
        if amount > 10000 or time > 23:
            prediction = 1

    elif profession == "employee":
        if amount > 50000 or (amount > 30000 and time < 6):
            prediction = 1

    return jsonify({"fraud": int(prediction)})


# 🔹 Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return {"status": "success"}
    else:
        return {"status": "fail"}


# 🔹 Register API
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data["username"], data["password"])
        )
        conn.commit()
        return {"message": "Registered Successfully"}
    except:
        return {"message": "User already exists"}
    finally:
        conn.close()


# 🔹 Home route
@app.route("/")
def home():
    return "API running"


# Run server
if __name__ == "__main__":
    app.run(debug=True)