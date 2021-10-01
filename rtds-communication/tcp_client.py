import socket
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((IP, PORT))

	if test:
		test_server_reply = s.recv(1024)
		print(test_server_reply)
	else:
		for i in range(20):
			# define which measurements should be received
			s.send('frequency_float = MeterCapture("W2");')
			s.send('sprintf(frequency_string, "W2 = %f END", frequency_float);')
			s.send('ListenOnPortHandshake(frequency_string);')

			# get measurements
			tokenstring = s.recv(1024)
			print('Frequency value at time step ', i, ' is: ', tokenstring)

			# following command is sent to RTDS TCP server to stop
			# for 1.0 seconds
			s.send('SUSPEND 1.0;')