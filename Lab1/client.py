import socket

host = socket.gethostname()
port = 5000

address = socket.socket()
address.connect((host, port))

message = input(" -> ")

address.send(message.encode())

address.close()
