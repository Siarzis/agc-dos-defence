import time

class PI:
	def __init__(self, Kp, Ki, setpoint):
		self.e = 0
		self.prev_t = -1
		self.I = 0
		self.Kp = Kp
		self.Ki = Ki
		self.SP = setpoint

	def calculate(self, current_timestep, process_value):
		t, PV = current_timestep, process_value
		
		self.e = self.SP - PV

		P = self.Kp * self.e
		self.I = self.I + self.Ki * self.e * (t - self.prev_t)

		new_PV = P + self.I
		
		return new_PV


""" if __name__ == '__main__':
	process_value = 0
	setpoint = 20

	Kp = 2
	Ki = 0.1

	pi = PI(Kp, Ki, setpoint)

	print(process_value, setpoint)

	for i in range(1000):
		process_value = pi.calculate(i, process_value)

		print(process_value, setpoint)
		# time.sleep(1) """