#include <Servo.h> // import servo library
#include <NewPing.h> // import sonar sensor library
#include <LiquidCrystal.h> // import lcd library
#define ECHO_PIN 9 // set echo pin for sonar
#define TRIGGER_PIN 8 // set trigger pin for sonar
#define MAX_DISTANCE 400 //set maximum distance of sonar in cm

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); //Create new sonar object

Servo myservo;  // create servo objects to control a servo
Servo myservo2;
Servo myservo3;

String myCmd; //create string to take in python values


LiquidCrystal lcd(7, 6, 5, 4, 3, 2); //LCD oject

void setup() {
  Serial.begin(115200); // set baud
  lcd.begin(16,2); //set dimensions of lcd
  myservo.attach(13); //attach servo on pins
  myservo2.attach(12);
  myservo3.attach(10);
}

void loop() {
  while(Serial.available()==0){ //loop when not taking in input
    lcd.clear(); // clear lcd screen
    lcd.setCursor(0, 0); // set lcd cursor back to start
    lcd.print("Have a good Day!"); // print text to lcd
    myservo.write(10); //move servos to angle position
    myservo2.write(10);
    myservo3.write(10);
    delay(1000); // 1 second delay
    Serial.print(sonar.ping_cm()); //output echolocation data as distance from object to sensor in cm
    Serial.print("\r\n"); // formating for delminiation in python file and nice out for distance
  }
  
  myCmd=Serial.readStringUntil('\r'); //set the myCmd string to our python data
  if(myCmd=="0"){ //python input of 0 (Compost)
        lcd.clear(); // clear lcd
        lcd.setCursor(0, 0); // set lcd cursor to start
        lcd.print("Compost"); // print text to lcd
        myservo.write(360);   //move servo to angle position
        delay(3000);  // 3s delay

  }
  if(myCmd=="1"){ //python input of 1 (Trash)
        lcd.clear(); // clear lcd
        lcd.setCursor(0, 0); // set lcd cursor to start
        lcd.print("Trash"); // print text to lcd
        myservo2.write(360); // move servo to angle position
        delay(3000); // 3s delay
  }
  if(myCmd=="2"){ // python input of 2 (Recycle)
        lcd.clear(); // clear lcd
        lcd.setCursor(0, 0); // set lcd position to start
        lcd.print("Recycle"); // print text to lcd
        myservo3.write(360);     // move servo to angle position
        delay(3000);  // 3s delay
  }
   if(myCmd=="3"){ // python input of 3 for people (default mode incase people get to close)
        myservo.write(10);    // move servo to angle position
        myservo2.write(10);       
        myservo3.write(10);        
        delay(1);  
   }
}