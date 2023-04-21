#include <Servo.h>
#include <SoftwareSerial.h>


SoftwareSerial rs485(0,1); // declare RX and TX pins on Nano
const byte HEADER = 0xAB;
const byte FOOTER = 0xB3;
const byte forwByte = 0xA3;
const byte backByte = 0xA4;
const byte upByte = 0xA5;
const byte downByte = 0xA6;
const byte rightByte = 0xA7;
const byte leftByte = 0xA8;
const byte servOpenByte = 0xA9;
const byte servCloseByte = 0xA0;
const byte stopByte = 0xB5;
int enablePin = 8;
byte msg;
byte prevmsg;

//thruster
Servo T1001;
Servo T1002;
Servo T601;
Servo T602;
Servo T603;

// Servo motor
Servo clawServ;
int clawAngle = 0;


int tStop = 1500;//0%
int forwMin = 1625; //25% //600-2400 min and max -> 1500 == stop -> 50% == 1950
int forwMax = 1750; //50%
int revMin = 1375; //-25%
int revMax = 1250; //-50%

byte state = 0;
byte speed = 0;





void setup() {
  Serial.begin(9600);
  rs485.begin(9600);
  T1001.attach(6);
  T1002.attach(5);
  T601.attach(11);
  T602.attach(10);
  T603.attach(9);
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

void process(byte command) {
  switch (command) {
    case forwByte: 
      // Handle command 1: Forward
      T1001.writeMicroseconds(forwMax);
      T1002.writeMicroseconds(forwMax); //may have to change to revMax depending on direction of T100 thruster
      T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);
      Serial.println("Forw");
      break;
    case upByte:
      // Handle command 2: Up
      T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);
      T601.writeMicroseconds(forwMin); //may have to change to revMin depending on direction of T60 thruster
      T602.writeMicroseconds(forwMax);
      T603.writeMicroseconds(forwMin);
      Serial.println("Up");
      break;
    case downByte:
      // Handle command 3: Down
      T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);
      T601.writeMicroseconds(revMin); //may have to change to revMin depending on direction of T60 thruster
      T602.writeMicroseconds(revMax);
      T603.writeMicroseconds(revMin);
      Serial.println("Down");
      break;
    case rightByte:
      // Handle command 4: Right
      T1001.writeMicroseconds(forwMax);
      T1002.writeMicroseconds(revMax); //may have to change to forwMax depending on direction of T100 thruster
      T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);
      Serial.println("Right");
      break;
    case leftByte:
      // Handle command 5: Left
      T1001.writeMicroseconds(revMax);
      T1002.writeMicroseconds(forwMax); //may have to change to revMax depending on direction of T100 thruster
      T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);
      Serial.println("Left");
      break;
    case backByte:
      // Handle command 6: Backward
      T1001.writeMicroseconds(revMax);
      T1002.writeMicroseconds(revMax); //may have to change to forwMax depending on direction of T100 thruster
      T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);
      Serial.println("Back");
      break;
    case stopByte:
      // Handle command 0: Off
      T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);
      T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);
      Serial.println("Stop");
      break;
    case servCloseByte: //servo close
       clawAngle = map(70, 0, 180, 0, 180);
       clawServ.write(clawAngle);
		 break;
    case servOpenByte: //servo open
        clawAngle = map (0, 0, 180, 0, 180);
        clawServ.write(clawAngle);
		  break;
    default:
      // Handle unknown command
      Serial.println("NULL");
      break;
  }
}

void loop() {
  T602.writeMicroseconds(1700);
  digitalWrite(enablePin, LOW); // enable "receiving"
  delay(50); //give a bit of delay to enable "receiving" mode
  if (rs485.available()) {
  msg = rs485.read();
  switch(msg){
    case HEADER:
      delay(50);
      msg = rs485.read();
      process(msg);
      break;
    case FOOTER:
      digitalWrite(enablePin, HIGH); //enable "transmitting"
      delay(50);
      Serial.println("REC"); // "received" msg
      prevmsg = msg;
      break;
  }
  } else {
    process(prevmsg);
  }
 
}
