#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial rs485(0,1);
Servo T1001;
Servo T1002;
Servo T601;
Servo T602;
Servo T603;
Servo clawServ;
const uint8_t HEADER = 0x7A;
const uint8_t FOOTER = 0xA7;
uint8_t data[256];
uint8_t idx = 0;


void setup() {
  Serial.begin(9600);
  rs485.begin(9600);
  T1001.attach(6);
  T1002.attach(5);
  T601.attach(11);
  T602.attach(10);
  T603.attach(9);
  clawServ.attach(3);
  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, LOW); // set to 'receive' mode
  T1001.writeMicroseconds(1500);
  T1002.writeMicroseconds(1500);
  T601.writeMicroseconds(1500);
  T602.writeMicroseconds(1500);
  T603.writeMicroseconds(1500);
  delay(1000);
  T1001.writeMicroseconds(2000);
  T1002.writeMicroseconds(2000);
  T601.writeMicroseconds(2000);
  T602.writeMicroseconds(2000);
  T603.writeMicroseconds(2000);
  delay(4);
  T1001.writeMicroseconds(1500);
  T1002.writeMicroseconds(1500);
  T601.writeMicroseconds(1500);
  T602.writeMicroseconds(1500);
  T603.writeMicroseconds(1500);
  delay(7500);
}

void command(uint8_t left, uint8_t right, uint8_t front, uint8_t backL, uint8_t backR, uint8_t claw) {
    T1001.writeMicroseconds(1000 + left * 4);
    T1002.writeMicroseconds(1000 + 4 * right);
    T601.writeMicroseconds(1000 + 4 * front);
    T602.writeMicroseconds(1000 + 4 * backL);
    T603.writeMicroseconds(1000 + 4 * backR);
    clawSer.writeMicroseconds(1000 + 4 * claw);
}

void runThrusters(){
    command(data[1], data[2], data[3], data[4], data[5], data[6]);
}

void loop() {
    digitalWrite(enablePin, LOW); // enable "receiving"
    delay(50); //give a bit of delay to enable "receiving" mode
    if (rs485.available()) {
        uint8_t msg = rs485.read();
        Serial.print(idx);
        Serial.print(': ');
        Serial.write(msg);
        Serial.println();
        data[idx] = msg;
        if (idx == 0 && msg == HEADER) {
            idx ++;
        }
        if (idx > 0 && idx <= 6) {
            idx ++;
        }
        if (idx >= 7) {
            if (msg == FOOTER) runThrusters()
            else idx = 0;
        }
    }
}