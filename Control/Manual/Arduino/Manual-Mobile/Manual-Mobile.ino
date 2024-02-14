#include "Motor.h"
#include "Kinematics.h"
#include "RPi_Pico_TimerInterrupt.h"
#include "pio_encoder.h"

//Timer Interrupt Setup
#define dt_us 1000  //Edit Here
float deltaT = dt_us / 1.0e6;
RPI_PICO_Timer Timer(0);
bool TimerStatus = false;

//Edit Here
//Motor Setup
Motor FL(0, 4, 5, 30000, 100, 0);
Motor FR(14, 2, 3, 30000, 100, 0);
Motor BL(18, 6, 7, 30000, 100, 0);
Motor BR(16, 8, 9, 30000, 100, 0);
//Edit Here

//Edit Here
float wheelDiameter = 0.1;
float lx = 0.2;
float ly = 0.2;
Kinematics kinematics(wheelDiameter, lx, ly);
//Edit Here


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

  // if (Serial.available()) {
  //   String data = Serial.readStringUntil('\n');
  //   // Serial.print("Received data: ");
  //   // Serial.println(data);

  //   int firstSemiColon = data.indexOf(';');
  //   int secondSemiColon = data.indexOf(';', firstSemiColon + 1);

  //   vx = data.substring(0, firstSemiColon);
  //   vy = data.substring(firstSemiColon + 1, secondSemiColon);
  //   wz = data.substring(secondSemiColon + 1);

  //   Serial.print("Parsed X: ");
  //   Serial.print(strToFloat(vx));
  //   Serial.print(" Y: ");
  //   Serial.print(strToFloat(vy));
  //   Serial.print(" Z: ");
  //   Serial.println(strToFloat(wz));
  // }
  // Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(vx, vy, wz);
  // FL.compute(wheelSpeeds.radps_fl, deltaT);
  // FR.compute(wheelSpeeds.radps_fr, deltaT);
  // BL.compute(wheelSpeeds.radps_bl, deltaT);
  // BR.compute(wheelSpeeds.radps_br, deltaT);

  //For test purpose
  TransformStep steps[] = {
    { 0, 0.15, 0, 10000 },
    { 0, -0.15, 0, 10000 }
  };

  T = millis();
  if (currentStep < sizeof(steps) / sizeof(steps[0])) {
    if (T - start_time < steps[currentStep].duration) {
      Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(steps[currentStep].vx, steps[currentStep].vy, steps[currentStep].wz);
      FL.compute(wheelSpeeds.radps_fl, deltaT);
      FR.compute(wheelSpeeds.radps_fr, deltaT);
      BL.compute(wheelSpeeds.radps_bl, deltaT);
      BR.compute(wheelSpeeds.radps_br, deltaT);
    } else {
      Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(0, 0, 0);
      FL.compute(wheelSpeeds.radps_fl, deltaT);
      FR.compute(wheelSpeeds.radps_fr, deltaT);
      BL.compute(wheelSpeeds.radps_bl, deltaT);
      BR.compute(wheelSpeeds.radps_br, deltaT);
      start_time = millis();
      currentStep++;
    }
  } else {
    Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(0, 0, 0);
    FL.compute(wheelSpeeds.radps_fl, deltaT);
    FR.compute(wheelSpeeds.radps_fr, deltaT);
    BL.compute(wheelSpeeds.radps_bl, deltaT);
    BR.compute(wheelSpeeds.radps_br, deltaT);
    currentStep = 10000;
  }
  //For test purpose

  return true;
}