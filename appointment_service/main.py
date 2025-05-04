from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from appointment_service.AzureConn import connect
import threading
import psycopg2

app = FastAPI()
lock = threading.Lock()

class Appointment(BaseModel):
    patient: str
    doctor: str
    time: str

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
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT patient, doctor, time FROM appointments")
        rows = cursor.fetchall()
        return [{"patient": row[0], "doctor": row[1], "time": row[2]} for row in rows]
    except Exception as e:
        print("Error reading data:", e)
        raise HTTPException(status_code=500, detail="Database read failed")
    finally:
        conn.close()

def write_data(appointment: Appointment):
    conn = connect()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (patient, doctor, time) VALUES (%s, %s, %s)",
            (appointment.patient, appointment.doctor, appointment.time)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="This appointment slot is already taken.")
    except Exception as e:
        conn.rollback()
        print("Error writing data:", e)
        raise HTTPException(status_code=500, detail="Database write failed")
    finally:
        conn.close()

@app.post("/book")
def book(appt: Appointment):
    with lock:
        write_data(appt)
    return {"msg": "Appointment booked"}

@app.get("/appointments/{patient}")
def get_appointments(patient: str):
    with lock:
        data = read_data()
        return [a for a in data if a["patient"] == patient]
