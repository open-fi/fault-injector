import serial
import os
import time
import termios
import re
from path import Path

class Koordinatentisch:
	
	def __init__(self,port,plot=0):
		self.plot = plot
		self.port = port
		self.baudRate = 115200
		
		#avoid dtr reset via termios
		with open(port) as f:
			attrs = termios.tcgetattr(f)
			attrs[2] = attrs[2] & ~termios.HUPCL
			termios.tcsetattr(f, termios.TCSAFLUSH, attrs)
		
		self.s = serial.Serial(port,self.baudRate)
		self.s.flushInput()
		self.s.flushOutput()
		
		if plot:
			self.p = Path()

	def getPos(self):
		time.sleep(0.1)
		self.s.flushInput()
		self.s.flushOutput()
		self.s.write('?\r\n')
		state = self.s.readline().strip()
		#print state
		match = re.search('MPos:([-+]?\d*\.\d+),([-+]?\d*\.\d+),([-+]?\d*\.\d+),', state)
		x_coordinate = float(match.group(1))
		y_coordinate = float(match.group(2))
		
		return [x_coordinate,y_coordinate]

	def sendPreamble(self):
		self.s.flushInput()
		self.s.flushOutput()
		self.s.write('G17 G21 G90 G94 G54' + '\r\n')
		response = self.s.readline()
		return response.strip()
		

	def moveAbsPos(self,x,y):
		self.s.flushInput()
		self.s.flushOutput()
		command = 'G0 X' + str(x) + 'Y' + str(y)
		#print command
		self.s.write(command + '\r\n')
		response = self.s.readline()
		#print response
		while 1:
			time.sleep(0.1)
			self.s.flushInput()
			self.s.flushOutput()
			self.s.write('?\r\n')
			state = self.s.readline().strip()
			try:
				match = re.search('.+,MPos:([-+]?\d*\.\d+),([-+]?\d*\.\d+),([-+]?\d*\.\d+),', state)
				x_coordinate = float(match.group(1))
				y_coordinate = float(match.group(2))
			except AttributeError:
				continue
			
			if self.plot:
				self.p.addPoint(x_coordinate,y_coordinate)
			#os.sys.stdout.write('\r' + "X:" + str(x_coordinate) + "\tY:" + str(y_coordinate))
			#os.sys.stdout.flush()
			if(re.search('^<Idle.*', state)):
				#print
				#time.sleep(0.1)
				break
		#time.sleep(0.2)

	def moveRelPos(self,x,y):
		self.s.flushInput()
		self.s.flushOutput()
		command = 'G91 G0 X' + str(x) + 'Y' + str(y)
		#print command
		self.s.write(command + '\r\n')
		response = self.s.readline()
		#print response
		while 1:
			time.sleep(0.1)
			self.s.flushInput()
			self.s.flushOutput()
			self.s.write('?\r\n')
			state = self.s.readline().strip()
			try:
				match = re.search('.+,MPos:([-+]?\d*\.\d+),([-+]?\d*\.\d+),([-+]?\d*\.\d+),', state)
				x_coordinate = float(match.group(1))
				y_coordinate = float(match.group(2))
			except AttributeError:
				continue
			if self.plot:
				self.p.addPoint(x_coordinate,y_coordinate)
			#os.sys.stdout.write('\r' + "X:" + str(x_coordinate) + "\tY:" + str(y_coordinate))
			#os.sys.stdout.flush()
			if(re.search('^<Idle.*', state)):
				#print
				time.sleep(0.1)
				self.s.flushInput()
				self.s.flushOutput()
				self.s.write('G90' + '\r\n')
				#print self.s.readline()
				#time.sleep(0.1)
				break
		#time.sleep(0.1)

	def calibratePos(self):
		print "!!!WARNING!!! z axis needs to be lifted type YES"
		response = raw_input()
		if(response!="YES"):
			return
		self.s.flushInput()
		self.s.flushOutput()
		command = '$H'
		#print command
		self.s.write(command + '\r\n')
		response = self.s.readline()
		print "Calibration finished"
		
	def moveIdlePos(self):
		self.moveAbsPos(-5.0,-5.0)
		
	def moveCenterPos(self):
		self.moveAbsPos(-75.0,-35.0)
		
	def cleanUp(self):
		if self.plot:
			self.p.closePath()

def main():
	print 'koordinatentisch'
	t = Koordinatentisch('/dev/ttyACM0',1)
	t.sendPreamble()
	#~ #print t.getPos()
	#~ #t.moveAbsPos(-20.0,-5.0)
	#~ #print t.getPos()
	#~ t.moveAbsPos(1.0,0.0)
	print t.getPos()
	#~ t.moveRelPos(0.0,1.0)
	#~ print t.getPos()
	#~ t.moveAbsPos(0.0,1.0)
	#~ print t.getPos()
	#~ #t.moveIdlePos()
	#~ #print t.getPos()
	t.p.closePath()
if __name__=='__main__':
	main()
