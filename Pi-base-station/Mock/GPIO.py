BOARD = 1
OUT = 1
IN = 1
LOW = "LOW"
HIGH = "HIGH"

def setmode(a):
    print(a)
def setup(pinNumber, pinMode, initial=None):
    print("Setting pin with: " + str(pinNumber) + ' ' + str(pinMode) + ' ' + str(initial))
def output(a, b):
    print(a)
def cleanup():
    print('a')
def setwarnings(flag):
    print('False')
def input(pin):
    return 1
def RPI_REVISION():
    return "Fake RPI"
def VERSION():
    return "Fake GPIO library"
