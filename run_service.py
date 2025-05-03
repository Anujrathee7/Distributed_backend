import subprocess
import time

# Start User Service
user_service = subprocess.Popen(["uvicorn", "user_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

# Start Appointment Service
appointment_service = subprocess.Popen(["uvicorn", "appointment_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"])

# Start Doctor Service
doctor_service = subprocess.Popen(["uvicorn", "doctor_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8002"])

# Start Notification Service
notification_service = subprocess.Popen(["uvicorn", "notification_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8003"])


# Wait for the services to finish (this will never actually stop unless you terminate the script)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Terminate services gracefully on script exit
    user_service.terminate()
    appointment_service.terminate()
    doctor_service.terminate()
    notification_service.terminate()
