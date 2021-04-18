#include <Stepper.h>
//set up all component
const int pingPin = 2; // pin4 on Atmega328
const int echoPin = 3; //pin5 on Atmega328
const int ledPin = 5;// pin11 on Atmega328
const int buzzerpin = 4; //pin6 on Atmega328
const int pResistor = A5;
// set Variables 
String nom = "Arduino";
String msg;
const int stepsPerRevolution = 200;  //num of steps per revolution
int light;
// Initialize the stepper library on pins 8 through 11:
Stepper myStepper = Stepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  Serial.begin(9600);           // start serial for output
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerpin,OUTPUT);
  myStepper.setSpeed(100);  // Set the motor speed (RPMs):
}

void readSerialPort() {
  msg = "";
  if (Serial.available()) {
    delay(10);
    while (Serial.available() > 0) {
      delay(1000);
      digitalWrite(ledPin, HIGH);
      delay(1000);
      digitalWrite(ledPin, LOW);
      msg += (char)Serial.read();
//      msg = Serial.readStringUntil('\n');

    }
    
    Serial.flush();
  }
}
void loop() {
  //set light read from pin A5
  light = analogRead(pResistor);
  
  //ultrasonic sensor 
  long duration, cm;
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(5);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(15);
  digitalWrite(pingPin, LOW);
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  cm = duration /29/2;
  
  if(cm<=10){
    delay(500);
   
      //send pi distance
      Serial.println("o");
      
      msg = "";
      //read data from pi
      while (msg == ""){
  
        readSerialPort();
      }
     delay(500);
     if(msg == "Bird"){
        
        //rotate motor to load food
        myStepper.step(100);
        delay(1000);
        myStepper.step(-100);
        
        //ligh up LED to detect food shortage
        digitalWrite(ledPin, HIGH);
        delay(3000);
        if(light > 100){
          Serial.println("f"); //send food shortage signal to Pi
          delay(500);
          }
        digitalWrite(ledPin, LOW);
        }
    
    }else{

    }
  
  

}

  
