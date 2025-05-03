from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from AzureConn import connect
import json
import threading
import os

app = FastAPI()
lock = threading.Lock()
DATA_FILE = "appointment_service/appointments.json"
conn = connect()


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
    # Can be removed if the database is working
    '''if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)'''
    # Connect to the PostgreSQL database and fetch appointments
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()
    appointments = []
    for row in rows:
        appointments.append(row)
    return appointments
    

def write_data(data):
    # Can be removed if the database is working
    '''with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)'''
    cursor = conn.cursor()
    for appt in data:
        cursor.execute("INSERT INTO appointments (patient, doctor, time) VALUES (%s, %s, %s)", 
                       (appt['patient'], appt['doctor'], appt['time']))


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
