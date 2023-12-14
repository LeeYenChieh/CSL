/***************************************************************/
/* Sample code for CSL final project                           */
/* Demonstrating 1) IR sensor, 2) Servo motor, and 3) DC Motor */
/***************************************************************/

// All grounds (GND) should be connected
// After finishing prototyping, you can power Nano by connecting a 9V battery to Vin pin 


// 2.5cm above the track, x < 100 = white, 500 < x < 900 = black, 100 < x < 500 = gray (outside the track, used for turning), x > 900 = air
// per stripe: 30mm wide, 20mm long.
// stop for 3s every 10 stripes
// width of sensor: 15mm

/***** IR Sensor *****/
#define ir_sensor1 A1 // A0 pin on the sensor
#define ir_sensor2 A2
#define ir_sensor3 A3
// Vcc -> 5V
// GND -> GND

/***** Track *****/
#define WHITE 0
#define BLACK 1
#define GREY 2
#define AIR 3

#define LEFT 0
#define MID 1
#define RIGHT 2

int stripCount = 0;
int prevTrack;
int stopTime = 0;

/***** Servo Motor *****/
#define servo_pin 11 // PWM pin (orange)
// Red -> 5V
// Brown -> GND

#include <Servo.h>
Servo myservo;
int servo_output = 0;

/***** DC Motor (L298N) *****/
#define ENA 5 // (pwm)
#define IN1 6
#define IN2 7
// +12V -> (+) of 9V battery
// GND -> GND
// OUT1 & OUT2 -> DC Motor

#define FORWARD 0
#define BACKWARD 1

// int dc_dir = 0;
// int dc_output = 255;
int highSpeed = 255;
int lowSpeed = 50;
int backSpeed = 100;
int currentSpeed = highSpeed;
int highSpeedTime = 300;
int lowSpeedTime = 600;
int switchTime = highSpeedTime; // switch between high spd and low spd to slow down

// degree
// track3: 26, 103, 179
// usual: 65, 103, 140
int straightDegree = 90;
int leftDegree = 50;
int rightDegree = 130;
int currentDegree = straightDegree;

// states
#define GOSTRAIGHT 0
#define TURNLEFT 1
#define TURNRIGHT 2
int state = GOSTRAIGHT;

// frame rate
int delayTime = 1;

void setup() {
  /****** IR Sensor ******/
  pinMode(ir_sensor1, INPUT);
  pinMode(ir_sensor2, INPUT);
  pinMode(ir_sensor3, INPUT);

  /***** Servo Motor *****/
  pinMode(servo_pin, OUTPUT);
  myservo.attach(servo_pin);

  /** DC Motor (L298N) ***/
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  // setDirection(dc_dir);
  // analogWrite(ENA, dc_output);
  
  Serial.begin(38400);
}

void loop() {
  // myservo.write((servo_output += 10) % 180);
  // delay(1000);

  /* Read from the IR Sensor */
  int left = analogRead(ir_sensor1);
  int mid = analogRead(ir_sensor2);
  int right = analogRead(ir_sensor3);
  if(stopTime <= 0)
    Serial.println("Left: " + (String)left + ", Mid: " + (String)mid + ", Right: " + (String)right + ", currentDegree: " + (String)currentDegree);

  /* Rotate the servo motor (by degree) */
  int leftTrack = getTrackType(left, LEFT);
  int midTrack = getTrackType(mid, MID);
  int rightTrack = getTrackType(right, RIGHT);

  int on_track = 1 - notOnTrack(leftTrack, midTrack, rightTrack);

  if(on_track == 1)
    adjustState(leftTrack, midTrack, rightTrack);
  if(state == TURNLEFT)
    currentDegree = max(currentDegree - 1, leftDegree);
  else if(state == TURNRIGHT)
    currentDegree = min(currentDegree + 1, rightDegree);
  else if(state == GOSTRAIGHT)
    currentDegree = towardsStraight(currentDegree);

  myservo.write(currentDegree);

  if(stopTime > 0 && ((midTrack == BLACK && prevTrack == WHITE) || (midTrack == WHITE && prevTrack == BLACK)))
  {
    stripCount++;
    prevTrack = midTrack;
  }

  if(stripCount == 20)
  {
    // stop
    Serial.println("Stop");
    stripCount = 0;
    stopTime = 3000;
    // reset currentSpeed to highSpeed to boost start
    currentSpeed = highSpeed;
    switchTime = highSpeedTime;
  }

  /* Set DC motor direction and power */
  if(on_track == 0 || stopTime > 0)
  {
    // speed = 0
    analogWrite(ENA, 0);
  }
  else
  {
    // move
    setDirection(FORWARD);
    analogWrite(ENA, currentSpeed);
    Serial.println("CurrentSpeed: " + String(currentSpeed));
    switchTime -= (delayTime + 4);
    if(switchTime < 0)
    {
      if(currentSpeed == highSpeed)
      {
        currentSpeed = lowSpeed;
        switchTime = lowSpeedTime;
      }
      else
      {
        currentSpeed = highSpeed;
        switchTime = highSpeedTime;
      }
    }
  }
  
  // if(stopTime <= 0)
  //   goBackIfNeeded();
  
  // loop time is about 4ms
  stopTime -= (delayTime + 4);
  delay(delayTime);
}

void setDirection(int dir){
  // 0 = forward, 1 = backward
  if (dir == 0){
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
  } else if (dir == 1){
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
  }
}

int getTrackType(int value, int direction) {
    // direction: mid = 0, left = 1, right = 2
    if(direction == LEFT || direction == MID)
    {
      if(value < 38)
          return WHITE;
      else if(value < 100)
          return GREY;
      else if(value < 800)
          return BLACK;
      else
          return AIR;
    }
    else
    {
      if(value < 50)
        return WHITE;
      else if(value < 300)
        return GREY;
      else if(value < 800)
        return BLACK;
      else
        return AIR;
    }
}

int notOnTrack(int leftTrack, int midTrack, int rightTrack)
{
  if((leftTrack == GREY || leftTrack == AIR) && 
  (midTrack == GREY || midTrack == AIR) && 
  (rightTrack == GREY || rightTrack == AIR))
    return 1;
  return 0;
}

void adjustState(int leftTrack, int midTrack, int rightTrack)
{
  if(leftTrack != GREY)
    state = TURNLEFT;
  else if(rightTrack != GREY)
    state = TURNRIGHT;
  else if(midTrack != GREY)
    state = GOSTRAIGHT;
  // else
  // {
  //   if(state == TURNLEFT)
  //     state = TURNRIGHT
  //   else if(state == TURNRIGHT)
  //     state = TURNLEFT;
  // }
}

int towardsStraight(int degree)
{
  if(degree < straightDegree)
    return degree + 1;
  else if(degree > straightDegree)
    return degree - 1;
  else
    return degree;
}

void goBackIfNeeded()
{
  int leftTrack = getTrackType(analogRead(ir_sensor1), LEFT);
  int midTrack = getTrackType(analogRead(ir_sensor2), MID);
  int rightTrack = getTrackType(analogRead(ir_sensor3), RIGHT);
  while(leftTrack == GREY && midTrack == GREY && rightTrack == GREY)
  {
    setDirection(BACKWARD);
    // myservo.write(straightDegree);
    analogWrite(ENA, backSpeed);

    leftTrack = getTrackType(analogRead(ir_sensor1), LEFT);
    midTrack = getTrackType(analogRead(ir_sensor2), MID);
    rightTrack = getTrackType(analogRead(ir_sensor3), RIGHT);
  } 
}
