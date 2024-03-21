
  // FL.compute(60, deltaT);
  // Serial.print(" ");
  // FR.compute(60, deltaT);
  // Serial.print(" ");
  // BL.compute(60, deltaT);
  // Serial.print(" ");
  // BR.compute(60, deltaT);
  // Serial.println();

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

  // //For test purpose
  // TransformStep steps[] = {
  //   // { 7, 0, 0, 1000 },
  //   { 5, 0, 0, 2500 },
  //   {0,0,0,1000},
  //   { 0, 0, 4, 2500 }
  // };

  // T = millis();
  // if (currentStep < sizeof(steps) / sizeof(steps[0])) {
  //   if (T - start_time < steps[currentStep].duration) {
  //     Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(steps[currentStep].vx, steps[currentStep].vy, steps[currentStep].wz);
  //     FL.compute(wheelSpeeds.radps_fl, deltaT);
  //     FR.compute(wheelSpeeds.radps_fr, deltaT);
  //     BL.compute(wheelSpeeds.radps_bl, deltaT);
  //     BR.compute(wheelSpeeds.radps_br, deltaT);
  //     Serial.println();
  //   } else {
  //     Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(0, 0, 0);
  //     FL.compute(wheelSpeeds.radps_fl, deltaT);
  //     FR.compute(wheelSpeeds.radps_fr, deltaT);
  //     BL.compute(wheelSpeeds.radps_bl, deltaT);
  //     BR.compute(wheelSpeeds.radps_br, deltaT);
  //     Serial.println();
  //     start_time = millis();
  //     currentStep++;
  //   }
  // } else {
  //   Kinematics::RadPS wheelSpeeds = kinematics.Inverse_Kinematics(0, 0, 0);
  //   FL.compute(wheelSpeeds.radps_fl, deltaT);
  //   FR.compute(wheelSpeeds.radps_fr, deltaT);
  //   BL.compute(wheelSpeeds.radps_bl, deltaT);
  //   BR.compute(wheelSpeeds.radps_br, deltaT);
  //   Serial.println();
  //   currentStep = 10000;
  // }
  // //For test purpose