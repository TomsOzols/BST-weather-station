class Serial():
    def __init__(self, linuxyMount, baudrate, timeout):
        print("Faking serial port library, arguments: " + linuxyMount, baudrate, timeout)
    def read(self):
        return "Some stuff was read"
    def write(self, someStuff):
        print("Wrote: " + someStuff + "| to serial port")
    def close(self):
        print("Serial port has been closed")
