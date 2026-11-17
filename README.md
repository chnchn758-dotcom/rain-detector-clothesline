# Rain Detector and Automatic Clothesline Retractor

An Arduino-based model house. A rain sensor on the roof detects rain and a servo closes the
clothesline; when it is dry again the clothesline reopens. Every rain/dry event is saved with its
time and shown on a live web dashboard.

CS403 – Integrative Programming Languages 1

## How it works

```
Rain sensor -> Arduino Uno -> USB serial -> bridge.py -> HTTP POST -> Flask API -> MySQL -> Dashboard
                    |
                  Servo (closes / opens the clothesline)
```

The server records the time of each event, so the microcontroller needs no clock.
A Wi-Fi board (ESP32 / NodeMCU) can later post to the same API instead of `bridge.py`.

## Hardware

- Arduino Uno
- Rain sensor module (rain pad + comparator board)
- SG90 servo motor
- Breadboard, jumper wires (optional: push button on pin 2 for testing)

| Part                  | Uno pin                        |
| --------------------- | ------------------------------ |
| Servo signal          | D9 (power 5V, ground GND)      |
| Rain sensor DO        | D3                             |
| Rain sensor AO        | A0 (only used for calibration) |
| Rain sensor VCC / GND | 5V / GND                       |

Servo angles: 110 degrees = open (dry), 0 degrees = closed (rain).

## Project structure

```
app.py                  Flask backend and API
bridge.py               Reads the Uno's serial output and posts events to the API
simulate.py             Sends fake rain/dry events for testing
templates/index.html    Dashboard (Tailwind CSS)
schema.sql              MySQL database and table
arduino/rain_clothesline/rain_clothesline.ino   Arduino firmware
requirements.txt        Python packages
```

## Setup

1. Start MySQL (XAMPP uses port 3307 in this project) and run `schema.sql` in phpMyAdmin.
2. Create the virtual environment and install packages:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Edit `DB_CONFIG` in `app.py` (host, port, user, password) to match your MySQL.
4. Start the server: `python app.py`, then open http://127.0.0.1:5000/
5. Upload `rain_clothesline.ino` to the Uno with the Arduino IDE, then close the IDE and Serial Monitor.
6. Set `SERIAL_PORT` in `bridge.py` (for example `COM3`) and run `python bridge.py`.

To test without hardware, run `python simulate.py` while the server is running.

## API

| Method | Endpoint               | Description                                                |
| ------ | ---------------------- | ---------------------------------------------------------- |
| POST   | `/api/rain`            | Save an event: `{"status": "rain"}` or `{"status": "dry"}` |
| GET    | `/api/events?limit=50` | Latest events, newest first                                |
| GET    | `/api/status`          | Current status and since when                              |
