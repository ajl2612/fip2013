import threading
from threading import Barrier
import sys
#from threadServer import NetworkThread

class MasterThread(threading.Thread):
	def __init__(self):
		super(MasterThread, self).__init__()
		self.fname  = sys.argv[1]		

	def run(self):
		ipAddrs = []
		portNums = []
		
		for line in open( self.fname ):
			data = line.strip().split( " " )
			ipAddrs.append( data[0] )
			portNums.append( int(data[1]) )
		numThreads = len( ipAddrs )
		timeout = 5
		bar = Barrier( numThreads, timeout )
		for index in range(0, len(ipAddrs) ):
			print( index )


def main():
	thread1 = MasterThread()
	thread1.start()
	thread1.join()
	print( "Finished" )

main()
