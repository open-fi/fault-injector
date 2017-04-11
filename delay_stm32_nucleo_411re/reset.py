#!/usr/bin/env python
import serial
import sys

s = serial.Serial("/dev/ttyACM0",baudrate=115200)
s.flushInput()
blub  =  b"\xCC" + b"\x01" + b"\xFF"
s.write(blub)
result = s.read(len(blub))
for i in result: print(i.encode('hex')),
print
#print ord(response)
