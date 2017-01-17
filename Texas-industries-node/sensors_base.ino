#include <SHT1x.h>                // Library for the STH15 temperature and humidity sensor
#include <SoftwareSerial.h>   // Library for radio

/* Variables for storing values */

// TEMPERATURE AND HUMIDITY
float tempC = 0;      // Temperature value in degree Celsius
float tempF = 0;      // Temperature value in degree Fahrenheit
float humidity = 0;

// Communication over radio
SoftwareSerial RT(5,2);
String RadioData;

// WIND DIRECTION, SPEED and RAIN
int rawWDIR    = 0;           // Raw data of the wind direction
int WDIR       = 0;           // Readable wind direction
int WSPEED     = 0;           // Readable wind speed
int RAIN       = 0;           // Readable rain data

// Create an instance of the SHT1X sensor
SHT1x sht15(11, 12);          // Data pin 11, Clock pin 12

/*// LEDs
#define LED RED_LED
*/

/*#define NORTH     1
#define NORTHEAST 2
#define EAST      3
#define SOUTHEAST 4
#define SOUTH     5
#define SOUTHWEST 6
#define WEST      7
#define NORTHWEST 8*/


void setup()
{
  Serial.begin(9600);          //  setup serial

  // Setup serial for radio
  RT.begin(9600);

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
  delay(200);         // Wait for 2 miliseconds

  /* WIND DIRECTION */
  //readWDIR();

  /* WIND SPEED AND RAIN */
  WSPEED = analogRead(15);
  RAIN   = analogRead(13);

  /* LEDs for system monitoring */
  /*if(WSPEED && RAIN)
  {
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
  }*/

  /* Print the data received from sensors */
  printOut();         
  
  /* Radio communication */
  if(Serial.available())              // Send data only when you receive data:
  {
    RadioData = RT.readString();      // Read the incoming bytes and store it in string object
    
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
  Serial.print(humidity); 
  Serial.println("%' }");

  /*// WIND DIRECTION 
  Serial.print("{ 'Wind direction' = '");
  Serial.print(WDIR);
  Serial.println("' }");
  */
  
  // WIND SPEED AND RAIN
  Serial.print("{ 'Wind Speed': '");
  Serial.print(WSPEED);
  Serial.print("', 'Ŗain': '");
  Serial.print(RAIN);
  Serial.println("' }");
}

void readSensor()
{
  // Read values from the sensors
  tempC = sht15.readTemperatureC();
  tempF = sht15.readTemperatureF();
  humidity = sht15.readHumidity();  
}

/*
void readWDIR()
{
    rawWDIR = analogRead(14); 

    if(rawWDIR > 960 && rawWDIR <= 1023 && rawWDIR >= 0 && rawWDIR <= 64)
    {
      WDIR = NORTH;
    }
    else if(rawWDIR > 64 && rawWDIR <= 192)
    {
      WDIR = NORTHEAST;
    }
    else if(rawWDIR > 192 && rawWDIR <= 320)
    {
      WDIR = EAST;
    }
    else if(rawWDIR > 320 && rawWDIR <= 448)
    {
      WDIR = SOUTHEAST;
    }
    else if(rawWDIR > 448 && rawWDIR <= 576)
    {
      WDIR = SOUTH;
    }
    else if(rawWDIR > 576 && rawWDIR <= 704)
    {
      WDIR = SOUTHWEST;
    }
    else if(rawWDIR > 704 && rawWDIR <= 832)
    {
      WDIR = WEST;
    }
    else 
    {
      WDIR = NORTHWEST;
    }
}
*/

