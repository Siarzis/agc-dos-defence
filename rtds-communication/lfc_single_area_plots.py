import matplotlib.pyplot as plt
import numpy as np
import yaml

with open('rtds_server.yaml', 'r') as stream:
		try:
			filename_paths = yaml.safe_load(stream)
			filename =  filename_paths.get('plots')['dataset1']
		except yaml.YAMLError as exc:
			print(exc)

with open(filename) as f:
	lines = f.readlines()
	power = [float(line.split(',')[0]) for line in lines]
	speed = [float(line.split(',')[1]) for line in lines]
	ace = [float(line.split(',')[2]) for line in lines]

start, end, step = 0000, 12000, 1

fig, axs = plt.subplots(2)

axs[0].scatter(np.arange(len(power[start:end:step])), power[start:end:step], s=0.8)
axs[0].set_title('Active Power G1')

axs[1].scatter(np.arange(len(ace[start:end:step])), ace[start:end:step], s=0.8)
axs[1].set_title('ACE')

axs[0].grid()
axs[1].grid()

plt.show()