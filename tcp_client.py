import socket

IP = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP, PORT))
    s.sendall(b'Hello, socket!')
    data = s.recv(1024)

print('Received', repr(data))