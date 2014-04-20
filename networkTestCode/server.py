import socket

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
	
