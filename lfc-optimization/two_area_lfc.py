from control import *
import matplotlib.pyplot as plt

# In this script, the Load Frequency Control of a two-area system
# is defined by its State Space representation

# Parameters
Kps1, Tps1 = 120, 20
Kg1, Tg1 = 1, 0.08
Kt1, Tt1 = 1, 0.5
R1 = 2.4
B1 = 0.425

Kps2, Tps2 = 120, 20
Kg2, Tg2 = 1, 0.08
Kt2, Tt2 = 1, 0.5
R2 = 2.4
B2 = 0.425

T12 = 0.215
a12 = -1

A = [[-1/Tps1, Kps1/Tps1, 0, 0, 0, 0, -Kps1/Tps1, 0, 0],
	 [0, -1/Tt1, 1/Tt1, 0, 0, 0, 0, 0, 0],
	 [-1/(R1/Tg1), 0, -1/Tg1, 0, 0, 0, 0, 0, 0],
	 [0, 0, 0, -1/Tps2, Kps2/Tps2, 0, -a12*Kps2/Tps2, 0, 0],
	 [0, 0, 0, 0, -1/Tt2, 1/Tt2, 0, 0, 0],
	 [0, 0, 0, -1/(R2/Tg2), 0, -1/Tg2, 0, 0, 0],
	 [T12, 0, 0, -T12, 0, 0, 0, 0, 0],
	 [B1, 0, 0, 0, 0, 0, 1, 0, 0],
	 [0, 0, 0, B2, 0, 0, a12, 0, 0]
	]

B = [[0, 0],
	 [0, 0],
	 [Tg1, 0],
	 [0, 0],
	 [0, 0],
	 [0, Tg2],
	 [0, 0],
	 [0, 0],
	 [0, 0]
	]

F = [[-Kps1/Tps1, 0],
	 [0, 0],
	 [0, 0],
	 [0, Kps2/Tps2],
	 [0, 0],
	 [0, 0],
	 [0, 0],
	 [0, 0],
	 [0, 0]
	]

BF = np.concatenate([B, F], axis=1).tolist()

print(BF)

C = [[1.0, 0, 0, 0, 0, 0, 0, 0, 0],
	 [0, 0, 0, 1.0, 0, 0, 0, 0, 0],
	 [0, 0, 0, 0, 0, 0, 0, 1.0, 0],
	 [0, 0, 0, 0, 0, 0, 0, 0, 1.0]
	]

two_area = ss(A, BF, C, 0)

response = step_response(two_area)

plt.plot(response.time, response.outputs)

plt.show()