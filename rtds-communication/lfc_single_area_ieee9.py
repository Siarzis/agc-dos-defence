import socket
import time
import struct
import binascii
import yaml

from simple_pid import PID

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open("power_ace_15-02-2022.txt", "w") as f:
	s.connect((IP, PORT))
	print('Successfully conected to %s:%i' % (IP , PORT))

	pi = PID(Kp, Ki, Kd, setpoint=setpoint)

	previous_time = time.time_ns() / (10 ** 9)

	while(True):
		ang_velocity = s.recv(4)
		power_gen1 = s.recv(4)
		ace = s.recv(4)
			
		# convert received data point from bytes to hex
		ang_velocity_hex = binascii.hexlify(ang_velocity)
		power_gen1_hex = binascii.hexlify(power_gen1)
		ace_hex = binascii.hexlify(ace)
			
		# convert hexademical data point to float
		ang_velocity_float = struct.unpack('>f', binascii.unhexlify(ang_velocity_hex))[0]
		power_gen1_float = struct.unpack('>f', binascii.unhexlify(power_gen1_hex))[0]
		ace_float = struct.unpack('>f', binascii.unhexlify(ace_hex))[0]

		# select sampling time
		current_time = time.time_ns() / (10 ** 9)
		time_diff = current_time - previous_time

		if time_diff > 0.101:
			previous_time = current_time

			# # compute Area Control Error (ACE)
			# ace_float = pi(ang_velocity_float)
			# ace = bytearray(struct.pack('>f', ace_float))
			
			print(power_gen1_float, ang_velocity_float, ace_float)
			# s.sendall(ace)

			frequency = ang_velocity_float / (2 * 3.14159265359)
			f.write(str(power_gen1_float) + ', ' + str(ang_velocity_float) + ', ' + str(ace_float) + '\n')