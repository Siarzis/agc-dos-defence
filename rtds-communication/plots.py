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
	velocity = [float(line.split(',')[1]) for line in lines]
	ace = [float(line.split(',')[2]) for line in lines]

fig, axs = plt.subplots(2)

axs[0].plot(power)
axs[0].set_title('Active Power G1')

axs[1].plot(ace)
axs[1].set_title('ACE')

axs[0].grid()
axs[1].grid()
plt.show()