from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from doctor_service.AzureConn import connect
import psycopg2

app = FastAPI()

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

class Doctor(BaseModel):
    name: str
    specialty: str

def read_data():
    conn = connect()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT dname, speciality FROM doctors")
        rows = cursor.fetchall()
        return [{"name": row[0], "speciality": row[1]} for row in rows]
    except Exception as e:
        print("Error reading doctors:", e)
        raise HTTPException(status_code=500, detail="Database query failed")
    finally:
        conn.close()

@app.get("/doctors")
def get_doctors():
    return read_data()
