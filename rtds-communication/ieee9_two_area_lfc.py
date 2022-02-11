import socket
import time
import struct
import binascii
import yaml

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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open("power_ace_11-02-2022.txt", "w") as f:
	s.connect((IP, PORT))
	print('Successfully conected to %s:%i' % (IP , PORT))
		
	previous_time = time.time_ns() / (10 ** 9)

	while(True):
		speed3 = s.recv(4)
		power3 = s.recv(4)
		tie_line3 = s.recv(4)
		tie_line4 = s.recv(4)
		ace1 = s.recv(4)
		ace2 = s.recv(4)
		
		# convert received data point from bytes to hex
		speed_hex = binascii.hexlify(speed3)
		power_hex = binascii.hexlify(power3)
		tie_line3_hex = binascii.hexlify(tie_line3)
		tie_line4_hex = binascii.hexlify(tie_line4)
		ace1_hex = binascii.hexlify(ace1)
		ace2_hex = binascii.hexlify(ace2)
			
		# convert hexademical data point to float
		speed_float = struct.unpack('>f', binascii.unhexlify(speed_hex))[0]
		power_float = struct.unpack('>f', binascii.unhexlify(power_hex))[0]
		tie_line3_float = struct.unpack('>f', binascii.unhexlify(tie_line3_hex))[0]
		tie_line4_float = struct.unpack('>f', binascii.unhexlify(tie_line4_hex))[0]
		ace1_float = struct.unpack('>f', binascii.unhexlify(ace1_hex))[0]
		ace2_float = struct.unpack('>f', binascii.unhexlify(ace2_hex))[0]

		# select sampling time
		current_time = time.time_ns() / (10 ** 9)
		time_diff = current_time - previous_time

		if time_diff > 0.101:
			previous_time = current_time

			# # compute Area Control Error (ACE)
			# ace_float = pi(ang_velocity_float)
			# ace = bytearray(struct.pack('>f', ace_float))

			# print(power_gen1_float, ang_velocity_float, ace_float)
			# s.sendall(ace)

			# frequency = ang_velocity_float / (2 * 3.14159265359)
			f.write(str(power_float) + ', ' + str(ace1_float) + ', ' + str(ace2_float) + '\n')