#define button 7
#define volume A4
#define led 9
bool prev_b = 0;
int prev_v = 0;
bool flag = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(button, INPUT);
  pinMode(volume, INPUT);
  pinMode(13, OUTPUT);
  pinMode(led, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  bool b = digitalRead(button);
  int v = analogRead(volume);
//  float temp = v;
//  temp /= 1023;
//  if(temp < 0.2)
//    flag = 0;
//  else
//    flag = 1;
  if (b) digitalWrite(13, HIGH);
  else digitalWrite(13, LOW);
  
  if(prev_b != b && b){
    Serial.print("b\n");
    if(flag)
      flag =0;
    else
      flag=1;
  }
  if(!flag){
    digitalWrite(led, LOW);
  }else{
    float light = v;
    light = light * 255 / 1023;
    analogWrite(led,(int)light);
//    digitalWrite(led, HIGH);
//    delay(1);
//    digitalWrite(led,LOW);
//    delay((int)light);
  }
  prev_b = b;
  
  if(abs(prev_v - v) > 60){
    Serial.print("v\n");
    Serial.println(v);
    if((float) v / 1023 < 0.2)
      flag = 0;
    else
      flag = 1;
    prev_v = v;
  }
  
  delay(10);
}
