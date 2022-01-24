from control import *
from scipy.integrate import simpson
import matplotlib.pyplot as plt



def pid_optimizer(x):
	s = tf('s')
	
	Kp, Ki, Kd = x[0], x[1], x[2]
	
	plant = 1 / (s**2 + 10*s + 20)
	controller = Kp + Ki/s + Kd*s
	
	error = abs(0 - step_response(feedback(plant, controller)).outputs)

	# TODO GA parameter: error criterion
	J = simpson(error)

	return J
	
	# plt.plot(response.time, response.outputs)
	# plt.show()

Kp, Ki, Kd = 100, 200, 50

pid_optimizer([Kp, Ki, Kd])