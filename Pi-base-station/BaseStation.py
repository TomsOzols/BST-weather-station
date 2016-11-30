# pylint: disable=C0103
# pylint: disable=C0111

import time

import GPIOfunctions as gpioFunctions
import MeasurementService as measurementService
workingOnRaspberry = True
if workingOnRaspberry:
    import serial as serial
    import os as os
else:
    import Mock.serial as serial
    import Mock.os as os

debug = True

def KillPi():
    gpioFunctions.InitiateShutdown()
    os.system('shutdown now -h')

def readlineCR(serialPort):
    rv = ""
    while True:
        ch = serialPort.read()
        rv += ch
        if ch == '\r' or ch == '':
            return rv

print("*****************************************")
print("**           BASE STATION              **")
print("*****************************************")
print("RasPi revision: " + gpioFunctions.RaspberryRevision())
print("RPi.GPIO version: " + gpioFunctions.GPIOLibraryVersion())
print("*****************************************")
print("Configuring software...")
gpioFunctions.ConfigureGPIOMode()

print("Opening serial port")
#AMB8420 default baud rate = 9600..
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

print("Setting up the measurement services")
measurementService.Setup()
print("Setting radio pins")
gpioFunctions.SetRadioPins()
gpioFunctions.SetShutdownPin() # Pain in the ass (or as some might say - pin in the ass)

print("Resetting radio")
gpioFunctions.ResetRadio()

print("Polling radio")

actionSleepTime = 1.0/100.0
while True:
    try:
        # Left in for extra debug purposes. Should remove as soon as possible.
        readyToSend = gpioFunctions.RTS()
        dataIndicate = gpioFunctions.DATA_INDICATE()
        print("RTS: " + str(readyToSend))
        print("Data indicate: " + str(dataIndicate))
        # Up till here.

        rcv = readlineCR(port)
        if debug:
            print(repr(rcv))

        measurementService.ProcessMeasurements(rcv)
        time.sleep(actionSleepTime)
    except KeyboardInterrupt: #Ctrl-c
        break

print("Closing serial port")
port.close()
print("Shut down")
KillPi()
