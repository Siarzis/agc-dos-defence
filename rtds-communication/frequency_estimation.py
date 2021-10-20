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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open("frequency_measurements.txt", "w") as f:
	s.connect((IP, PORT))
	print('Successfully conected to %s:%i' % (IP , PORT))

	pi = PID(Kp, Ki, Kd, setpoint=setpoint)
	
	previous_time = time.time_ns() / (10 ** 9)

	while(True):
		ang_velocity = s.recv(4)
		power_gen1 = s.recv(4)
		
		# convert received data point from bytes to hex
		power_gen1_hex = binascii.hexlify(power_gen1)

		# convert hexademical data point to float
		power_gen1_float = struct.unpack('>f', binascii.unhexlify(power_gen1_hex))[0]

		# angular velocity estimation => w = 2*pi*(P-P0)/R + w0
		ang_velocity_estimation = -(2 * 3.14159265359)*(power_gen1_float - 71.67)/34.02 + 377.0

		# select sampling time
		current_time = time.time_ns() / (10 ** 9)
		time_diff = current_time - previous_time

		if time_diff > 3.001:
			previous_time = current_time

			# compute Area Control Error (ACE)
			ace_float = pi(ang_velocity_estimation)
			print(ace_float)
			ace = bytearray(struct.pack('>f', ace_float))

			s.sendall(ace)

			frequency = ang_velocity_estimation / (2 * 3.14159265359)
			f.write(str(ang_velocity_estimation) + ' ' + str(ace_float) + '\n')