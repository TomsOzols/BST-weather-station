# pylint: disable=C0103
# pylint: disable=C0111

import time

import RadioModuleHelpers as radioHelper
import MeasurementService as measurementService
workingOnRaspberry = True
if workingOnRaspberry:
    import serial as serial
else:
    import Mock.serial as serial

debug = True

print("*****************************************")
print("**           BASE STATION              **")
print("*****************************************")
print("RasPi revision: " + radioHelper.RaspberryRevision())
print("RPi.GPIO version: " + radioHelper.GPIOLibraryVersion())
print("*****************************************")
print("Configuring software...")
radioHelper.ConfigureGPIOMode()

def readlineCR(serialPort):
    rv = ""
    while True:
        ch = serialPort.read()
        rv += ch
        if ch == '\r' or ch == '':
            return rv

print("Opening serial port")
#AMB8420 default baud rate = 9600..
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

print("Setting up the measurement services")
measurementService.Setup()
print("Setting radio pins")
radioHelper.SetRadioPins()
radioHelper.SetShutdownPin()


print("Resetting radio")
radioHelper.ResetRadio()

print("Polling radio")

actionSleepTime = 1.0/100.0

while True:
    radioHelper.InitiateShutdown()
    time.sleep(3)
    radioHelper.DELETEME()

while True:
    try:
        # Left in for extra debug purposes. Should remove as soon as possible.
        readyToSend = radioHelper.RTS()
        dataIndicate = radioHelper.DATA_INDICATE()
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

print("Closing serial port and ending")
port.close()

