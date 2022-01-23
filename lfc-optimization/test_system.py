import control as ct
import matplotlib.pyplot as plt

s = ct.tf('s')

Kp, Ki, Kd = 10, 100, 50

plant = 1 / (s**2 + 10*s + 20)
controller = Kp + Ki/s + Kd*s

response = ct.step_response(ct.feedback(plant, controller))
plt.plot(response.time, response.outputs)
plt.show()
