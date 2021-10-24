#include <Wire.h>
#include <VL53L1X.h>

VL53L1X sensor;
const int L = 35;
long samples[L]; 
long sum = 0;
long avg = 0;
const int threshold = 900;


void setup()
{
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(400000); // use 400 kHz I2C

  sensor.setTimeout(500);
  if (!sensor.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
    while (1);
  }

  sensor.setDistanceMode(VL53L1X::Long);
  sensor.setMeasurementTimingBudget(15000);
  sensor.startContinuous(15);
  Serial.println("new program");
}

void loop()
{
  //Serial.println(String(millis())+","+String(sensor.read()));

  Serial.println("Here");
  for (int i = 0; i<L; ++i){
    if (samples[i] != 0) {
        sum-=samples[i]; //First, subtract oldest value that you're replacing from sum 
    }
    samples[i] = sensor.read(); //Then replace that value; sensor.read doesn't return until there is a value
    sum = sum+samples[i];
    avg = sum/(i+1);
    //Serial.println(String(avg));
    //Serial.println("Here");
    
    if (avg < threshold) {
        Serial.println(String(1)+","+String(avg)+","+String(samples[i])); //Send to Pi
    }
    else if (avg > threshold){
        Serial.println(String(0)+","+String(avg)+","+String(samples[i])); //Send to Pi
    }
    
 }

}
