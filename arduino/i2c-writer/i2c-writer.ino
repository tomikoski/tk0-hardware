#include <Wire.h>

#define ADDR_Ax 0b000 //A2, A1, A0
#define ADDR (0b1010 << 3) + ADDR_Ax
#define MAX 255

char message[MAX] = "DEADBEEF RULES 2022";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();

  for(byte i=0; i<strlen(message); i++) {
   writeI2CByte(i, (byte) message[i]);
  }

  Serial.println("Write done");
  Serial.print(strlen(message), DEC); Serial.println(" bytes");
  delay(500);
  
  for(byte i=0; i<strlen(message); i++) {
   Serial.println( (char) readI2CByte(i));
  }

  Serial.println("Read done");

  Wire.end();
  Serial.end();
}

void loop() {
  // put your main code here, to run repeatedly:
  
}

void writeI2CByte(byte data_addr, byte data){
  Wire.beginTransmission(ADDR);
  Wire.write(data_addr);
  Wire.write(data);
  delay(500);
  Wire.endTransmission();
}

byte readI2CByte(byte data_addr){
  byte data = 0;
  Wire.beginTransmission(ADDR);
  Wire.write(data_addr);
  Wire.endTransmission();
  Wire.requestFrom(ADDR, 1); //retrieve 1 returned byte
  delay(1);
  if(Wire.available()){
    data = Wire.read();
  }
  return data;
}
