#include <Stepper.h>
//set up all component
const int pingPin = 2; // pin4 on Atmega328
const int echoPin = 3; //pin5 on Atmega328
const int ledPin = 5;// pin11 on Atmega328
const int buzzerpin = 4; //pin6 on Atmega328
const int pResistor = A5;
// set Variables 
bool object_detected = false; //initialize the object flag
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
    object_detected = true;
    //test if cm<10T
    tone(buzzerpin,35000);
    delay(1000);
    noTone(buzzerpin);
//    Serial.println(object_detected); //send object detected signal to Pi
    myStepper.step(100);
    delay(1000);
    myStepper.step(-100);
    }
  else if(light <50){
//    object_detected = false;
//    Serial.println("false"); //send object detected signal to Pi
    Serial.print(light);
      digitalWrite(ledPin, HIGH);
      delay(3000);
      digitalWrite(ledPin, LOW);
    }
  
  delay(1000);

}

  
