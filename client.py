import socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('129.21.58.247', 8090))
message = 'Banana Pancakes'
clientsocket.send(message.encode())
