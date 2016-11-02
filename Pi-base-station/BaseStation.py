# pylint: disable=C0103
# pylint: disable=C0111

import time

import RadioModuleHelpers as radioHelper
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

print("Setting radio pins")
radioHelper.SetRadioPins()
print("Resetting radio")
radioHelper.ResetRadio()

print("Polling radio")
while True:
    try:
        if radioHelper.RTS() and not radioHelper.DATA_INDICATE():
            if debug:
                print("Nothing happens")
            port.write("\r\nSay something:")
            time.sleep(1.0/100.0)
        elif radioHelper.RTS() and radioHelper.DATA_INDICATE():
            if debug:
                print("something received")
            rcv = readlineCR(port)
            print(repr(rcv))
            time.sleep(1.0/100.0)
        elif not radioHelper.RTS() and not radioHelper.DATA_INDICATE():
            if debug:
                print("UART buffer full")
            time.sleep(1.0/100.0)
        # This is pretty much the last possible one - not RTS and DATA_INDICATE
        else:
            if debug:
                print("something received, but UART buffer full")
            time.sleep(1.0/100.0)
    except KeyboardInterrupt: #Ctrl-c
        break

print("Closing serial port and ending")
port.close()
