#include "Arduino.h"
#include "Kinematics.h"

Kinematics::Kinematics(float wheel_diameter, float lx, float ly) {
  robot.wheel_diameter = wheel_diameter;
  robot.lx = lx;
  robot.ly = ly;
  robot.wheel_circumference = robot.wheel_diameter * M_PI;
  robot.angular_to_rpm = 60 / robot.wheel_circumference;
}

Kinematics::Velocity Kinematics::Forward_Kinematics_Velocity(float radps_fl, float radps_fr, float radps_bl, float radps_br) {
  Velocity basev;
  basev.vx = ((robot.wheel_diameter / 2.0) / 4.0) * (radps_fl + radps_fr + radps_bl + radps_br) * 0.1047198;
  basev.vy = ((robot.wheel_diameter / 2.0) / 4.0) * (-radps_fl + radps_fr + radps_bl - radps_br) * 0.1047198;
  basev.wz = ((robot.wheel_diameter / 2.0) / (4.0 * (robot.lx + robot.ly))) * (-radps_fl + radps_fr - radps_bl + radps_br) * 0.1047198;
  return basev;
}

Kinematics::RadPS Kinematics::Inverse_Kinematics(float vx, float vy, float wz) {
  RadPS wheel_rads;
  if (vx == 0.0 && vy == 0.0 && wz == 0.0) {
    wheel_rads.radps_fl = 0;
    wheel_rads.radps_fr = 0;
    wheel_rads.radps_bl = 0;
    wheel_rads.radps_br = 0;
  } else {
    wheel_rads.radps_fl = (vx - vy - (robot.lx + robot.ly) * wz) / (robot.wheel_diameter * 0.5) * 9.5492968;
    wheel_rads.radps_fr = (vx + vy + (robot.lx + robot.ly) * wz) / (robot.wheel_diameter * 0.5) * 9.5492968;
    wheel_rads.radps_bl = (vx + vy - (robot.lx + robot.ly) * wz) / (robot.wheel_diameter * 0.5) * 9.5492968;
    wheel_rads.radps_br = (vx - vy + (robot.lx + robot.ly) * wz) / (robot.wheel_diameter * 0.5) * 9.5492968;
  }
  return wheel_rads;
}

Kinematics::Position Kinematics::Forward_Kinematics_Position(float radps_fl, float radps_fr, float radps_bl, float radps_br, Position current_position, float deltaTime) {
  Velocity basev = Forward_Kinematics_Velocity(radps_fl, radps_fr, radps_bl, radps_br);
  current_position.x += basev.vx * deltaTime;
  current_position.y += basev.vy * deltaTime;
  current_position.theta += basev.wz * deltaTime * (180.0 / M_PI);
  current_position.theta = fmod(current_position.theta, 360.0);

  if (current_position.theta < 0) {
    current_position.theta += 360.0;
  }

  return current_position;
}