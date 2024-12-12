#include <Wire.h>
#include <BH1750.h>


// Create an instance of the BH1750 sensor
BH1750 lightMeter;

void setup() {
  Serial.begin(9600);

  // Initialize I2C communication on default pins (SDA on GPIO 19, SCL on GPIO 20)
  Wire1.setSDA(14);
  Wire1.setSCL(15);

  Wire1.begin();  // Raspberry Pi Pico defaults to GPIO 19 and GPIO 20 for I2C

  // Initialize the BH1750 sensor
  if (!lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, 0x23, &Wire1)) {
    Serial.println(F("Error initializing BH1750. Check wiring!"));
    while (true);  // Halt execution if initialization fails
  }

  Serial.println(F("BH1750 Test begin"));
}

void loop() {

  // Read the light level in lux
if (Serial.available() > 0) {

  float lux = lightMeter.readLightLevel();
  String command = Serial.readStringUntil('\n');  // Read the command sent from RP Zero
  command.trim();  // Remove any trailing whitespace or newline characters
  command.toLowerCase();
  if (command == "run"){
    if (lux > 0.8){
      Serial.print(F("Light Level Exceeds Threhold. Box Has Been Opened!"));
      Serial.println();
    }else if (lux != -1){
      Serial.print(F("Light Level: "));
      Serial.print(lux);
      Serial.println(F(" lx"));
    }else{
      Serial.println(F("Error reading light level!"));
    }

    delay(10000);  // Wait for 800 ms before the next reading
  
    }
  }
}