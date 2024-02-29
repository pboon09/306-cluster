#include "BallShooter.h"
#include <Arduino.h>

BallShooter::BallShooter() {
    s.attach(servoPin);
    pinMode(limit_switch, INPUT_PULLUP);
    pinMode(motor1, OUTPUT);
    pinMode(motor2, OUTPUT);
    pinMode(wheel1, OUTPUT);
    pinMode(wheel2, OUTPUT);
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
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
    if (digitalRead(limit_switch) == 1) {
        Serial.println("1");
    } else {
        Serial.println("0");  // trig
    }
}

void BallShooter::stepper_cw() {
    digitalWrite(dirPin, HIGH);
    for (int i = 0; i < stepsPerRevolution; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(1000);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(1000);
    }
}

void BallShooter::stepper_ccw() {
    digitalWrite(dirPin, LOW);
    for (int i = 0; i < 4.2 * stepsPerRevolution; i++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(1000);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(1000);
    }
}

void BallShooter::stepper_stop() {
    digitalWrite(dirPin, LOW);
    for (int i = 0; i < 2 * stepsPerRevolution; i++) {
        digitalWrite(stepPin, LOW);
        delayMicroseconds(1000);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(1000);
    }
}

void BallShooter::motor() {
    analogWrite(motor1, 50);
    analogWrite(motor2, 50);
    digitalWrite(motor1, LOW);
    digitalWrite(motor2, HIGH);
}

void BallShooter::motor_stop() {
    analogWrite(motor1, 50);
    analogWrite(motor2, 50);
    digitalWrite(motor1, LOW);
    digitalWrite(motor2, LOW);
}

void BallShooter::wheel() {
    analogWrite(wheel1, 230);
    digitalWrite(wheel1, HIGH);
}

void BallShooter::wheel_stop() {
    analogWrite(wheel1, 0);
    digitalWrite(wheel1, LOW);
}
