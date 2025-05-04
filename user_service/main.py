from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from user_service.AzureConn import connect
import threading

app = FastAPI()
lock = threading.Lock()

class User(BaseModel):
    username: str
    password: str  # Keep this name in the API request body

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_data():
    conn = connect()
    if not conn:
        print("Failed to connect to PostgreSQL")
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, pass FROM users")  # Use "pass" here
        rows = cursor.fetchall()
        return [{"username": row[0], "password": row[1]} for row in rows]  # Normalize to "password"
    except Exception as e:
        print("Error reading data:", e)
        raise HTTPException(status_code=500, detail="Error reading data")
    finally:
        conn.close()

def write_data(user: User):
    conn = connect()
    if not conn:
        print("Failed to connect to PostgreSQL")
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, pass) VALUES (%s, %s)",  # Use "pass" here
            (user.username, user.password)
        )
        conn.commit()
    except Exception as e:
        print("Error writing data:", e)
        raise HTTPException(status_code=500, detail="Error writing data")
    finally:
        conn.close()

@app.post("/register")
def register(user: User):
    with lock:
        data = read_data()
        if any(u['username'] == user.username for u in data):
            raise HTTPException(status_code=400, detail="User already exists")
        write_data(user)
    return {"msg": "User registered"}

@app.post("/login")
def login(user: User):
    with lock:
        data = read_data()
        if not any(u['username'] == user.username and u['password'] == user.password for u in data):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": "Login successful"}
