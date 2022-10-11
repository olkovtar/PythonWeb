import socket
from datetime import datetime

host = 'localhost'
port = 16789

address = socket.socket()
address.connect((host, port))

message = input(" -> ")

address.send(message.encode())

data = address.recv(1024).decode()

print('Received from server: ' + data, datetime.now())

address.close()
