#include <SHT1x.h>            // Library for the STH15 temperature and humidity sensor
#include <SoftwareSerial.h>   // Library for radio communication

/* Variables for storing values */

// WIND DIRECTION, WIND SPEED AND RAIN
float Direction;
float currentWindDirection;
float currentWindSpeed;
float totalRain;
float startSampleTime;
long currentWindCount = 0;
long currentRainCount = 0;
float sampleTime = 5.0;

// TEMPERATURE AND HUMIDITY
float tempC = 0;      // Temperature value in degree Celsius
float tempF = 0;      // Temperature value in degree Fahrenheit
float HUMIDITY = 0;

// Communication over radio
SoftwareSerial RT(5,2);
String RadioData;

/* Instances */

// Create an instance of the SHT1X sensor
SHT1x sht15(11, 12);          // Data pin 11, Clock pin 12


/*  Monitoring with LEDs 
#define LED RED_LED
*/

/* Define pin */
#define pinWindDir 14
#define pinAnem    15
#define pinRain    13

#define WIND_FACTOR 2.400 

boolean fuzzyCompare(float compareValue, float value)
{
  #define VARYVALUE 0.05
  
   if ( (value > (compareValue * (1.0-VARYVALUE)))  && (value < (compareValue *(1.0+VARYVALUE))) )
   {
     return true; 
   }
   return false;
}

float voltageToDegrees(float value, float defaultWindDirection)
{
  
  // Note:  The original documentation for the wind vane says 16 positions.  Typically only recieve 8 positions.  And 315 degrees was wrong.
  
  // For 5V, use 1.0.  For 3.3V use 0.66
float ADJUST3OR5    =  0.66;
float PowerVoltage  = 3.3;

  if (fuzzyCompare(3.84 * ADJUST3OR5 , value))
      return 0.0;

  if (fuzzyCompare(1.98 * ADJUST3OR5, value))
      return 22.5;

  if (fuzzyCompare(2.25 * ADJUST3OR5, value))
      return 45;

  if (fuzzyCompare(0.41 * ADJUST3OR5, value))
      return 67.5;

  if (fuzzyCompare(0.45 * ADJUST3OR5, value))
      return 90.0;

  if (fuzzyCompare(0.32 * ADJUST3OR5, value))
      return 112.5;

  if (fuzzyCompare(0.90 * ADJUST3OR5, value))
      return 135.0;

  if (fuzzyCompare(0.62 * ADJUST3OR5, value))
      return 157.5;

  if (fuzzyCompare(1.40 * ADJUST3OR5, value))
      return 180;

  if (fuzzyCompare(1.19 * ADJUST3OR5, value))
      return 202.5;

  if (fuzzyCompare(3.08 * ADJUST3OR5, value))
      return 225;

  if (fuzzyCompare(2.93 * ADJUST3OR5, value))
      return 247.5;

  if (fuzzyCompare(4.62 * ADJUST3OR5, value))
      return 270.0;

  if (fuzzyCompare(4.04 * ADJUST3OR5, value))
      return 292.5;

  if (fuzzyCompare(4.34 * ADJUST3OR5, value))  // chart in documentation wrong
      return 315.0;

  if (fuzzyCompare(3.43 * ADJUST3OR5, value))
      return 337.5;
      
  //Serial.print(" FAIL WIND DIRECTION");
  return defaultWindDirection;  // return previous value if not found
  
  
}

unsigned long lastWindTime;

void serviceInterruptAnem()
{
  unsigned long currentTime= (unsigned long)(micros()-lastWindTime);

  lastWindTime=micros();
  if(currentTime>1000)   // debounce
  {
     currentWindCount++;
  } 
}

unsigned long currentRainMin;
unsigned long lastRainTime;

void serviceInterruptRain()
{
  unsigned long currentTime=(unsigned long) (micros()-lastRainTime);

  lastRainTime=micros();
  if(currentTime>500)   // debounce
  {
       currentRainCount++;
//      interrupt_count[19]++;
    if(currentTime<currentRainMin)
    {
     currentRainMin=currentTime;
    }
 }
}

void setup()
{
  Serial.begin(9600);          //  setup serial

  /* Setup serial for radio */
  RT.begin(9600);
  
  pinMode(pinAnem, INPUT_PULLUP);     // pinAnem is input to which a switch is connected and configure internal pull-up resistor
  pinMode(pinRain, INPUT_PULLUP);     // pinRain is input to which a switch is connected  and configure internal pull-up resistor

  /* Initialize the LED pins for output
  pinMode(LED, OUTPUT);
  */
}

void loop()
{ 
  flash();
  sleepSeconds(2);
}

void flash()
{
  /* TEMPERATURE AND HUMIDITY using STH15 sensor */  
  readSensor();       // Receive the values from the sensor

  /* WEATHER METER */
  currentWindDirection = 0.0;
  totalRain = 0.0;
  currentWindSpeed = 0.0;
  startSampleTime = micros();
  
  attachInterrupt(5, serviceInterruptAnem, RISING);
  attachInterrupt(1, serviceInterruptRain, RISING);

  // WIND DIRECTION
  Direction = voltageToDegrees((analogRead(pinWindDir)*0.003f), currentWindDirection); 

  // RAIN
  float rain_amount = 0.2794 * currentRainCount/2;  // mm of rain - we get two interrupts per bucket
  currentRainCount = 0;
  totalRain = totalRain + rain_amount/25.4;

  // WIND SPEED
  unsigned long compareValue;
  compareValue = sampleTime*1000000;
  
  if (micros() - startSampleTime >= compareValue)
  {
      // sample time exceeded, calculate currentWindSpeed
      float timeSpan;
      // timeSpan = (unsigned long)(micros() - startSampleTime);
      timeSpan = (micros() - startSampleTime);
 
      currentWindSpeed = ((float)currentWindCount/(timeSpan)) * WIND_FACTOR*1000000;

      currentWindCount = 0;
      
      startSampleTime = micros();
  }

  /* Print the data received from sensors */
  printOut();         
  
  /* Radio communication */
  if(Serial.available())              // Send data only when you receive data:
  {
    RadioData = RT.readString();          // Read the incoming bytes and store it in string object
    
    // Print the received data
    Serial.print("{ 'Radio data': '");

    Serial.print(RadioData);
    Serial.println("' }");
  }
}

void printOut()
{
  //TEMP AND HUMIDITY
  Serial.print("{ 'temperatureF': '");
  Serial.print(tempF);
  Serial.print("F', 'temperatureC': '");
  Serial.print(tempC);
  Serial.print("C', 'Humidity': '");
  Serial.print(HUMIDITY); 
  Serial.println("%' }");

  /* WEATHER METER */
  float WindSpeed = currentWindSpeed/1.6;
  
  Serial.print("{ 'Rain total': '");
  Serial.print(totalRain);
  Serial.print("', 'Wind speed': '");
  Serial.print(WindSpeed);
  Serial.print(" MPH', 'Wind direction': '");
  Serial.print(Direction);
  Serial.println(" degrees' }");
}

void readSensor()
{
  // Read values from the sensors
  tempC = sht15.readTemperatureC();
  tempF = sht15.readTemperatureF();
  HUMIDITY = sht15.readHumidity();  
}



