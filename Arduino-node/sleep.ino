#include "Wire.h"
#include <avr/sleep.h>
#define PCF8593address 0x51

byte control, hundredths, second, minute, hour, dayOfWeek, dayOfMonth, month, year;
byte temp5;
byte temp6;
String days[] = {
  "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" };
int ThisYear = 2013;

int wakePin = 3;                 // pin used for waking up
int sleepStatus = 0;             // variable to store a request for sleep
int count = 0;                   // counter
 
void wakeUpNow()        // here the interrupt is handled after wakeup
{
  
}
 
void sleepNow()         // here we put the arduino to sleep
{
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);   // sleep mode is set here
 
    sleep_enable();          // enables the sleep bit in the mcucr register
                             // so sleep is possible. just a safety pin
 
    attachInterrupt(0,wakeUpNow, LOW); // use interrupt 0 (pin 3) and run function
                                       // wakeUpNow when pin 2 gets LOW
 
    sleep_mode();            // here the device is actually put to sleep!!
                             // THE PROGRAM CONTINUES FROM HERE AFTER WAKING UP
 
    sleep_disable();         // first thing after waking from sleep:
                             // disable sleep...
    detachInterrupt(0);      // disables interrupt 0 on pin 2 so the
                             // wakeUpNow code will not be executed
                             // during normal running time.
 
}

byte bcdToDec(byte value)
{
  return ((value / 16) * 10 + value % 16);
}

byte decToBcd(byte value){
  return (value / 10 * 16 + value % 10);
}

void setPCF8593()
// this sets the time and date to the PCF8593
{
  Wire.beginTransmission(PCF8593address);
  Wire.write(0x00);
  Wire.write(decToBcd(control));    // location 00h
  Wire.write(decToBcd(hundredths)); // location 01h
  Wire.write(decToBcd(second));     // location 02h 
  Wire.write(decToBcd(minute));     // location 03h
  Wire.write(decToBcd(hour));       // location 04h also am/pm & 24 or 12 hr
  Wire.write(temp5);
  Wire.write(temp6);
  Wire.endTransmission();
}

void readPCF8593()
// this gets the time and date from the PCF8593
{
  Wire.beginTransmission(PCF8593address);
  Wire.write(0x02);
  Wire.endTransmission();
  Wire.requestFrom(PCF8593address, 5);
  second     = bcdToDec(Wire.read());             // location 02h
  minute     = bcdToDec(Wire.read() & B01111111); // remove unwanted bits from MSB
  hour       = bcdToDec(Wire.read() & B00111111); // location 04h
  temp5      = Wire.read();                       // location 05h 
  temp6      = Wire.read();                       // location 06h 
  dayOfMonth = bcdToDec((temp5) & B00111111);  
  month      = bcdToDec((temp6) & B00011111);      
  year       = (temp5 >> 6);
  dayOfWeek  = (temp6 >> 5);
}

void setup()
{
  Wire.begin();
  Serial.begin(9600);
  ThisYear = ((ThisYear / 4) * 4);  //  change to last leap year
  ////////////////////////////////////////////////////
  // change the following to set your initial time
  ///////////////////////////////////////////////////
  control = 0;
  hundredths = 0;
  second = 45;
  minute = 59;
  hour = 23;
  dayOfWeek = 1;    // 0 to 6
  dayOfMonth = 31;
  month = 3;    
  year = 2;        // 0 to 3
  temp5 = ((year << 6) | decToBcd(dayOfMonth));
  temp6  = ((dayOfWeek << 5) | decToBcd(month));
  // comment out the next line and upload again 
  // to set and keep the time from resetting every reset

  pinMode(4, OUTPUT);
  pinMode(5, INPUT);
  digitalWrite(4, HIGH);
  setPCF8593();  
  pinMode(wakePin, INPUT);
 
  attachInterrupt(0, wakeUpNow, LOW); // use interrupt 0 (pin 2) and run function
                                      // wakeUpNow when pin 2 gets LOW
}

void loop()
{
  readPCF8593();
//  Serial.print(days[dayOfWeek]); 
//  Serial.print(" ");
//  Serial.print(month, DEC);  
//  Serial.print("/");
//  Serial.print(dayOfMonth, DEC);  
//  Serial.print("/");
//  Serial.print((ThisYear + year), DEC);
//  Serial.print(" - ");
//  Serial.print(hour, DEC);
//  Serial.print(":");
//  if (minute < 10)
//  {
//    Serial.print("0");
//  }
//  Serial.print(minute, DEC);
//  Serial.print(":");  
//  if (second < 10)
//  {
//    Serial.print("0");
//  }  
//  Serial.println(second, DEC);

  int val = LOW;
  
  while (!(val == HIGH)){

    val = digitalRead(5);

    if (val == HIGH) {
      delay(20000);
      digitalWrite(4, LOW);
      Serial.println("Sleep time");
      sleepNow();
    }
    delay(1000);
    Serial.println("No sleep");    
  }
  
}
