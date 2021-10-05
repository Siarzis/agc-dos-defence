import socket
import time
import struct
import binascii
import yaml

# variable to choose test TCP server or RTDS
test = True

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open("frequency_measurements.txt", "w") as f:
	s.connect((IP, PORT))

	if test:
		# Test server

		# read test TCP server's reply
		test_server_reply = s.recv(1024)
		print(test_server_reply)
	else:
		# RTDS server
		
		# command that sends data to RTDS
		# s.sendall((1).to_bytes(4, 'big'))
		
		# while(True):
		for i in range(5):
			ang_velocity = s.recv(4)
			
			# convert received data point from bytes to hex
			ang_velocity_hex = binascii.hexlify(ang_velocity)
			
			# convert hexademical data point to float
			ang_velocity_float = struct.unpack('>f', binascii.unhexlify(ang_velocity_hex))[0]
			frequency = ang_velocity_float / (2 * 3.14159265359)
			print(frequency)

			f.write(str(frequency) + '\n')
			
			time.sleep(1)