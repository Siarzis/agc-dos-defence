from control import *
import matplotlib.pyplot as plt

# In this script, the Load Frequency Control of a two-area system
# is defined by its State Space representation

# Parameters
Kps1, Tps1 = 1, 20
Kg1, Tg1 = 1, 0.8
Kt1, Tt1 = 1, 0.3
R1 = 2.4

Kps1, Tps1 = 1, 20
Kg2, Tg2 = 1, 0.8
Kt2, Tt2 = 1, 0.3
R2 = 2.4

A = [[0, 1.], [-k/m, -b/m]]
B = [[0], [1/m]]
C = [[1., 0]]
sys = ss(A, B, C, 0)