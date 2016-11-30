# pylint: disable=C0103
# pylint: disable=C0111
import time

workingOnRaspberry = True
if workingOnRaspberry:
    import RPi.GPIO as GPIO
else:
    import Mock.GPIO as GPIO

def RaspberryRevision():
    return str(GPIO.RPI_REVISION)

def GPIOLibraryVersion():
    return str(GPIO.VERSION)

# Ready to send - true when signal low.
# if true: Data can be received via UART
# else: UART buffer full. Data coming via UART ignored.
def RTS():
    return GPIO.input(11) == 0

# Data indication - true when signal low.
# if true: Something has been received.
# else: Nothing received. TODO: Validate this stuff, not 100% sure if this is true.
def DATA_INDICATE():
    return GPIO.input(13) == 1

# Not really a radio helper but oh well.
def fastblink(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1.0/10.0)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1.0/10.0)
    return

# The reset pin must set to low for at least 10 ms
def ResetRadio():
    GPIO.output(12, GPIO.LOW)
    for i in range(0,3):
        fastblink(16)
    GPIO.output(12, GPIO.HIGH)

def SetShutdownPin():
    # Shutdown signal pin
    GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)

def SetRadioPins():
    # SLEEP pin
    GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
    # TRX-DISABLE pin
    GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)
    # CONFIG pin
    # Only for entering command mode.
    # Must go high-low(falling edge) to activate command mode. Do not touch command mode.
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

def ConfigureGPIOMode():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

def InitiateShutdown():
    GPIO.output(16, GPIO.HIGH)
