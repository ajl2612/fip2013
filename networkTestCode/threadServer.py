import socket


import threading

class NetworkThread(threading.Thread):
	def __init__(self,ip_addr,port_num):
        	super(NetworkThread, self).__init__()
		self.ip_addr = ip_addr
		self.port_num = port_num

	def run(self):
		host = socket.gethostname()
		print(host)
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(('', 8090))
		serversocket.listen(5) # become a server socket, maximum 5 connections

		print("Awaiting packages")
		while True:
			print("Waiting")
		        connection, address = serversocket.accept()
		        buf = connection.recv(64).decode()
		        print("recieved")
		        if len(buf) > 0:
		                print(buf)




def main():
	thread1 = NetworkThread("",8090)
	thread1.start() # This actually causes the thread to run
	thread1.join()  # This waits until the thread has completed
	# At this point, both threads have completed
	print("Done")

main()
