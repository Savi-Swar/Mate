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
const byte servHookByte = 0xA1;

const byte stopByte = 0xB5;
const byte precision = 0xF1;
const byte regular = 0xF2;
const byte rapid = 0xF3;
const byte pitchUpByte = 0xC1;
const byte pitchDownByte = 0xC2;
const byte rollRightByte = 0xC;
const byte rollLeftByte = 0xC4;
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


const int t100forPre = 1550;
const int t100forReg = 1700;
const int t100forRap = 1800;
const int t100revPre = 1450;
const int t100revReg = 1300;
const int t100revRap = 1200;
const int t60forPre = 1600;
const int t60forReg = 1750;
const int t60forRap = 1900;
const int t60revPre = 1400;
const int t60revReg = 1250;
const int t60revRap = 1100;
bool cur = false;
int directionT100 = 0; // 1 for forward, 2 for reverse, 3 for right, 4 for left, 5 for sharp right, 6 for sharp left
//byte state = 0;
//byte speed = 0;
int t100forSpeed = 1600;
int t100revSpeed = 1400;
int t60forSpeed = 1600;
int t60revSpeed = 1400;
const int tStop = 1500;

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

void process(byte command) {
  switch (command) {
    case forwByte: 
      // Handle command 1: Forward
      T1001.writeMicroseconds(t100revSpeed);
      T1002.writeMicroseconds(t100revSpeed); //may have to change to revMax depending on direction of T100 thruster
      T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);
      Serial.println("Forw");
      break;
    case upByte:
      // Handle command 2: Up
      T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);
      T601.writeMicroseconds(1500+ (t60forSpeed-1500)/2); //may have to change to revMin depending on direction of T60 thruster
      T602.writeMicroseconds(t60forSpeed);
      T603.writeMicroseconds(1500+ (t60forSpeed-1500)/2);
      Serial.println("Up");
      break;
    case downByte:
      // Handle command 3: Down
      T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);
      T601.writeMicroseconds(1500+ (t60revSpeed-1500)/2); //may have to change to revMin depending on direction of T60 thruster
      T602.writeMicroseconds(t60revSpeed);
      T603.writeMicroseconds(1500+ (t60revSpeed-1500)/2);
      Serial.println("Down");
      break;
    case rightByte:
      // Handle command 4: Right
      T1001.writeMicroseconds(t100revSpeed);
      T1002.writeMicroseconds(t100forSpeed); //may have to change to forwMax depending on direction of T100 thruster
      T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);
      Serial.println("Right");
      break;
    case leftByte:
      // Handle command 5: Left
      T1001.writeMicroseconds(1500+1*(t100forSpeed-1500));
      T1002.writeMicroseconds(t100revSpeed); //may have to change to revMax depending on direction of T100 thruster
      T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);
      Serial.println("Left");
      break;
    case backByte:
      // Handle command 6: Backward
      T1001.writeMicroseconds(1500+1*(t100forSpeed-1500));
      T1002.writeMicroseconds(t100forSpeed); //may have to change to forwMax depending on direction of T100 thruster
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
    case servHookByte: //servo close
       
       clawServ.write(60);
       delay(100);
    case servCloseByte: //servo close
       
       clawServ.write(60);
       delay(100);
		 break;
    case servOpenByte: //servo open
        clawServ.write(180);
		  break;
    case pitchUpByte:
      T601.writeMicroseconds((((t60forSpeed-1500)/2))+1500);
      T602.writeMicroseconds(t60revSpeed);
      T603.writeMicroseconds((((t60forSpeed-1500)/2))+1500);
      T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);
      break;
    case pitchDownByte:
      T601.writeMicroseconds(1500+ (t60revSpeed-1500)/2);
      T602.writeMicroseconds(t60forSpeed);
      T603.writeMicroseconds(1500+ (t60revSpeed-1500)/2);
      T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);
      break;
    case rollRightByte:
      T601.writeMicroseconds(t60forSpeed);
      T602.writeMicroseconds((((t60forSpeed-1500)/2))+1500); // may need to change to forMax, revMax, revMin
      T603.writeMicroseconds(t60revSpeed);
      break;
    case rollLeftByte:
      T601.writeMicroseconds(t60revSpeed);
      T602.writeMicroseconds((((t60forSpeed-1500)/2))+1500); //may need to change to forMax, revMax, revMin
      T603.writeMicroseconds(t60forSpeed);
      break;
    default:
      // Handle unknown command
      Serial.println("NULL");
      break;
  }
}

void loop() {
  digitalWrite(enablePin, LOW); // enable "receiving"
  delay(50); //give a bit of delay to enable "receiving" mode
  if (rs485.available()) {
  msg = rs485.read();

  switch(msg){
    case HEADER:
      delay(50);
      msg = rs485.read();
      Serial.println(msg);

      switch(msg){
        case precision:
          t100forSpeed = t100forPre;
          t100revSpeed = t100revPre;
          t60forSpeed = t60forPre;
          t60revSpeed = t60revPre;
          Serial.println("precision");

          break;
        case regular:
          t100forSpeed = t100forReg;
          t100revSpeed = t100revReg;
          t60forSpeed = t60forReg;
          t60revSpeed = t60revReg;
          Serial.println("Mid");
          break;
        case rapid:
          t100forSpeed = t100forRap;
          t100revSpeed = t100revRap;
          t60forSpeed = t60forRap;
          t60revSpeed = t60revRap;
          Serial.println("rapid");

          break;
      }
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
