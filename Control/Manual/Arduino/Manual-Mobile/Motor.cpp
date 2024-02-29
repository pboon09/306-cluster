#include "Arduino.h"
#include "Motor.h"

Motor::Motor(int encoderPin, int INA_PIN, int INB_PIN, double kp, double ki, double kd)
  : encoder(encoderPin), _INA_PIN(INA_PIN), _INB_PIN(INB_PIN), _kp(kp), _ki(ki), _kd(kd) {
  pinMode(_INA_PIN, OUTPUT);
  pinMode(_INB_PIN, OUTPUT);
}

void Motor::setSpeed(int speed) {
  if (speed > 0) {
    analogWrite(_INA_PIN, speed);
    digitalWrite(_INB_PIN, 0);
  } else if (speed < 0) {
    digitalWrite(_INA_PIN, 0);
    analogWrite(_INB_PIN, -speed);
  } else {
    digitalWrite(_INA_PIN, 0);
    digitalWrite(_INB_PIN, 0);
  }
}

void Motor::stop() {
  digitalWrite(_INA_PIN, LOW);
  digitalWrite(_INB_PIN, LOW);
}

void Motor::compute(float setPoint_RPM, float deltaTime) {
  if (setPoint_RPM != 0) {
    int pos = encoder.getCount();
    float velocity = (pos - _prevCount) / deltaTime;
    _v = velocity / 980 * 60;                                              //edit here
    _vFilt = 0.96906992 * _vFilt + 0.01546504 * _v + 0.01546504 * _vPrev;  //edit here

    // _ffw = 621.79 * setPoint_RPM + 2508.9;  //edit here
    // setSpeed(_ffw + _u);

    _error = setPoint_RPM - _vFilt;
    _integral += _error * deltaTime;
    float P = _kp * _error;
    float I = _ki * _integral;
    float D = _kd * (_error - _lastError) / deltaTime;
    if (_error == 0) {
      I = 0;
    }
    if (I > 62500) {
      I = 62500;
    }
    _u = P + I + D;

    _u = std::max(std::min(_u, 62500.0f), -62500.0f);

    setSpeed(_u);

    // Serial.print(setPoint_RPM);
    // Serial.print(" ");
    Serial.print(_vFilt);
    Serial.print(" ");

    _vPrev = _v;
    _prevCount = pos;
    _lastError = _error;

  } else if (setPoint_RPM == 0) {
    setSpeed(0);
  }
}

void Motor::FindSpeedFromPWM(float pwm, float deltaTime) {
  int pos = encoder.getCount();
  float velocity = (pos - _prevCount) / deltaTime;
  _v = velocity / 980 * 60;                                              //edit here
  _vFilt = 0.96906992 * _vFilt + 0.01546504 * _v + 0.01546504 * _vPrev;  //edit here

  setSpeed(pwm);

  Serial.print(_v);
  Serial.print(" ");
  Serial.print(_vFilt);
  Serial.print(" ");


  _vPrev = _v;
  _prevCount = pos;
}

void Motor::setKP(float kp) {
  _kp = kp;
}

void Motor::setKI(float ki) {
  _ki = ki;
}

void Motor::setKD(float kd) {
  _kd = kd;
}
