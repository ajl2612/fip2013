import socket
from Camera import Camera
import threading

class NetworkThread(threading.Thread):
	
	FRAME_MEMORY_LIMIT = 10
	NO_FACE = "0:0:0:0"

	def __init__(self,ip_addr,port_num, cam):
		super(NetworkThread, self).__init__()
		self.ip_addr = ip_addr
		self.port_num = port_num
		self.cam = cam
		# This variable is used to track the number of frames since the last 
		# detected face. The camera will remember a face position for 
		# FRAME_MEMORY_LIMIT frames after a face has been detected. 
		self.detectionFrameCounter = 0 

	def run(self):
		host = socket.gethostname()
		print(host)
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind((self.ip_addr, self.port_num))
		serversocket.listen(5) # become a server socket, maximum 5 connections

		print("Awaiting packages")
		while True:
			print("Waiting")
			connection, address = serversocket.accept()
			buff = connection.recv(64).decode()
			if( buff == self.NO_FACE ):
				self.detectionFrameCounter += 1
				print( "Using Past Face" )
				if( self.detectionFrameCounter >= self.FRAME_MEMORY_LIMIT):
					self.cam.updateData(0,0,0,0)
					
			else:
				self.detectionFrameCounter = 0
				data = buff.split(":")
				x1 = data[0]
				y1 = data[1]
				width = data[2]
				height = data[3]
				self.cam.updateData(x1, y1, width, height)
			print("recieved")
			print( self.cam )




def main():
	cam1 = Camera(0,0,0,0,False, "RED2")
	cam2 = Camera(0,0,0,0,False, "RED6")
	camList = []
	thread1 = NetworkThread("", 8091, cam1)
	thread2 = NetworkThread("", 8092, cam2)
	thread1.start() # This actually causes the thread to run
	thread2.start()	
	thread1.join()
	thread2.join()  # This waits until the thread has completed
	# At this point, both threads have completed
	print("Done")

main()
