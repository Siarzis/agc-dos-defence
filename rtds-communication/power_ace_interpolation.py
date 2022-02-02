import matplotlib.pyplot as plt
import numpy as np

with open("C:\\Users\\andre\\Documents\\data\\frequency_ace_measurements\\power_frequency_ace_01-02-2022.txt") as f:
	lines = f.readlines()
	power = [float(line.split(',')[0]) for line in lines]
	velocity = [float(line.split(',')[1]) for line in lines]
	ace = [float(line.split(',')[1]) for line in lines]

time = 220

x = np.arange(0, len(power[:time]), 1, dtype=float).tolist()

x_sample = np.arange(0, len(power[:time]), 0.1, dtype=float).tolist()
power_interp = np.interp(x_sample, x, power[:time])
ace_interp = np.interp(x_sample, x, ace[:time])

fig, axs = plt.subplots(2)

axs[0].scatter(x_sample, power_interp, s=1, c = ['tab:orange'])
axs[0].scatter(x, power[:time], s=3)
axs[0].hlines(y=71.66, xmin = 0, xmax = 220, linewidth=0.8, linestyles='--', color='r')
axs[0].set_title('Active Power G1')

axs[1].scatter(x_sample, ace_interp, s=1, c = ['tab:orange'])
axs[1].scatter(x, ace[:time], s=3)
axs[1].set_title('ACE')

# with open("measurements_generation.txt", "w") as f:
# 	for i in range(len(power_interp)):
# 		f.write(str(power_interp[i]) + ', ' + str(ace_interp[i]) + '\n')

# axs[2].plot(velocity[:220])
# axs[2].set_title('Angular Velocity')

axs[0].grid()
axs[1].grid()
plt.show()