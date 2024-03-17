#ifndef SEEDHARVESTER_H
#define SEEDHARVESTER_H

#include <Servo.h>

class SeedHarvester {
public:
  SeedHarvester(int gpin, int lfpin, int limitpin, int dirPin, int stepPin);
  void linearDrive(double dis, int dir);
  void setZero();
  void grabbing();
  void release();
  // void harvest(int n);
  void singleHarvest_locking();
  void singleRelease();

private:
  int gap = 80;  //distance between seed

  int gpin_;      // grabber pin (servo)
  int lfpin_;     // lifter pin (servo)
  int limitpin_;  // limit pin
  int dir_pin_;    // Direction pin for the stepper motor
  int step_pin_;   // Step pin for the stepper motor

  int storage = 0;
  int manual_lock_dis = 455;

  int n_release = 0;

  bool Ldir = LOW, Rdir = HIGH;

  int grbAng = 5;
};

#endif  // SEEDHARVESTER_H
