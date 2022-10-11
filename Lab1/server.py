import socket
from datetime import datetime
import time

host = 'localhost'
port = 16789

address = socket.socket()
address.bind((host, port))

print('Starting the server at', datetime.now())

address.listen(2)

conn, addr = address.accept()

print("Connection from: " + str(addr))

data = conn.recv(1024).decode()

print("From connected user: " + str(data) + "  received at", datetime.now())

if data:
    time.sleep(5)
    conn.send(data.encode())

conn.close()
