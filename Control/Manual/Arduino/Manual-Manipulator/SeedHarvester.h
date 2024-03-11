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
    // void harvest(int n);
    void singleHarvest_locking();
    void singleRelease();

private:
     int gap = 75; //distance between seed

    int gpin_; // grabber pin (servo)
    int lfpin_; // lifter pin (servo)
    int limitpin_; // limit pin

    int storage = 0;
    int manual_lock_dis = 470;

    int n_release = 0;
    int dir_pin = 17, step_pin = 16;

    bool Ldir = LOW, Rdir = HIGH;

    int grbAng = 10;
};

#endif // SEEDHARVESTER_H
