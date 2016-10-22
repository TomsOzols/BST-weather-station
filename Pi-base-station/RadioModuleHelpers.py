# pylint: disable=C0103
# pylint: disable=C0111
import time

workingOnRaspberry = False
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
# else: UART buffer full or wireless reception of a telegram detected. Data coming via UART ignored.
def RTS():
    return GPIO.input(11) == 0

def DATA_INDICATE():
    if GPIO.input(13) == 0:
        return  # TODO: FINISH THIS SHIT!!

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

def SetRadioPins():
    # SLEEP pin
    GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
    # TRX-DISABLE pin
    GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)
    # CONFIG pin
    # Only for entering command mode. Must go high-low to activate command mode. Do not touch.
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
