import time
import requests

URL = "http://127.0.0.1:5000/api/rain"

for status in ["rain", "dry", "rain", "dry"]:
    response = requests.post(URL, json={"status": status})
    print(status, response.status_code, response.json())
    time.sleep(2)