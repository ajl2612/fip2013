"""
This code is the control code for the system.  It calls methods in the cinematography class object
For the 2014 Freshman Imaging Project at CIS, RIT

Authors: Noah Kram, Anna Dining
"""

import atem_control as bm
from Camera import Camera
#import Cinematography
import time
import config
from motor import Motor

cam_list = []
motor_list = []

for i in range( 0, 3 ):
    cam_list.append( Camera() )
    motor_ip = config.motors[i]['ip']
    motor_port = config.motors[i]['port']
    motor_list.append( Motor( motor_ip, motor_port ) )


cinema = None

def change_camera(cam):
	bm.change_program_input(cam)
	#time.sleep(0)

def test_camera_ranks():
	cameraList = [1,2,3,4]
	currentCamera = cameralist[0]
	cameraList.append(cameraList.pop(0))
	return cameraList

#def test_best_pan_angle():

def main():
	print("Pre thread create")
	#cinema = Cinematography()
	print("Post Thread Create")
	print("pre switch")
	defaultCamera = 1
	defaultPanAngle = 2
	change_camera(defaultCamera)
	change_camera(2)
	print("post switch")

	while True:
		startTime = time.time()
		bestCamera = cinema.camera_ranks()[0]
		#bestCamera = test_camera_ranks()[0]

		if bestCamera == self.currentCamera:
			pass		
			#bestAngle = cinema.best_angle(bestCamera)
			#cinema.pan_camera(bestAngle)

		else:
			print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
			change_camera(bestCamera)
			currentCamera = bestCamera
			#bestAngle = cinema.best_angle(bestCamera)
			#scinema.pan_camera(bestAngle)
			#change_camera(bestCamera)
			#currentCamera = bestCamera
            
		stopTime = time.time()
		timeElapsed = (stopTime-startTime)
		if timeElapsed > 4:
			pass
		else:
			time.sleep(4-timeElapsed)


main()
