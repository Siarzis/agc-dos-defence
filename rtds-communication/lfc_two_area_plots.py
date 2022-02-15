import matplotlib.pyplot as plt
import numpy as np
import yaml

with open('rtds_server.yaml', 'r') as stream:
		try:
			filename_paths = yaml.safe_load(stream)
			filename =  filename_paths.get('plots')['dataset']
		except yaml.YAMLError as exc:
			print(exc)

with open(filename) as f:
	lines = f.readlines()
	power = [float(line.split(',')[0]) for line in lines]
	tie3 = [float(line.split(',')[1]) for line in lines]
	tie4 = [float(line.split(',')[2]) for line in lines]
	ace1 = [float(line.split(',')[3]) for line in lines]
	ace2 = [float(line.split(',')[4]) for line in lines]

start, end, step = 1000, 7000, 1

fig, axs = plt.subplots(5)

axs[0].scatter(np.arange(len(power[start:end:step])), power[start:end:step], s=0.8)
axs[0].set_title('Active Power G1')

axs[1].scatter(np.arange(len(tie3[start:end:step])), tie3[start:end:step], s=0.8)
axs[1].set_title('Tie Line 3')

axs[2].scatter(np.arange(len(tie4[start:end:step])), tie4[start:end:step], s=0.8)
axs[2].set_title('Tie Line 4')

axs[3].scatter(np.arange(len(ace1[start:end:step])), ace1[start:end:step], s=0.8)
axs[3].set_title('ACE1')

axs[4].scatter(np.arange(len(ace2[start:end:step])), ace2[start:end:step], s=0.8)
axs[4].set_title('ACE2')

axs[0].grid()
axs[1].grid()
axs[2].grid()
axs[3].grid()
axs[4].grid()

plt.show()