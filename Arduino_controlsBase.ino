#include <Servo.h>
//thruster
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
// servo motors
Servo servo6;
Servo servo7;
Servo servo8;
Servo servo9;
Servo servo10;

 int servo7_pos = 0;
 int servo8_pos = 0;
 int servo9_pos = 0;
 int servo10_pos = 0;
 int minSpeed = 1200;
 int maxSpeed = 1800;
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
servo1.attach(2);
servo2.attach(3);
servo3.attach(4);
servo4.attach(5);
servo5.attach(6);
servo7.attach(8);
servo8.attach(9);
servo9.attach(10);
servo10.attach(11);


}

void loop() {


  if (Serial.available() > 0) {
    String x =Serial.readString();
    if (x.equals("FORWARD")) {
       servo1.writeMicroseconds(maxSpeed);
       servo2.writeMicroseconds(maxSpeed);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);
       servo5.writeMicroseconds(1500);
    }
    if (x.equals("UP")) {
       servo5.writeMicroseconds(maxSpeed);
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds((maxSpeed-1500)/2 + 1500);
       servo4.writeMicroseconds((maxSpeed-1500)/2 + 1500);    
       }
    if (x.equals("DOWN")) {
       servo5.writeMicroseconds(minSpeed);
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds((minSpeed-1500)/2 + 1500);
       servo4.writeMicroseconds((minSpeed-1500)/2 + 1500); 
          }
    if (x.equals("LEFT")) {
       servo5.writeMicroseconds(1500);
       servo1.writeMicroseconds(maxSpeed);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);    
        }
    if (x.equals("RIGHT")) {
       servo5.writeMicroseconds(1500);
       servo2.writeMicroseconds(maxSpeed);
       servo1.writeMicroseconds(1500);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);  
      }
    if (x.equals("BACKWARD")) {
       servo1.writeMicroseconds(minSpeed);
       servo2.writeMicroseconds(minSpeed);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);
       servo5.writeMicroseconds(1500);
    }
    if (x.equals("OFF")) {
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds(1500);
       servo4.writeMicroseconds(1500);
       servo5.writeMicroseconds(1500);
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

    if (x.equals(1) {   
      maxSpeed++;
      minSpeed--;
                  }
    if (x.equals(2) {   
      maxSpeed--;
      minSpeed++;
    }
    if (x.equals("TiltUp")) {
       servo5.writeMicroseconds(maxSpeed);
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds(minSpeed);
       servo4.writeMicroseconds(minSpeed);    
       }
    if (x.equals("TiltDown")) {
       servo5.writeMicroseconds(minSpeed);
       servo1.writeMicroseconds(1500);
       servo2.writeMicroseconds(1500);
       servo3.writeMicroseconds(maxSpeed);
       servo4.writeMicroseconds(maxSpeed); 
          }

    
          
      

  }

} 
