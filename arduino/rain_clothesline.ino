#include <Servo.h>

Servo clothesServo;

const int SERVO_PIN = 9;
const int RAIN_DO_PIN = 3;       // rain sensor DO: LOW = wet
const int DRY_ANGLE = 110;       // clothesline out / open (dry)
const int RAIN_ANGLE = 0;        // clothesline in / closed (rain)

const unsigned long RAIN_CONFIRM_MS = 500;   // must be wet this long before closing
const unsigned long DRY_CONFIRM_MS = 5000;   // must be dry this long before opening
                                             // (use 60000 or more for real use)

bool isRaining = false;
bool lastWet = false;
unsigned long conditionSince = 0;

void applyState() {
  if (isRaining) {
    clothesServo.write(RAIN_ANGLE);
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("rain");
  } else {
    clothesServo.write(DRY_ANGLE);
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("dry");
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(RAIN_DO_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  clothesServo.attach(SERVO_PIN);
  clothesServo.write(DRY_ANGLE);
}

void loop() {
  bool wet = (digitalRead(RAIN_DO_PIN) == LOW);

  if (wet != lastWet) {
    lastWet = wet;
    conditionSince = millis();
  }

  unsigned long elapsed = millis() - conditionSince;

  if (wet && !isRaining && elapsed >= RAIN_CONFIRM_MS) {
    isRaining = true;
    applyState();
  } else if (!wet && isRaining && elapsed >= DRY_CONFIRM_MS) {
    isRaining = false;
    applyState();
  }
}
