import matplotlib.pyplot as plt
import numpy as np

class Path:

	def __init__(self):
		plt.ion()
		self.fig, self.ax = plt.subplots()
		self.plot = self.ax.scatter([], [])
		self.ax.set_xlim(-4, +4)
		self.ax.set_ylim(-4, +4)
		self.ax.set_xlabel('x-axis')
		self.ax.set_ylabel('y-axis')
		self.array = np.array([])

	def addPoint(self,x,y):
		point = [x, y]
		self.array = self.plot.get_offsets()
		self.array = np.append(self.array, point)
		self.ax.set_xlim(np.amin(self.array[::2])-1, np.amax(self.array[::2])+1)
		self.ax.set_ylim(np.amin(self.array[1::2]-1), np.amax(self.array[1::2])+1)
		#ax.set_xlim(-3, 3)
		#ax.set_ylim(-3, 3)
		self.plot.set_offsets(self.array)
		self.fig.canvas.draw()

	def addPath(self,x,y):
		point = np.insert(y, np.arange(len(x)), x)
		self.array = self.plot.get_offsets()
		self.array = np.append(self.array, point)
		self.ax.set_xlim(np.amin(self.array[::2])-1, np.amax(self.array[::2])+1)
		self.ax.set_ylim(np.amin(self.array[1::2]-1), np.amax(self.array[1::2])+1)
		#ax.set_xlim(-3, 3)
		#ax.set_ylim(-3, 3)
		self.plot.set_offsets(self.array)
		self.fig.canvas.draw()
	
	def clearPath(self):
		self.array = np.array([])
		self.plot.set_offsets(self.array)
		self.fig.canvas.draw()
		
	def closePath(self):
		plt.close()


def main():
	p = Path()
	#raw_input()
	p.addPoint(1.0,1.0)
	#raw_input()	
	#p.clearPath()
	#raw_input()
	#p.addPoint(1.0,1.0)
	raw_input()
	#p.closePath()


if __name__=='__main__':
	main()
