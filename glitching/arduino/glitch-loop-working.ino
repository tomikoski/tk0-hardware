// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

volatile int locked = 1;
long int counter = 0;
char tempstr[50];

void loop() {  
  while (locked){
    sprintf(tempstr, "Loop 1, counter=%d\n\r", counter);
    Serial.print(tempstr);
    volatile long int k=0;
    for (volatile long int i=0;i<99999;i++)
       k++;
    locked = (k==99999);
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(10);                         // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(10);                         // wait for a second
    counter++;
  } 
  locked = 1;
  counter = 0;
  while (locked){
    sprintf(tempstr, "Loop 2, counter=%d\n\r", counter);
    Serial.print(tempstr);

    volatile long int j=0;
    for (volatile long int i=0;i<99999;i++)
       j++;
    locked =(j==99999);
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(1000);                         // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(1000);                         // wait for a second    
    counter++;
  }
  locked = 1;
  counter = 0;
  while (locked){
    sprintf(tempstr, "Glitched! %s, counter=%d\n\r", "Flag {123123123}", counter);
    Serial.print(tempstr);
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(3000);                         // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(3000);                         // wait for a second
    counter++;
  }
}
