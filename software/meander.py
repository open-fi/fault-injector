import numpy as np

def horMeander(xOrigin,yOrigin,xLen,yLen,resolution):
	
	pointsX = np.empty([1,0])
	pointsY = np.empty([1,0])
	
	stepsX = int(xLen / resolution)+1
	stepsY = int(yLen / resolution)+1
	
	#print stepsX
	#print stepsY
	
	
	xRow = [xOrigin+i*resolution for i in range(0,stepsX)]
	
	for i in range(0,stepsY):
		if not (i%2):
			pointsX = np.append(pointsX,xRow)
			tmp = np.ones([1,stepsX])*resolution*i+yOrigin
			#print np.shape(tmp)
			pointsY = np.append(pointsY,tmp)
			#print 'A'
		else:
			pointsX = np.append(pointsX,xRow[::-1])
			tmp = np.ones([1,stepsX])*resolution*i+yOrigin
			#print np.shape(tmp)
			pointsY = np.append(pointsY,tmp)
			#print 'B'

	#print pointsX
	#print pointsY
	
	
	points = np.vstack((pointsX,pointsY)) 
	return points
	
def verMeander(xOrigin,yOrigin,xLen,yLen,resolution):
	pointsX = np.empty([1,0])
	pointsY = np.empty([1,0])
	
	stepsX = int(xLen / resolution) +1
	stepsY = int(yLen / resolution) +1
	
	#print stepsX
	#print stepsY
	
	
	yRow = [yOrigin+i*resolution for i in range(0,stepsY)]
	
	for i in range(0,stepsX):
		if not (i%2):
			pointsY = np.append(pointsY,yRow)
			tmp = np.ones([1,stepsY])*resolution*i+xOrigin
			#print np.shape(tmp)
			pointsX = np.append(pointsX,tmp)
			#print 'A'
		else:
			pointsY = np.append(pointsY,yRow[::-1])
			tmp = np.ones([1,stepsY])*resolution*i+xOrigin
			#print np.shape(tmp)
			pointsX = np.append(pointsX,tmp)
			#print 'B'

	#print pointsX
	#print pointsY
	
	
	points = np.vstack((pointsX,pointsY)) 
	return points
	
def main():
	from path import Path
	p = Path()
	points = horMeander(1.0,1.0,1.0,1.0,0.1)
	print points
	print np.shape(points)[1]
	
	p.addPath(points[0,:],points[1,:])
	raw_input()

if __name__=='__main__':
	main()
