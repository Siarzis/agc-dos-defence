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
setpoint = 377.0 + 86.71 + 24.08

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
			power_gen1 = s.recv(4)
			power_tie_line3 = s.recv(4)
			power_tie_line6 = s.recv(4)
			
			# convert received data point from bytes to hex
			ang_velocity_hex = binascii.hexlify(ang_velocity)
			power_gen1_hex = binascii.hexlify(power_gen1)
			power_tie_line3_hex = binascii.hexlify(power_tie_line3)
			power_tie_line6_hex = binascii.hexlify(power_tie_line6)
			
			# convert hexademical data point to float
			ang_velocity_float = struct.unpack('>f', binascii.unhexlify(ang_velocity_hex))[0]
			power_gen1_float = struct.unpack('>f', binascii.unhexlify(power_gen1_hex))[0]
			power_tie_line3_float = struct.unpack('>f', binascii.unhexlify(power_tie_line3_hex))[0]
			power_tie_line6_float = struct.unpack('>f', binascii.unhexlify(power_tie_line6_hex))[0]

			# select sampling time
			current_time = time.time_ns() / (10 ** 9)
			time_diff = current_time - previous_time

			if time_diff > 3.001:
				previous_time = current_time

				# scheduled power of tie-lines: P_TL_31 = -84.36 , P_TL_32 = 86.71 , P_TL_61 = -23.98 , P_TL_62 = 24.08

				# compute Area Control Error (ACE)
				ace1_float = pi(ang_velocity_float + power_tie_line3_float + power_tie_line6_float)
				ace1 = bytearray(struct.pack('>f', ace1_float))

				print(power_gen1_float, ang_velocity_float, ace1_float)
				s.sendall(ace1)

				ace2_float = pi(ang_velocity_float - power_tie_line3_float - power_tie_line6_float)
				ace2 = bytearray(struct.pack('>f', ace2_float))

				print(power_gen1_float, ang_velocity_float, ace2_float)
				s.sendall(ace2)

				# frequency = ang_velocity_float / (2 * 3.14159265359)
				# f.write(str(power_gen1_float) + ', ' + str(ang_velocity_float) + ', ' + str(ace_float) + '\n')