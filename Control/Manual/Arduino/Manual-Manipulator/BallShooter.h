#ifndef BALL_SHOOTER_H
#define BALL_SHOOTER_H

#include <Servo.h>

class BallShooter {
public:
    BallShooter();
    void servo();
    void limitswitch();
    void stepper_cw();
    void stepper_ccw();
    void stepper_stop();
    void motor();
    void motor_stop();
    void wheel();
    void wheel_stop();

private:
    static const int servoPin = 2;
    static const int limit_switch = 3;
    static const int motor1 = 4;
    static const int motor2 = 5;
    static const int wheel1 = 8;
    static const int wheel2 = 9;
    static const int stepPin = 18;
    static const int dirPin = 19;
    static const int stepsPerRevolution = 200;
    Servo s;
};

#endif // BALL_SHOOTER_H
