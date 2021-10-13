import socket
import time
import struct
import binascii
import yaml

from simple_pid import PID

# variable to choose test TCP server or RTDS TCP server
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

Kp = 0.0
Ki = 0.001
Kd = 0.0
setpoint = 377.0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open("frequency_measurements.txt", "w") as f:
	s.connect((IP, PORT))
	print('Successfully conected to %s:%i' % (IP , PORT))

	pi = PID(Kp, Ki, Kd, setpoint=setpoint)

	if test:
		# Test server

		# read test TCP server's reply
		test_server_reply = s.recv(1024)
		print(test_server_reply)
	else:
		# RTDS server
		
		previous_time = time.time_ns() / (10 ** 9)

		while(True):
			ang_velocity = s.recv(4)
			
			# convert received data point from bytes to hex
			ang_velocity_hex = binascii.hexlify(ang_velocity)
			
			# convert hexademical data point to float
			ang_velocity_float = struct.unpack('>f', binascii.unhexlify(ang_velocity_hex))[0]

			# select sampling time
			current_time = time.time_ns() / (10 ** 9)
			time_diff = current_time - previous_time

			if time_diff > 3.001:
				print(time.time())
				previous_time = current_time

				# compute Area Control Error (ACE)
				ace_float = pi(ang_velocity_float)
				ace = bytearray(struct.pack('>f', ace_float))

				s.sendall(ace)

				frequency = ang_velocity_float / (2 * 3.14159265359)
				f.write(str(ang_velocity_float) + ' ' + str(ace_float) + '\n')