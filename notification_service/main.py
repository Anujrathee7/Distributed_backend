from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Notification(BaseModel):
    recipient: str
    message: str

@app.post("/notify")
def notify(notification: Notification):
    print(f"Notification to {notification.recipient}: {notification.message}")
    return {"status": "sent"}
