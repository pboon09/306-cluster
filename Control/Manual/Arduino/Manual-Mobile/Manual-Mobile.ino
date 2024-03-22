#include "Motor.h"
#include "Kinematics.h"
#include "RPi_Pico_TimerInterrupt.h"
#include "pio_encoder.h"

//Timer Interrupt Setup
#define dt_us 2400  //Edit Here
float deltaT = dt_us / 1.0e6;
RPI_PICO_Timer Timer(0);
bool TimerStatus = false;

//Edit Here
//Motor Setup
Motor FL(8, 14, 15, 17000, 100, 100);  //correct encode pin
Motor FR(6, 10, 11, 17000, 100, 100);  //wrong encode pin
Motor BL(4, 20, 21, 17000, 100, 100);  //wrong encode pin
Motor BR(2, 12, 13, 17000, 100, 100);  //wrong encode pin
//Edit Here

float wheelDiameter = 0.127;
float lx = 0.26/2;
float ly = 0.432/2;
Kinematics kinematics(wheelDiameter, lx, ly);

//For test purpose
//variable
long start_time, T;
int currentStep = 0;
int stepsCount = 0;
bool newStepsAvailable = false;

//Transform
struct TransformStep {
  float vx;
  float vy;
  float wz;
  unsigned long duration;
};
//For test purpose

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  analogWriteFreq(2400);
  analogWriteRange(62500);

  FR.encoder.begin();
  FL.encoder.begin();
  BR.encoder.begin();
  BL.encoder.begin();

  //Timer Interrupt Setup
  TimerStatus = Timer.attachInterruptInterval(dt_us, TimerHandler);

  start_time = millis();
}

void loop() {
}

bool TimerHandler(struct repeating_timer* t) {
  (void)t;
  //debug part
  // Kinematics::Velocity speed = kinematics.Forward_Kinematics_Velocity(-138, 138, -138, 138);
  // Kinematics::RPM wheelSpeeds = kinematics.Inverse_Kinematics(0, 0, 1);
  // Serial.print(speed.vx);
  // Serial.print(" ");
  // Serial.print(speed.vy);
  // Serial.print(" ");
  // Serial.print(speed.wz);
  // Serial.println(" ");
  // Serial.print(wheelSpeeds.radps_fl);
  // Serial.print(" ");
  // Serial.print(wheelSpeeds.radps_fr);
  // Serial.print(" ");
  // Serial.print(wheelSpeeds.radps_bl);
  // Serial.print(" ");
  // Serial.print(wheelSpeeds.radps_br);
  // Serial.println(" ");

  // FL.setSpeed(10000);
  // FR.setSpeed(10000);
  // BL.setSpeed(10000);
  // BR.setSpeed(10000);

  // FL.FindSpeedFromPWM(62500, deltaT);
  // FR.FindSpeedFromPWM(62500, deltaT);
  // BL.FindSpeedFromPWM(62500, deltaT);
  // BR.FindSpeedFromPWM(62500, deltaT);
  // Serial.println();

  Kinematics::RPM wheelSpeeds = kinematics.Inverse_Kinematics(1, 1, 1);  //Set Joy to 0.92 0.92 2.65
  FL.setSpeed(map(wheelSpeeds.RPM_FL, -138, 138, -62500, 62500));
  FR.setSpeed(map(wheelSpeeds.RPM_FR, -138, 138, -62500, 62500));
  BL.setSpeed(map(wheelSpeeds.RPM_BL, -138, 138, -62500, 62500));
  BR.setSpeed(map(wheelSpeeds.RPM_BR, -138, 138, -62500, 62500));
  return true;
}