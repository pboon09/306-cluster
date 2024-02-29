#ifndef SEEDHARVESTER_H
#define SEEDHARVESTER_H

#include <Servo.h>

class SeedHarvester {
public:
    SeedHarvester(int gpin, int lfpin, int limitpin);
    void linearDrive(double dis, int dir);
    void setZero();
    void grabbing();
    void release();
    void harvest(int n);
    void singleHarvest();

private:
    int gap = 60; // Distance between seeds
    int gpin_;
    int lfpin_;
    int limitpin_;
    int manual_n = 0;
    int manual_hv_dis = 455;
    int manual_drop_dis = 395;
    Servo GrabServo;
    Servo LiftServo;
};

#endif // SEEDHARVESTER_H
