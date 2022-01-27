from control import *
import matplotlib.pyplot as plt

s = tf('s')
	
Kp1, Ki1, Kd1 = 200, 100, 50
Kp2, Ki2, Kd2 = 524.06857637, 690.12146414, 16.03660779
	
plant = 1 / (s**2 + 10*s + 20)
controller_1 = Kp1 + Ki1/s + Kd1*s
controller_2 = Kp2 + Ki2/s + Kd2*s

response_1 = step_response(feedback(plant, controller_1))
response_2 = step_response(feedback(plant, controller_2))

plt.plot(response_1.time, response_1.outputs, label='Controller 1')
plt.plot(response_2.time, response_2.outputs, label='Controller 2')
plt.legend(loc='upper right')

plt.show()