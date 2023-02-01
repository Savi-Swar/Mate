#include <Servo.h>
//thruster
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
// cameras
Servo servo7;
Servo servo8;
Servo servo9;
Servo servo10;

 int servo7_pos = 0;
 int servo8_pos = 0;
 int servo9_pos = 0;
 int servo10_pos = 0;
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
servo1.attach(2);
servo2.attach(3);
servo3.attach(4);
servo4.attach(5);
servo5.attach(6);
servo6.attach(7);
servo7.attach(8);
servo8.attach(9);
servo9.attach(10);
servo10.attach(11);


}

void loop() {


  if (Serial.available() > 0) {
    String x =Serial.readString();
    if (x.equals("FORWARD")) {
       servo3.writeMicroseconds(1750);
       servo4.writeMicroseconds(1750);
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo5.writeMicroseconds(1500);
       servo6.writeMicroseconds(1500);
    }
    if (x.equals("UP")) {
       servo5.writeMicroseconds(1250);
       servo6.writeMicroseconds(1250);
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);    
       }
    if (x.equals("DOWN")) {
       servo5.writeMicroseconds(1750);
       servo6.writeMicroseconds(1750);
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);    }
    if (x.equals("LEFT")) {
       servo1.writeMicroseconds(1750);
       servo3.writeMicroseconds(1750);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds(1500);
       servo5.writeMicroseconds(1500);
       servo6.writeMicroseconds(1500);       }
    if (x.equals("RIGHT")) {
       servo2.writeMicroseconds(1750);
       servo4.writeMicroseconds(1750);
       servo1.writeMicroseconds(1500);
       servo3.writeMicroseconds(1500);
       servo5.writeMicroseconds(1500);
       servo6.writeMicroseconds(1500);    
      }
    if (x.equals("BACKWARD")) {
       servo1.writeMicroseconds(1750);
       servo2.writeMicroseconds(1750);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);
       servo5.writeMicroseconds(1500);
       servo6.writeMicroseconds(1500);
    }
    if (x.equals("OFF")) {
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);
       servo5.writeMicroseconds(1500);
       servo6.writeMicroseconds(1500);
    }
    if (x.equals("CAMUP")) {
      servo7_pos++;
      if (servo7_pos > 50) {
        servo7_pos = 50;
      }
      servo7.write(servo7_pos);
                        }
    if (x.equals("CAMDOWN")) {  
          servo7_pos--;
      if (servo7_pos < 0) {
        servo7_pos = 0;
      }
      servo7.write(servo7_pos);
                        }
    if (x.equals("CLAWIN")) {
          servo8_pos--;
        if (servo8_pos < 0) {
        servo8_pos = 0;
      }
      servo7.write(servo7_pos);
                        }
                        }
    if (x.equals("CLAWOUT")) {
       servo8_pos++;
      if (servo8_pos > 50) {
        servo8_pos = 50;
      }  
       servo8.write(servo8_pos);
 
                        }
    if (x.equals("CLAWLEFT")) {
       servo9_pos++;
      if (servo9_pos < 0) {
        servo9_pos = 0;
      }  
       servo9.write(servo9_pos);
      
                        }
    if (x.equals("CLAWRIGHT")) { 
        servo9_pos++;
      if (servo9_pos > 180) {
        servo9_pos = 180;
      }  
       servo9.write(servo9_pos); 
                        }
    if (x.equals("CLAWUP")) {
       servo10_pos++;
      if (servo10_pos > 180) {
        servo10_pos = 180;
      }  
       servo8.write(servo10_pos);
                        }
    if (x.equals("CLAWDOWN")) {   
       servo10_pos++;
      if (servo10_pos < 0) {
        servo10_pos = 0;
      }  
       servo9.write(servo9_pos);
                        }

  }

} 
