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
    double rpt = dis / 0.285;
    for (int i = 0; i < rpt; i++) {
        digitalWrite(dir_pin, dir);
        digitalWrite(step_pin, HIGH);
        delayMicroseconds(600);
        digitalWrite(step_pin, LOW);
        delayMicroseconds(600);
    }
    delay(500);
}

void SeedHarvester::setZero() {
    while (digitalRead(limitpin_) == 1) {
        digitalWrite(dir_pin, Rdir);
        digitalWrite(step_pin, HIGH);
        delayMicroseconds(600);
        digitalWrite(step_pin, LOW);
        delayMicroseconds(600);
    }
    delay(500);
}

void SeedHarvester::grabbing() {
    GrabServo.write(0);
    delay(1000);
    LiftServo.writeMicroseconds(3000);
    delay(1200);
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

void SeedHarvester::singleHarvest_locking(){
    if(storage == 6){
        return;
      }
      if(storage == 5){
        delay(500);
        GrabServo.write(180);
        linearDrive(manual_lock_dis,Ldir);
        grabbing();
        linearDrive(manual_lock_dis - gap,Rdir);
        manual_lock_dis = manual_lock_dis - gap;
        storage = storage + 1;
        return;
      }
      if(storage > 0){
        // grabbing stage
        delay(500);
        GrabServo.write(180);
        linearDrive(manual_lock_dis,Ldir);
        grabbing();
        linearDrive(manual_lock_dis - gap,Rdir);

        LiftServo.writeMicroseconds(0);
        delay(100); 
        LiftServo.writeMicroseconds(1499);
        delay(200); 
        
        manual_lock_dis = manual_lock_dis - gap;
        storage = storage + 1;
      }
      else{
        // grabbing stage
        delay(500);
        GrabServo.write(180);
        linearDrive(manual_lock_dis,Ldir);
        grabbing();
        setZero();
        
        LiftServo.writeMicroseconds(0);
        delay(100); 
        LiftServo.writeMicroseconds(1499);
        delay(200); 
        
        storage = storage + 1;
      }
}

void SeedHarvester::singleRelease(){
    if (storage == 0){
        return;
      }
      if (storage == 1){
        setZero();

        LiftServo.writeMicroseconds(3000);
        delay(350); // Wait for 1 second
        LiftServo.writeMicroseconds(1499);
        delay(500);
        
        linearDrive(manual_lock_dis,Ldir);
        release();
        delay(200);
        setZero();
        storage = storage + 1;
      }
      else if(storage == 6){
        linearDrive(manual_lock_dis,Ldir);
        release();
        delay(200);
        linearDrive(gap + manual_lock_dis,Rdir);
        GrabServo.write(grbAng);
        manual_lock_dis = manual_lock_dis + gap;
        storage = storage - 1;
      }
      else{
        LiftServo.writeMicroseconds(3000);
        delay(350); // Wait for 1 second
        LiftServo.writeMicroseconds(1499);
        delay(500);
        
        linearDrive(manual_lock_dis,Ldir);
        release();
        delay(200);
        linearDrive(gap + manual_lock_dis,Rdir);
        GrabServo.write(grbAng);
        manual_lock_dis = manual_lock_dis + gap;
        storage = storage - 1;
      }
}
//um