#include <Arduino.h>


int pins[5] = {6,9,10,11,12};

void parse_message(String message) {
  Serial.print("OK: ");
  Serial.print(message);
  Serial.println(" >");

  for (int i=0;i<message.length();i++) {
    if (message[i]=='0'){
      digitalWrite(pins[i],LOW);
    }
    else if (message[i]=='1') {
      digitalWrite(pins[i],HIGH);
    }
    
  }

}

void setup() {
  
  // put your setup code here, to run once:
  pinMode(6,OUTPUT);
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

    // Serial.println(incomingMessage[0]);
    if (incomingMessage.length() == 5){
    
      parse_message(incomingMessage);
      
    }

    else {
      Serial.print("Invalid Command: ");
      Serial.print(incomingMessage);
      Serial.println(" >");
    }




    // Serial.print(" I received:");

    // Serial.println(incomingMessage);

}
}