#include <Arduino.h>
#include <micro_ros_platformio.h>

#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <std_msgs/msg/string.h>

#include <Motor.h>
#include <Kinematics.h>
#include <pio_encoder.h>

rcl_subscription_t subscriber;
std_msgs__msg__String joy_msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

#define LED_PIN 13

#define RCCHECK(fn)                                                                                                    \
  {                                                                                                                    \
    rcl_ret_t temp_rc = fn;                                                                                            \
    if ((temp_rc != RCL_RET_OK))                                                                                       \
    {                                                                                                                  \
      error_loop();                                                                                                    \
    }                                                                                                                  \
  }

// control setup

// Motor Setup
int frequency = 1000;
float deltaT = frequency / 1.0e6;
Motor FL(0, 4, 5, 30000, 100, 0);
Motor FR(14, 2, 3, 30000, 100, 0);
Motor BL(18, 6, 7, 30000, 100, 0);
Motor BR(16, 8, 9, 30000, 100, 0);
// Edit Here

// Edit Here
float wheelDiameter = 0.1;
float lx = 0.2;
float ly = 0.2;
Kinematics kinematics(wheelDiameter, lx, ly);
// Edit Here

// For test purpose
// variable
long start_time, T;
int currentStep = 0;
int stepsCount = 0;
bool newStepsAvailable = false;

// Transform
struct TransformStep
{
  float vx;
  float vy;
  float wz;
  unsigned long duration;
};

// end control setup

void error_loop()
{
  while (1)
  {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void timer_callback(rcl_timer_t* timer, int64_t last_call_time)
{
  RCLC_UNUSED(last_call_time);
  if (timer != NULL)
  {
    // control code
    TransformStep steps[] = { { 0, 0.15, 0, 10000 }, { 0, -0.15, 0, 10000 } };

    T = millis();
    if (currentStep < sizeof(steps) / sizeof(steps[0]))
    {
      if (T - start_time < steps[currentStep].duration)
      {
        Kinematics::RadPS wheelSpeeds =
            kinematics.Inverse_Kinematics(steps[currentStep].vx, steps[currentStep].vy, steps[currentStep].wz);
        FL.compute(wheelSpeeds.radps_fl, deltaT);
        FR.compute(wheelSpeeds.radps_fr, deltaT);
        BL.compute(wheelSpeeds.radps_bl, deltaT);
        BR.compute(wheelSpeeds.radps_br, deltaT);
      }
      else
      {
        Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(0, 0, 0);
        FL.compute(wheelSpeeds.radps_fl, deltaT);
        FR.compute(wheelSpeeds.radps_fr, deltaT);
        BL.compute(wheelSpeeds.radps_bl, deltaT);
        BR.compute(wheelSpeeds.radps_br, deltaT);
        start_time = millis();
        currentStep++;
      }
    }
    else
    {
      Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(0, 0, 0);
      FL.compute(wheelSpeeds.radps_fl, deltaT);
      FR.compute(wheelSpeeds.radps_fr, deltaT);
      BL.compute(wheelSpeeds.radps_bl, deltaT);
      BR.compute(wheelSpeeds.radps_br, deltaT);
      currentStep = 10000;
    }
  }
}

void subscription_callback_joy(const void* msgin)
{
  const std_msgs__msg__String* joy_msg = (const std_msgs__msg__String*)msgin;
  digitalWrite(LED_PIN, (joy_msg->data.data == "\0") ? LOW : HIGH);
}

void setup()
{
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);

  delay(2000);

  // control part
  FR.encoder.begin();
  FL.encoder.begin();
  BR.encoder.begin();
  BL.encoder.begin();

  allocator = rcl_get_default_allocator();

  // create init_options
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  // create node
  RCCHECK(rclc_node_init_default(&node, "micro_ros_mobile", "", &support));

  // create subscriber
  RCCHECK(rclc_subscription_init_default(&subscriber, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
                                         "/joy_data"));

  // create timer
  const unsigned int timer_timeout = frequency;
  RCCHECK(rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(timer_timeout), timer_callback));

  // create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &joy_msg, &subscription_callback_joy, ON_NEW_DATA));
}

void loop()
{
  delay(100);
  RCCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));
}