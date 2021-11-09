#include <Wire.h>
#include <VL53L1X.h>

VL53L1X sensor;
const int L = 35;
long samples[L]; 
long sum = 0;
long avg = 0;
const int threshold = 900;
int track = 0;


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
  //long time = millis();
  //Serial.println("Here");
  for (int i = 0; i<L; ++i){
    if (samples[i] != 0) {
        sum-=samples[i]; //First, subtract oldest value that you're replacing from sum 
    }
    //Serial.println(millis()-time);
    samples[i] = sensor.read(); //Then replace that value; sensor.read doesn't return until there is a value
    //time = millis();
    sum = sum+samples[i];
    if (track < L){ //Divide by i+1 until array is filled
      avg = sum/(track+1);
      track+=1;
    }
    else{
      avg = sum/L;
    }
    
    if (avg < threshold) {
        Serial.println(String(1)+","+String(avg)+","+String(samples[i])); //Send to Pi
    }
    else if (avg > threshold){
        Serial.println(String(0)+","+String(avg)+","+String(samples[i])); //Send to Pi
    }
    
 }

}
