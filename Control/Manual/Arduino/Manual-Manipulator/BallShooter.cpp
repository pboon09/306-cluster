#include "BallShooter.h"
#include <Arduino.h>

BallShooter::BallShooter(int servoPin, int limitSwitchPin, int INA, int INB, int wheel1Pin, int wheel2Pin, int stepPin, int dirPin)
  : servoPin_(servoPin),
    limitSwitchPin_(limitSwitchPin),
    INA_(INA),
    INB_(INB),
    wheel1Pin_(wheel1Pin),
    wheel2Pin_(wheel2Pin),
    stepPin_(stepPin),
    dirPin_(dirPin) {
  s.attach(servoPin_);
  pinMode(limitSwitchPin_, INPUT_PULLUP);
  pinMode(INA_, OUTPUT);
  pinMode(INB_, OUTPUT);
  pinMode(wheel1Pin_, OUTPUT);
  pinMode(wheel2Pin_, OUTPUT);
  pinMode(stepPin_, OUTPUT);
  pinMode(dirPin_, OUTPUT);
  Serial.begin(115200);
}

void BallShooter::servo() {
  s.write(140);
  delay(2000);
  s.write(180);
  delay(2000);
  s.write(140);
  delay(2000);
}

void BallShooter::limitswitch() {
  if (digitalRead(limitSwitchPin_) == 1) {
    Serial.println("1");
  } else {
    Serial.println("0");  // trig
  }
}

void BallShooter::stepper_cw() {
  digitalWrite(dirPin_, HIGH);
  for (int i = 0; i < stepsPerRevolution; i++) {
    digitalWrite(stepPin_, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin_, LOW);
    delayMicroseconds(1000);
  }
}

void BallShooter::stepper_ccw() {
  digitalWrite(dirPin_, LOW);
  for (int i = 0; i < 4.2 * stepsPerRevolution; i++) {
    digitalWrite(stepPin_, HIGH);
    delayMicroseconds(1000);
    digitalWrite(stepPin_, LOW);
    delayMicroseconds(1000);
  }
}

void BallShooter::stepper_stop() {
  digitalWrite(dirPin_, LOW);
  for (int i = 0; i < 2 * stepsPerRevolution; i++) {
    digitalWrite(stepPin_, LOW);
    delayMicroseconds(1000);
    digitalWrite(stepPin_, LOW);
    delayMicroseconds(1000);
  }
}

void BallShooter::motor() {
  analogWrite(INA_, 255);
  digitalWrite(INB_, HIGH);
}

void BallShooter::motor_stop() {
  analogWrite(INA_, 0);
  digitalWrite(INB_, LOW);
}

void BallShooter::wheel() {
  analogWrite(wheel1Pin_, 230);
  digitalWrite(wheel1Pin_, HIGH);
}

void BallShooter::wheel_stop() {
  analogWrite(wheel1Pin_, 0);
  digitalWrite(wheel1Pin_, LOW);
}
