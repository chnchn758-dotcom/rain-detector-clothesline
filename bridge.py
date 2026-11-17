import time
import requests
import serial

SERIAL_PORT = "COM3"   # change to your Uno's port
BAUD_RATE = 9600
API_URL = "http://127.0.0.1:5000/api/rain"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # the Uno restarts when the port opens
print("Listening on", SERIAL_PORT)

while True:
    line = ser.readline().decode("utf-8", errors="ignore").strip()

    if line in ("rain", "dry"):
        try:
            response = requests.post(API_URL, json={"status": line}, timeout=5)
            print(line, response.status_code)
        except requests.RequestException as error:
            print("Could not reach the dashboard:", error)