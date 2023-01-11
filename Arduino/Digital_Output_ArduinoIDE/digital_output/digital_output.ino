#include <Arduino.h>


int pins[5] = {6,9,10,11,12};
String state = String("00000");

String parse_command(String message, String state_p) {
  Serial.print("Received Valid Message: ");
  Serial.print(message);
  Serial.println(">");

  // state = message;

  // routine for pump control (bits 0-3)
  for (int i=0;i<message.length()-1;i++) {
    if (message[i]=='0'){
      digitalWrite(pins[i],LOW);
      state_p[i] = '0';
    }
    else if (message[i]=='1') {
      digitalWrite(pins[i],HIGH);
      state_p[i] = '1';
    }
    
  }
  // routine for sedflux dump (bit 4)
  if (message[4] == '1' && state[4] != '2'){ // if bit 4 of the incoming message is 1 then a dump is requested
    digitalWrite(pins[4],LOW);
    delay(25); // delay 25 milliseconds
    digitalWrite(pins[4],HIGH);
    state_p[4] = '0';
  }
  else if (message[4] == '2') { // if bit 4 of the incoming message is 2 then the motor should be disabled. 
    digitalWrite(pins[4],LOW);
    state_p[4]='2';
  }

  else if (message[4] == '0') {
   digitalWrite(pins[4], HIGH);
   state_p[4] = '0';
  }
  return state_p;
}

void parse_poll(String message,String state_string) {
  if (message == "p") {
    Serial.print(state_string);
    Serial.println(">");
  }
  

}

void setup() {

  // state = '00000';
  
  // put your setup code here, to run once:
  pinMode(6,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(12,OUTPUT);

  digitalWrite(6,LOW);
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  digitalWrite(12,HIGH);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {

    String incomingMessage = Serial.readStringUntil('\n'); // read the incoming byte:

    // Serial.println(incomingMessage[0]);
    if (incomingMessage.length() == 5){ // IF message is 5 characters long its a command to turn on or off digital outputs
      // String state = incomingMessage;
      state = parse_command(incomingMessage,state);
      
    }

    else if (incomingMessage.length() == 1) { // if the message is only 1 character long its a poll for status
      parse_poll(incomingMessage,state);
    }

    else { // the message is neither 1 character or 5 characters is an invalid command
      Serial.print("Invalid Command: ");
      Serial.print(incomingMessage);
      Serial.println(" >");
    }




    // Serial.print(" I received:");

    // Serial.println(incomingMessage);

}
}