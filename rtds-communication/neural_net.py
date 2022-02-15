import yaml
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
# from sklearn.metrics import mean_absolute_error as mae

def window_stack(a, stepsize=1, width=3):
	n = a.shape[0]
	return np.hstack(a[i:1+n+i-width:stepsize] for i in range(0,width))

# purpose of Dataset class -> return a pair of [input, label] 
# represents the dataset as an object of a class, not a set of data and labels
class PrepareData(Dataset):

	def __init__(self, filename, w):

		with open(filename) as f:
			a = np.loadtxt(f, delimiter = ',')
			# reshape(-1, 1) turns row vectors to column vectors
			# pytorch requires inputs as column vectors
			self.x, self.y = a[:, 0].reshape(-1, 1), a[:, 1].reshape(-1, 1)
		
		# the result of the following np.pad() is:
		#			[[.]
		#			 [.]
		# [[a1]		 [.]
		#  [a2]	 ->  [0] 
		#  [a3]]  	 [0]
		#  	   	     [a1]
		#  	 		 [a2]
		#			 [a3]]
		self.x = np.pad(self.x, ((w, 0), (0, 0)), 'constant', constant_values=(self.x[0]))
		# the result of the window_stack() is:
		# [  0.        ]	[  0.         0.         0.         0.         0.      ]
		# [  0.        ]	[  0.         0.         0.         0.       107.484505]
		# [  0.        ]	[  0.         0.         0.       107.484505 106.50603 ]
		# [  0.        ]	[  0.         0.       107.484505 106.50603  105.52754 ]
		# [  0.        ] -> [  0.       107.484505 106.50603  105.52754  104.54906 ]
		# [107.4845047 ]	[107.484505 106.50603  105.52754  104.54906  103.57058 ]
		# [106.50602341]	.
		# [105.52754211]	.
		# [104.54906082]	.
		# [103.57057953]	.
		self.x = window_stack(self.x[:-1], width = w).astype(np.float32)
		self.x = torch.from_numpy(self.x)

		self.y = torch.from_numpy(self.y)			
    
	def __len__(self):
		return len(self.x)
    
	# function that returns one training example, a pair of [input, label] 
	def __getitem__(self, index):
		_x = self.x[index]
		_y = self.y[index]
        
		return _x, _y


with open('rtds_server.yaml', 'r') as stream:
		try:
			filename_paths = yaml.safe_load(stream)
			train_file =  filename_paths.get('files')['train_1']
			test_file =  filename_paths.get('files')['test_1']
		except yaml.YAMLError as exc:
			print(exc)

# hyperparameter definition

w = 20
learning_rate = 0.0001
input_neurons = w
hidden_neurons_1 = 8
output_neurons = 1
number_of_epochs = 200
bs = 64

# DataLoader provides useful functionalities like batch training, multiprocessing, etc.
train_dataset = PrepareData(train_file, w)
train_dataloader = DataLoader(dataset=PrepareData(train_file, w), batch_size=bs)
test_dataset = PrepareData(test_file, w)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Using {} device'.format(device))

class Net(torch.nn.Module):

	def __init__(self, n_feature, n_hidden_1, n_output):
		super(Net, self).__init__()
		self.linear_relu_stack = nn.Sequential(
			nn.Linear(n_feature, n_hidden_1),
			nn.ReLU(),
			nn.Linear(n_hidden_1, n_output),
		)

	def forward(self, x):
		x = self.linear_relu_stack(x)
		return x

# define Neural Net architecture
neural_net = Net(n_feature = input_neurons,
				 n_hidden_1 = hidden_neurons_1,
				 n_output= output_neurons)

# configure optimizer
optimizer = torch.optim.Adam(neural_net.parameters(), lr = learning_rate)

# select loss function
loss_function = nn.MSELoss()

losses = []
for e in range(number_of_epochs):
	running_loss = 0.0

	# mini-batch Gradient Descent
	for x_batch, y_batch in train_dataloader:

		# forward pass
		prediction = neural_net(x_batch)

		loss = loss_function(prediction, y_batch.float())

		# backward pass
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

		running_loss += loss.item() * x_batch.size(0)

	epoch_loss = running_loss / len(x_batch)
	losses.append(epoch_loss)

# plt.plot(losses)
# plt.show()

results = [neural_net(t[0]).detach().numpy() for t in test_dataset]
target = [t[1].detach().numpy() for t in test_dataset]
input_timeseries = [t[0][0].detach().numpy() for t in test_dataset]

# print('Mean Absolute Error:', mae(target, results))

plt.grid()
plt.title('Line Graph')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.plot(results, color = 'blue')
plt.plot(target, color = 'green')
# plt.plot(input_timeseries, color = 'red')
plt.show()