import socket
import yaml

# variable to choose test TCP server or RTDS
test = False

if test:
	IP = '127.0.0.1'
	PORT = 65432
else:
	with open('rtds_server.yaml', 'r') as stream:
		try:
			rtds_credentials = yaml.safe_load(stream)
			IP = rtds_credentials.get('ADDRESS')['IP']
			PORT = rtds_credentials.get('ADDRESS')['PORT']
		except yaml.YAMLError as exc:
			print(exc)

print(IP, PORT)

""" with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP, PORT))
    s.sendall(b'Hello, socket!')
    data = s.recv(1024)

print('Received', repr(data)) """