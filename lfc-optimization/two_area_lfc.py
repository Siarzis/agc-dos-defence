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
	 [-1/(R1*Tg1), 0, -1/Tg1, 0, 0, 0, 0, 0, 0],
	 [0, 0, 0, -1/Tps2, Kps2/Tps2, 0, -a12*Kps2/Tps2, 0, 0],
	 [0, 0, 0, 0, -1/Tt2, 1/Tt2, 0, 0, 0],
	 [0, 0, 0, -1/(R2*Tg2), 0, -1/Tg2, 0, 0, 0],
	 [T12, 0, 0, -T12, 0, 0, 0, 0, 0],
	 [B1, 0, 0, 0, 0, 0, 1, 0, 0],
	 [0, 0, 0, B2, 0, 0, a12, 0, 0]
	]

B = [[0, 0],
	 [0, 0],
	 [1/Tg1, 0],
	 [0, 0],
	 [0, 0],
	 [0, 1/Tg2],
	 [0, 0],
	 [0, 0],
	 [0, 0]
	]

F = [[-Kps1/Tps1, 0],
	 [0, 0],
	 [0, 0],
	 [0, -Kps2/Tps2],
	 [0, 0],
	 [0, 0],
	 [0, 0],
	 [0, 0],
	 [0, 0]
	]

BF = np.hstack([B, F]).tolist()

C = [[1.0, 0, 0, 0, 0, 0, 0, 0, 0],
	 [0, 0, 0, 1.0, 0, 0, 0, 0, 0],
	 [0, 0, 0, 0, 0, 0, 0, 1.0, 0],
	 [0, 0, 0, 0, 0, 0, 0, 0, 1.0]
	]

two_area_lfc = ss(A, BF, C, 0)

T = np.arange(0, 30, 0.1, dtype=float).tolist()

U = [np.zeros_like(T).tolist(), np.zeros_like(T).tolist(), np.ones_like(T).tolist(), np.zeros_like(T).tolist()]

t, y = forced_response(two_area_lfc, T=T, U=U)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True)

ax1.plot(t, y[0])
ax1.set_title('Output 1')

ax2.plot(t, y[1])
ax2.set_title('Output 2')

ax3.plot(t, y[2])
ax3.set_title('Output 3')

ax4.plot(t, y[3])
ax4.set_title('Output 4')

plt.show()