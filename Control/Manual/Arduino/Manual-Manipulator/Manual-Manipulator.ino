#include "SeedHarvester.h"
#include "BallShooter.h"

// SeedHarvester pins
#define grabberPin 27
#define lifterPin 28
#define limitPin 26
#define dirPin_Seed 17
#define stepPin_Seed 16

SeedHarvester seedHarvester(grabberPin, lifterPin, limitPin, dirPin_Seed, stepPin_Seed);

// BallShooter pins
#define servoPin 2
#define limitSwitchPin 3
#define INA 12
#define INB 13
#define wheel1Pin 10
#define wheel2Pin 11
#define stepPin_Ball 18
#define dirPin_Ball 19

BallShooter ballShooter(servoPin, limitSwitchPin, INA, INB, wheel1Pin, wheel2Pin, stepPin_Ball, dirPin_Ball);

void setup() {
  //VDO Filiming purpose
  //Harvest Button
  seedHarvester.setZero();
  seedHarvester.linearDrive(455, LOW);
  seedHarvester.grabbing();
  delay(5000);  // comment this line
  //Release Button 

  // More specific with the command. what dose x do? what dose B,A,Y do?
  seedHarvester.release();

  // Example usage for joystick
  // seedHarvester.singleHarvest();
  // seedHarvester.singleHarvest();
  // seedHarvester.singleHarvest();

  // ballShooter.servo();
  // ballShooter.wheel();
  // delay(1000);
  // while (digitalRead(BallShooter::limit_switch) == 1) {      //Need to use getter setter because its private.
  //   ballShooter.stepper_cw();
  // }
  // ballShooter.wheel_stop();
  // if (digitalRead(BallShooter::limit_switch) == 0) {  //Need to use getter setter because its private.
  //   ballShooter.stepper_stop();
  //   ballShooter.stepper_ccw();
  // }
}

void loop() {
}
