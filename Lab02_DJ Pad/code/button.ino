#define button 7

void setup() {
  Serial.begin(9600);
  pinMode(button, INPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  bool b = digitalRead(button);
  if(b) digitalWrite(13, HIGH);
  else digitalWrite(13, LOW);
}
