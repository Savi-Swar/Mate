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
const byte pitchUpByte = 0xC1;
const byte pitchDownByte = 0xC2;
const byte rollRightByte = 0xC3;
const byte rollLeftByte = 0xC4;
//optional if using IMU:
const byte hoverByte = 0xD1;
const byte stopByte = 0xB5;
const byte precision = 0xF1;
const byte regular = 0xF2;
const byte rapid = 0xF3;
byte memMsg[9];
int enablePin = 8;
byte msg;
int bufferSize = 0;
int forSpeed;
int revSpeed;

//thruster
Servo T1001;
Servo T1002;
Servo T601;
Servo T602;
Servo T603;

// Servo motor
Servo clawServ;
int clawAngle = 0;


const int tStop = 1500;//0%

const int forwMin = 1625; //25% //600-2400 min and max -> 1500 == stop -> 50% == 1950
const int forwMax = 1750; //50%
const int revMin = 1375; //-25%
const int revMax = 1250; //-50%
//things above may be useless with new speed control
//new 3-type speed control:
const int forPre = 1600;
const int forReg = 1750;
const int forRap = 1900;
const int revPre = 1400;
const int revReg = 1250;
const int revRap = 1100;

//byte state = 0;
//byte speed = 0;





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
  T1001.writeMicroseconds(tStop);
  T1002.writeMicroseconds(tStop);
  T601.writeMicroseconds(tStop);
  T602.writeMicroseconds(tStop);
  T603.writeMicroseconds(tStop);
  delay(7500);
  digitalWrite(enablePin, LOW); // enable "receiving"
  delay(50); //give a bit of delay to enable "receiving" mode
}

void process(byte command) {
  switch (command) {
    case forwByte: 
      // Handle command 1: Forward
      T1001.writeMicroseconds(forSpeed);
      T1002.writeMicroseconds(forSpeed); //may have to change to revMax depending on direction of T100 thruster
      /*T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);*/
      Serial.println("Forw");
      break;
    case upByte:
      // Handle command 2: Up
      /*T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);*/
      T601.writeMicroseconds(((forSpeed-1500)/2))+1500); //may have to change to revMin depending on direction of T60 thruster
      T602.writeMicroseconds(forSpeed);
      T603.writeMicroseconds(((forSpeed-1500)/2))+1500);
      Serial.println("Up");
      break;
    case downByte:
      // Handle command 3: Down
      /*T1001.writeMicroseconds(tStop);
      T1002.writeMicroseconds(tStop);*/
      T601.writeMicroseconds(1500-((1500-revSpeed)/2)); //may have to change to revMin depending on direction of T60 thruster
      T602.writeMicroseconds(revSpeed);
      T603.writeMicroseconds(1500-((1500-revSpeed)/2));
      Serial.println("Down");
      break;
    case rightByte:
      // Handle command 4: Right
      T1001.writeMicroseconds(forSpeed);
      T1002.writeMicroseconds(revSpeed); //may have to change to forwMax depending on direction of T100 thruster
      /*T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);*/
      Serial.println("Right");
      break;
    case leftByte:
      // Handle command 5: Left
      T1001.writeMicroseconds(revSpeed);
      T1002.writeMicroseconds(forSpeed); //may have to change to revMax depending on direction of T100 thruster
      /*T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);*/
      Serial.println("Left");
      break;
    case backByte:
      // Handle command 6: Backward
      T1001.writeMicroseconds(revSpeed);
      T1002.writeMicroseconds(revSpeed); //may have to change to forwMax depending on direction of T100 thruster
      /*T601.writeMicroseconds(tStop);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(tStop);*/
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
    case pitchUpByte:
      T601.writeMicroseconds(forSpeed);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(forSpeed);
      break;
    case pitchDownByte:
      T601.writeMicroseconds(revSpeed);
      T602.writeMicroseconds(tStop);
      T603.writeMicroseconds(revSpeed);
      break;
    case rollRightByte:
      T601.writeMicroseconds(forSpeed);
      T602.writeMicroseconds(((forSpeed-1500)/2))+1500); // may need to change to forMax, revMax, revMin
      T603.writeMicroseconds(revSpeed);
      break;
    case rollLeftByte:
      T601.writeMicroseconds(revSpeed);
      T602.writeMicroseconds(((forSpeed-1500)/2))+1500)); //may need to change to forMax, revMax, revMin
      T603.writeMicroseconds(forSpeed);
      break;
    default:
      // Handle unknown command
      Serial.println("NULL");
      break;
  }
}

void loop() {
  msg = rs485.read();
  switch(msg){
    case HEADER:
      msg = rs485.read();
      switch(msg){
        case precision:
          forSpeed = forPre;
          revSpeed = revPre;
          break;
        case regular:
          forSpeed = forReg;
          revSpeed = revReg;
          break;
        case rapid:
          forSpeed = forRap;
          revSpeed = revRap;
          break;
      }
      msg = rs485.read();
      if(msg != stopByte){
        memMsg[bufferSize] = msg;
        bufferSize++;
      }else{
        bufferSize = 0;
      }
      process(msg);
      break;
    case FOOTER:
      Serial.println("package received"); //not sending msg to master
      break;
    default:
      if(bufferSize > 0){
        for(int i=0; i<bufferSize; i++){
        process(memMsg[i]);
        }
      }
      break;
  }
  }
