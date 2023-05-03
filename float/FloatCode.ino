#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Servo.h>
#include <time.h>

// Wi-Fi and server settings
const char* ssid = "Siddhant's iPhone";
const char* password = "password";
const IPAddress serverIP(172, 20, 10, 6);
const uint16_t serverPort = 8080;

// Servo pin
const int servoPin = D1;

// Time thresholds
const unsigned long servoOnTime = 20000; // 1 minute in milliseconds
const unsigned long servoOffTime = 20000; // 1 minute in milliseconds

// NTP settings
const char* ntpServer = "pool.ntp.org";
const long timezoneOffset = 7*3600; // Offset in seconds for your timezone

Servo myservo;
bool startSignalReceived = false;
bool sent = false;
void servoCalib() {
  myservo.write(0);
  delay(3000);
  myservo.write(120);
  delay(3000);
  myservo.write(0);
  delay(3000);

}
void setup() {
  Serial.begin(115200);
  myservo.attach(servoPin);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to Wi-Fi");

  // Configure NTP
  configTime(timezoneOffset, 0, ntpServer);
}

bool checkStartSignal() {
  WiFiClient client;

  if (client.connect(serverIP, serverPort)) {
    client.print("check_start_signal");
    String response = client.readStringUntil('\n');
    client.stop();

    if (response == "start") {
      Serial.println("Start signal received");
      return true;
    } else {
      Serial.println("Waiting for start signal");
      return false;
    }
  } else {
    Serial.println("Failed to connect to server");
    return false;
  }
}

void loop() {
  if (!startSignalReceived) {
    startSignalReceived = checkStartSignal();
  } else {
    // Control the servo with a timer
    if (!sent) {
      sendData();
    }
    servoCalib();
    myservo.write(120); // Open the syringes
    delay(servoOnTime);
    myservo.write(0); // Close the syringes
    delay(servoOffTime);

    // Send data when surfaced (assuming the float is surfaced after closing the syringes)
    if (!sent) {
      sendData();
      sent = true;
    }
  }
}

String getFormattedTime() {
  time_t now;
  struct tm timeinfo;
  char buffer[30];

  time(&now);
  localtime_r(&now, &timeinfo);
  strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &timeinfo);

  return String(buffer);
}

void sendData() {
  WiFiClient client;

  if (client.connect(serverIP, serverPort)) {
    String currentTime = getFormattedTime();
    String data = "shrimp," + currentTime;
    client.print(data);
    client.stop();
    Serial.println("Data sent");
  } else {
    Serial.println("Failed to connect to server");
  }
}
