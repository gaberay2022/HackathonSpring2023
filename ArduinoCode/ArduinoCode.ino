#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
String myCmd;
int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(115200);
  myservo.attach(12);// attaches the servo on pin 9 to the servo object
}

void loop() {
  while(Serial.available()==0){

  }
  myCmd=Serial.readStringUntil('\r');
  if(myCmd=="1"){
    for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15ms for the servo to reach the position
    }
    for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(1);                       // waits 15ms for the servo to reach the position
    }
  }
}