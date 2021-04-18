#include <Stepper.h>

#define trigPin 2                // ultrasonic sensor trig pin
#define echoPin 3                // ultrasonic sensor echo pin
#define buzzerPin 4               // buzzer pin
#define ledPin 5
#define BUZZER_FREQUENCY 1000     // buzzer frequency
#define TIME_B 1000      
const int pResistor = A5;
String nom = "Arduino";
String msg;
const int stepsPerRevolution = 200;  //num of steps per revolution
int light;
long duration, distance;
Stepper myStepper = Stepper(stepsPerRevolution, 8, 9, 10, 11);

//for food shortage detect 
unsigned long previousMillis = 0;       
const unsigned long interval = 2UL*60UL*60UL*1000UL;

void setup() {
  Serial.begin(9600);           
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin,OUTPUT);
  myStepper.setSpeed(100); 
}

void detect_food(){
  digitalWrite(ledPin, HIGH);
  delay(3000);
  if(light > 100){
  Serial.println("f"); //send food shortage signal to Pi
  delay(500);
  }
  digitalWrite(ledPin, LOW);
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
  
  pinMode(trigPin, OUTPUT);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(15);
  digitalWrite(trigPin, LOW);
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  distance = duration /29/2;

  light = analogRead(pResistor);
  //if >2hr, detect food
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis += interval;
    detect_food();
  }
  //detect bird
  else if(distance<10){
    delay(500);
    Serial.println("o");
    msg = "";
    
    //get detection result
    while (msg == ""){
      readSerialPort();
      }
      
    if(msg == "B"){
      myStepper.step(100);
      delay(1000);
      myStepper.step(-100);
      digitalWrite(ledPin, HIGH);
      delay(1000);
      digitalWrite(ledPin, LOW);
    }
    else if(msg == "S"){
      tone(buzzerPin, 35000);
      delay(3000);
      noTone(buzzerPin);
    }
  }
}
