#!/usr/bin/env python
import serial
import time

class injector:

    """Class to handle the communication between the host and the microcontroller """
    def __init__(self,Port):

        #command codes stored here
        self.COMMAND_SEND_DELAY = b"\xAA"
        self.COMMAND_SEND_TRIGGER = b"\xBB"
        self.COMMAND_SEND_RESET = b"\xCC"

        #print("opening serial port")
        try:
            self.s = serial.Serial(port=Port,baudrate=115200)

        except:
            if(not(self.s.isOpen())):
                print("error opening port")
            raise
        self.s.flush()

    def writeByte(self,byte):
        self.s.write(byte)

    def delay(self,cycles):
        cycles = cycles & 0xFFFF
        self.s.write(self.COMMAND_SEND_DELAY + b"\x02" + chr(cycles >> 8) +chr(cycles & 0xFF))
        response = self.s.read(4)
        return response

    def trigger(self):
        self.s.write(self.COMMAND_SEND_TRIGGER + b"\x01" + b"\xFF")
        response = self.s.read(3)
        return response

    def reset(self):
        self.s.write(self.COMMAND_SEND_RESET + b"\x01" + b"\xFF")
        response = self.s.read(3)
        return response

def toHexList(input):
        a = map(ord, input)
        return map(hex, a)

def toHexString(input):
        return ''.join('{:02x}'.format(x) for x in input)
        
        
def toByteArray(input):
        return map(ord, input)

def main():
	i = injector('/dev/ttyACM0')
	i.reset()

if __name__ == "__main__":
	main()
