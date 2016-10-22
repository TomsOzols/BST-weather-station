# pylint: disable=C0103
# pylint: disable=C0111

import time

import RadioModuleHelpers as radioHelper
workingOnRaspberry = False
if workingOnRaspberry:
    import RPi.GPIO as GPIO
    import serial as serial
else:
    import Mock.GPIO as GPIO
    import Mock.serial as serial


debug = True
# Allow to send
send = 0
# Allow to receive
receive = 0

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
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)    #AMB8420 default baud rate.

print("Setting radio pins")
radioHelper.SetRadioPins()
print("Resetting radio")
radioHelper.ResetRadio()

print("Polling radio")
while True:
    try:
        if radioHelper.RTS() and GPIO.input(13) == 1 and receive == 0 and send == 0:
            if debug:
                print("Nothing happens")
            port.write("\r\nSay something:")
            send = 1
            time.sleep(1.0/100.0)
        elif radioHelper.RTS() and GPIO.input(13) == 0 and receive == 1:
            if debug:
                print("something received")
            rcv = readlineCR(port)
            print(repr(rcv))
            receive = 0
            send = 0
            time.sleep(1.0/100.0)
        elif not radioHelper.RTS() and GPIO.input(13) == 1:
            if debug:
                print("UART buffer full")
            send = 1
            time.sleep(1.0/100.0)
        else:
            if debug:
                print("something received, but UART buffer full")
            receive = 1
            send = 1
            time.sleep(1.0/100.0)
    except KeyboardInterrupt: #Ctrl-c
        break

print("Closing serial port and ending")
port.close()
