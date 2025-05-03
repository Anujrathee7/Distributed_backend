from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os



app = FastAPI()
DATA_FILE = "doctor_service/doctor.json"

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

class Doctor(BaseModel):
    name: str
    specialty: str

def read_data():
    if not os.path.exists(DATA_FILE):
        print("no data file")
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.get("/doctors")
def get_doctors():
    return read_data()
