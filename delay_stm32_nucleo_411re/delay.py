#!/usr/bin/env python
import serial
import sys

cycles = int(sys.argv[1]) & 0xFFFF
s = serial.Serial("/dev/ttyACM0",baudrate=115200)
s.flushInput()
blub  =  b"\xAA" + b"\x02" + chr(cycles >> 8) +chr(cycles & 0xFF)
s.write(blub)
result = s.read(len(blub))
for i in result: print(i.encode('hex')),
print
#print ord(response)
