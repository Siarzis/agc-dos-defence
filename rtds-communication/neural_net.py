import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import mean_absolute_error as mae

w = 100

def window_stack(a, stepsize=1, width=3):
	n = a.shape[0]
	return np.hstack(a[i:1+n+i-width:stepsize] for i in range(0,width))

class PrepareData(Dataset):
		
	def __init__(self, np_array, w):
		# use 'a.reshape(-1, 1)' for line regression or '(3 + np.sin(a)).reshape(-1, 1)' for sine regression
		# x_train = a.reshape(-1, 1)
		self.x = (np.sin(np_array[w:])).reshape(-1, 1)
		self.x = np.pad(self.x, ((w, 0), (0, 0)), 'constant', constant_values=(0.0))
		self.x = window_stack(self.x[:-1], width = w).astype(np.float32)
		self.x = torch.from_numpy(self.x)
			
		# use '(10 - a[10:]).reshape(-1, 1)' for line regression or '(-3 + np.sin(a[10:])).reshape(-1, 1)' for sine regression
		# y_train = (10 - a[10:]).reshape(-1, 1).astype(np.float32)
		self.y = (np.cos(np_array[w:])).reshape(-1, 1).astype(np.float32)
		self.y = torch.from_numpy(self.y)
    
	def __len__(self):
		return len(self.x)
    
	def __getitem__(self, index):
		_x = self.x[index]
		_y = self.y[index]
        
		return _x, _y

train_dataloader = DataLoader(dataset=PrepareData(np.arange(0, 10, 0.01), w), batch_size=64)
test_dataset = PrepareData(np.arange(20, 30, 0.01), w)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Using {} device'.format(device))

# hyperparameter definition

learning_rate = 0.002
input_neurons = w
hidden_neurons_1 = 20
output_neurons = 1
number_of_epochs = 200

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

for e in range(number_of_epochs):

	# mini-batch Gradient Descent
	for x_batch, y_batch in train_dataloader:

		# forward pass
		prediction = neural_net(x_batch)
		loss = loss_function(prediction, y_batch)

		# backward pass 
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

results = [neural_net(t[0]) for t in test_dataset]
target = [t[1] for t in test_dataset]
input_timeseries = [t[0][0] for t in test_dataset]

print('Mean Absolute Error:', mae(target, results))

plt.grid()
plt.title('Line Graph')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.plot(results, color = 'blue')
plt.plot(target, color = 'green')
plt.plot(input_timeseries, color = 'red')
plt.show()