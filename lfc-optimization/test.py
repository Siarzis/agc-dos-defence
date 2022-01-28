from control import *
import matplotlib.pyplot as plt

A = [[-0.5572, -0.7814],
	 [0.7814, 0]
	]

B = [[1, -1],
	 [0, 2]
	]

F = [[0, 0],
	 [0, 0],
	 [0, 0],
	 [0, 0],
	 [0, 0]
	]

# BF = np.concatenate([B, F], axis=1).tolist()

C = [[1.9691, 6.4493]
	]

test_system = ss(A, B, C, 0)

flag = 1
if flag == 0:
	response = step_response(test_system)
elif flag == 1:
	T = np.arange(0, 30, 0.1, dtype=float).tolist()
	U = [np.ones_like(T).tolist(), np.ones_like(T).tolist()]
	response = forced_response(test_system, T=T, U=U)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
print(response.outputs.shape)

ax1.plot(response.time, response.outputs)
ax1.set_title('Input 1')

ax2.plot(response.time, response.outputs)
ax2.set_title('Input 2')

plt.show()