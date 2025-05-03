from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import threading
import os

app = FastAPI()
lock = threading.Lock()
DATA_FILE = "appointment_service/appointments.json"


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

class Appointment(BaseModel):
    patient: str
    doctor: str
    time: str

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.post("/book")
def book(appt: Appointment):
    with lock:
        data = read_data()
        if any(a['doctor'] == appt.doctor and a['time'] == appt.time for a in data):
            raise HTTPException(status_code=400, detail="Slot already booked")
        data.append(appt.dict())
        write_data(data)
    return {"msg": "Appointment booked"}

@app.get("/appointments/{patient}")
def get_appointments(patient: str):
    with lock:
        data = read_data()
        user_appts = [a for a in data if a["patient"] == patient]
    return user_appts
