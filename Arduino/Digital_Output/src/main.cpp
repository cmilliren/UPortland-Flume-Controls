#include <Arduino.h>


void setup() {
  
  // put your setup code here, to run once:
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {

    String incomingMessage = Serial.readStringUntil('\n'); // read the incoming byte:

    Serial.println(incomingMessage[0]);

    if (incomingMessage[0]=='1'){
      Serial.println("turn on Pump1");
      digitalWrite(9,HIGH);
    }

    if (incomingMessage[0] == '0'){
      Serial.println("turn off Pump1");
      digitalWrite(9,LOW);
    }

    Serial.print(" I received:");

    Serial.println(incomingMessage);

}
}