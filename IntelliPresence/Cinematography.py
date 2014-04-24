"""
Tracking and capture integration for the 2014 Freshman Imaging Project
at CIS, RIT

Authors: Noah Kram, Anna Dining
"""
#import atem_control as bm
from threadServer import NetwrokThread
from Camera import Camera
import socket

class Cinematography:
    
	defaultAngle = 2
	def __init__(self):
		"""
		Initializes cinematography structure, allows access to tracking data
	
		Note: self.mcsCams is a Tuple of the 4 mcs cameras. They are in order
		(0, 1, 2, 3) and the values in them are updated continuously by code
		from MCS. To access values in them, refer to the Camera class
	
		angles is a dict of the 4 capture cameras and their respective angles. If
		camera fixture 2 is at angle 1, then self.angles[2] returns 1, etc
		"""
		self.currentCamera = 1
		self.previousCamera = 1
		self.angles = {1:2, 2:2, 3:2, 4:2}
		self.motorIPs = {1:('129.21.58.202',8094),2:('129.21.58.202',8094),
			3:('129.21.58.202',8094), 4:('129.21.58.202',8094)}
	        
		cam1 = Camera()
		cam2 = Camera()
		cam3 = Camera()
		cam4 = Camera()
		mcscams = []
	
		mcscams.append(cam1)
		mcscams.append(cam2)
		mcscams.append(cam3)
		mcscams.append(cam4)
		#self.mcsCams = tuple(mcsCams)
		self.mcsCams = mcscams
		thread1 = NetworkThread("", 8091, cam1)
		thread2 = NetworkThread("", 8092, cam2)
		thread1.start() # This actually causes the thread to run
		thread2.start()

    
        
	def camera_ranks(self):
		"""
		Determines capture camera with the largest percentage of face
		as given by Facial Detection
		returns a list (1-4) of the rankings by largest area of each mcs cam
		"""

		tempList = []
		detectedList = []
		for c in self.mcsCams:
			if c.detected:
				tempList.append(c)
			else:
				detectedList.append(c)
		tempList.sort(key=lambda x: x.getWidth(), reverse = True)
		tempList.extend(detectedList)
		#currently does not say where detected begins
		print(tempList)
		z = range(1,5)

		for i in range(4):
			index = self.mcsCams.index(tempList[i])
			z[i] = index + 1
		#z.sort(key = lambda x: self.mcsCams.index(tempList[x]))
		return z
    
    
	def best_angle(self, cam, mcs=False):
		"""
		Finds the best angle for camera 'cam'
        
		Depends on IR Code for input for now. Waiting for them.
		mcs = (bool) if method should run based on mcs input. False by default
		"""
		#IR_code.getAngle or whatever they use
		bestAngle = defaultAngle
		if not mcs:#Fix following part
			if angle >= 0 and angle < 30:
				newPanAngle= 1            
			elif angle >= 30 and angle <60:
				newPanAngle= 2
			elif  angle >=60 and angle <90:
				newPanAngle= 3
			else:
				pass
		else:
			currentAngle = self.angles[cam]
			temp = self.mcsCams[cam]
			if currentAngle == 1 and temp.getX2() <= 133 or currentAngle == 3 and temp.getX1() <= 167:
				bestAngle = 2
			elif currentAngle == 2:
				if temp.getX1() >= 233:
					bestAngle = 1
				elif temp.getX2() <= 67:
					bestAngle = 3
			elif currentAngle == 3:
				#SWAG
				pass
			else:
				#YOLOSWAG
				pass
		return bestAngle

	def pan_camera(self, position, cam):
		## position: best pan angle
		## cPos: current pan position
		cPos = self.angles[cam]
		if position < 1 or position > 3:
			raise ValueError(str(position) + " is not a valid position") 
		elif position != cPos:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(self.motorIPs[cam])
			message = ''
		if cPos == 1:
			if position == 2:
				message = 'True:Left:1'
		elif position == 3:
			message = 'True:Left:2'
		if cPos == 2:
			if position == 1:
				message = 'True:Right:1'
			elif position == 3:
				message = 'True:Left:1'
			else:
				pass
		if cPos == 3:
			if position == 1:
				message = 'True:Right:2'
			elif position == 2:
				message = 'True:Right:1'
			else:
				pass
		print('Sending packet')
		sock.send(message.encode())
		self.angles[cam] = position
	    

#        
#if __name__ == '__main__':
#
#    cine = Cinematography()
#    cine.mcsCams[0] = Camera(0,0,0,0,False)#, 'cam1')
#    cine.mcsCams[1] = Camera(0, 25, 35, 60)#, name='cam2')
#    cine.mcsCams[2] = Camera(0, 60, 600, 150)#, name='cam3')
#    cine.mcsCams[3] = Camera(30, 20, 300, 35)#,False, name='cam4')
#
#    #print cine.camera_ranks()    
#    cine.pan_camera(1,2)
