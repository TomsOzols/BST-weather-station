# Base station software for WSN-SOA network
# (c)2014 by Reinholds Zviedris
#

import RPi.GPIO as GPIO
import time
import serial

Debug = True
# Allow to send
Send = 0
# Allow to receive
Receive = 0

print "*****************************************"
print "**           BASE STATION              **"
print "*****************************************"

s = "RasPi revision: " + str(GPIO.RPI_REVISION)
print s
s = "RPi.GPIO version" + str(GPIO.VERSION)
print s
print "*****************************************"
print "Configuring software..."
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# blinking function
def blink(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    return

def fastblink(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1.0/10.0)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1.0/10.0)
    return

def readlineCR(port):
    rv = ""
    while true:
        ch = port.read()
        rv += ch
        if ch == '\r' or ch=='':
            return rv

print "Opening serial port"
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

print "Setting radio pins"
# SLEEP pin
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
# TRX-DIS pin
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)
# CONFIG pin
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
# DATA_REQUEST pin
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
# RTS pin
GPIO.setup(11, GPIO.IN)
# DATA_INDICATE pin
GPIO.setup(13, GPIO.IN)
# LED/WD pin
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
# RESET pin
GPIO.setup(12, GPIO.OUT, initial=GPIO.HIGH)

print "Resetting radio"
GPIO.output(12, GPIO.LOW)
for i in range(0,3):
    fastblink(16)
GPIO.output(12, GPIO.HIGH)
#raw_inpt("Press Enter to continue")
print "*****************************************"

print "Configuring radio"

print "Polling radio"

while True:
    try:
        if GPIO.input(11) == 0 and GPIO.input(13) == 1 and Receive == 0 and Send == 0:
            if Debug == True:
                print "Nothing happens"
            port.write("\r\nSay something:")
            Send = 1
            time.sleep(1.0/100.0)
        elif GPIO.input(11) == 0 and GPIO.input(13) == 0 and Receive == 1:
            if Debug == True:
                print "something received"
            rcv = readlineCR(port)
            print repr(rcv)
            Receive = 0
            Send = 0
            time.sleep(1.0/100.0)
        elif GPIO.input(11) == 1 and GPIO.input(13) == 1:
            if Debug == True:
                print "UART buffer full"
            Send = 1
            time.sleep(1.0/100.0)
        else:
            if Debug == True:
                print "something received, but UART buffer full"
            Receive = 1
            Send = 1
            time.sleep(1.0/100.0)
    except KeyboardInterrupt: #Ctrl-c
        break

print "Closing serial port and ending"
port.close()