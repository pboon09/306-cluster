#ifndef BALL_SHOOTER_H
#define BALL_SHOOTER_H

#include <Servo.h>

class BallShooter {
public:
    BallShooter(int servoPin, int limitSwitchPin, int INA, int INB, int wheel1Pin, int wheel2Pin, int stepPin, int dirPin);
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
    Servo s;
    int servoPin_;
    int limitSwitchPin_;
    int INA_;
    int INB_;
    int wheel1Pin_;
    int wheel2Pin_;
    int stepPin_;
    int dirPin_;
    static const int stepsPerRevolution = 200;
};

#endif // BALL_SHOOTER_H
