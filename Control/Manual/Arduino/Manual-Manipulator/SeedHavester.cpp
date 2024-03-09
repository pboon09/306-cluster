#include "SeedHarvester.h"
#include <Arduino.h>

SeedHarvester::SeedHarvester(int gpin, int lfpin, int limitpin) {
    gpin_ = gpin;
    lfpin_ = lfpin;
    limitpin_ = limitpin;
    pinMode(dir_pin, OUTPUT);            //unknow varieble because its not in this file!! (there are more than this please check)
    pinMode(step_pin, OUTPUT);
    pinMode(limitpin_, INPUT_PULLUP);
    GrabServo.attach(gpin_);
    LiftServo.attach(lfpin_);
    GrabServo.write(180);
    setZero();
}

void SeedHarvester::linearDrive(double dis, int dir) {
    double rpt = dis / 0.161;
    for (int i = 0; i < rpt; i++) {
        digitalWrite(dir_pin, dir);
        digitalWrite(step_pin, HIGH);
        delayMicroseconds(500);
        digitalWrite(step_pin, LOW);
        delayMicroseconds(500);
    }
    delay(500);
}

void SeedHarvester::setZero() {
    while (digitalRead(limitpin_) == 1) {
        digitalWrite(dir_pin, Rdir);
        digitalWrite(step_pin, HIGH);
        delayMicroseconds(500);
        digitalWrite(step_pin, LOW);
        delayMicroseconds(500);
    }
    delay(500);
}

void SeedHarvester::grabbing() {
    GrabServo.write(0);
    delay(1000);
    LiftServo.writeMicroseconds(3000);
    delay(1000);
    LiftServo.writeMicroseconds(1499);
    delay(500);
}

void SeedHarvester::release() {
    LiftServo.writeMicroseconds(0);
    delay(1000);
    LiftServo.writeMicroseconds(1499);
    delay(1000);
    GrabServo.write(180);
    delay(500);
}

void SeedHarvester::harvest(int n) {
    int hv_dis = 455; // Harvesting location
    int drop_dis = 395; // Dropping location
    linearDrive(455, Ldir);
    grabbing();
    linearDrive(455, Rdir);
    GrabServo.write(180);
    delay(500);

    if (n > 1) {
        for (int i = 0; i < n; i++) {
            linearDrive(hv_dis, Ldir);
            grabbing();
            linearDrive(drop_dis, Rdir);
            GrabServo.write(180);
            delay(500);
            drop_dis -= gap;
            hv_dis -= gap;
        }
    }
    setZero();
}

void SeedHarvester::singleHarvest() {
    if (manual_n > 0) {
        linearDrive(manual_hv_dis, Ldir);
        grabbing();
        linearDrive(manual_drop_dis, Rdir);
        GrabServo.write(180);
        delay(500);
        manual_drop_dis -= gap;
        manual_hv_dis -= gap;
        manual_n++;
    } else {
        linearDrive(455, Ldir);
        grabbing();
        linearDrive(455, Rdir);
        GrabServo.write(180);
        delay(500);
        manual_n++;
    }
    if (manual_n == 6) {
        setZero();
        manual_n = 0;
    }
}
