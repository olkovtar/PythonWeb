import socket
from datetime import datetime

host = socket.gethostname()
port = 5000

address = socket.socket()
address.bind((host, port))

print('Starting the server at', datetime.now())

address.listen(2)

conn, addr = address.accept()  # accept new connection

print("Connection from: " + str(addr))

data = conn.recv(1024).decode()

print("From connected user: " + str(data) + "  received at", datetime.now())

conn.close()
