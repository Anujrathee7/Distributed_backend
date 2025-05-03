from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import json
import threading
import os

app = FastAPI()
lock = threading.Lock()
DATA_FILE = "user_service/user.json"

class User(BaseModel):
    username: str
    password: str

origins = [
    "http://localhost:5173",  # Your frontend's URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the React frontend on localhost:5173 to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

def read_data():

    # Can be removed if the database is working

    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    '''cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append(row)
    return users'''
    

def write_data(data):
    # Can be removed if the database is working
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    '''cursor = conn.cursor()
    for user in data:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                       (user['username'], user['password']))'''

@app.post("/register")
def register(user: User):
    with lock:
        data = read_data()
        if any(u['username'] == user.username for u in data):
            raise HTTPException(status_code=400, detail="User already exists")
        data.append(user.dict())
        write_data(data)
    return {"msg": "User registered"}

@app.post("/login")
def login(user: User):
    with lock:
        data = read_data()
        if not any(u['username'] == user.username and u['password'] == user.password for u in data):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": "Login successful"}
