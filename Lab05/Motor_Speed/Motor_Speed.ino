int in1Pin = 6;
int in2Pin = 7;
int pwmPin = 9;

void setup() {
  pinMode(pwmPin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);

  SetDirection(0);
  analogWrite(pwmPin, 0);
}

void loop() {
  analogWrite(pwmPin, 50);
  delay(2000);
  analogWrite(pwmPin, 100);
  delay(2000);
  analogWrite(pwmPin, 255);
  delay(2000);
}

void SetDirection(int dir){
  if (dir == 0){
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
  } else if (dir == 1){
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
  }
}
