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

def default_time_vector(sys, N=None, tfinal=None, is_step=True):
	"""Returns a time vector that has a reasonable number of points.
	if system is discrete-time, N is ignored """

	N_max = 5000
	N_min_ct = 100    # min points for cont time systems
	N_min_dt = 20     # more common to see just a few samples in discrete time

	ideal_tfinal, ideal_dt = _ideal_tfinal_and_dt(sys, is_step=is_step)

	if isdtime(sys, strict=True):
		# only need to use default_tfinal if not given; N is ignored.
		if tfinal is None:
			# for discrete time, change from ideal_tfinal if N too large/small
			# [N_min, N_max]
			N = int(np.clip(np.ceil(ideal_tfinal/sys.dt)+1, N_min_dt, N_max))
			tfinal = sys.dt * (N-1)
		else:
			N = int(np.ceil(tfinal/sys.dt)) + 1
			tfinal = sys.dt * (N-1)  # make tfinal integer multiple of sys.dt
	else:
		if tfinal is None:
			# for continuous time, simulate to ideal_tfinal but limit N
			tfinal = ideal_tfinal
		if N is None:
			# [N_min, N_max]
			N = int(np.clip(np.ceil(tfinal/ideal_dt)+1, N_min_ct, N_max))

	return np.linspace(0, tfinal, N, endpoint=True)

def convert_to_statespace(sys, **kw):

	import itertools

	if isinstance(sys, StateSpace):
		if len(kw):
			raise TypeError("If sys is a StateSpace, _convert_to_statespace "
							"cannot take keywords.")

		return sys

	elif isinstance(sys, TransferFunction):

		if any([[len(num) for num in col] for col in sys.num] >
				[[len(num) for num in col] for col in sys.den]):
			raise ValueError("Transfer function is non-proper; can't "
							 "convert to StateSpace system.")
		try:
			from slycot import td04ad
			if len(kw):
				raise TypeError("If sys is a TransferFunction, "
								"_convert_to_statespace cannot take keywords.")

			num, den, denorder = sys.minreal()._common_den()

			# transfer function to state space conversion now should work!
			ssout = td04ad('C', sys.ninputs, sys.noutputs,
							denorder, den, num, tol=0)

			states = ssout[0]
			return StateSpace(ssout[1][:states, :states],
							  ssout[2][:states, :sys.ninputs],
							  ssout[3][:sys.noutputs, :states], ssout[4],
							  sys.dt)
		except ImportError:

			maxn = max(max(len(n) for n in nrow)
						for nrow in sys.num)
			maxd = max(max(len(d) for d in drow)
						for drow in sys.den)
			if 1 == maxn and 1 == maxd:
				D = empty((sys.noutputs, sys.ninputs), dtype=float)
				for i, j in itertools.product(range(sys.noutputs),
												range(sys.ninputs)):
					D[i, j] = sys.num[i][j][0] / sys.den[i][j][0]
				return StateSpace([], [], [], D, sys.dt)
			else:
				if sys.ninputs != 1 or sys.noutputs != 1:
					raise TypeError("No support for MIMO without slycot")

				A, B, C, D = \
					sp.signal.tf2ss(squeeze(sys.num), squeeze(sys.den))
				return StateSpace(A, B, C, D, sys.dt)

	elif isinstance(sys, (int, float, complex, np.number)):
		if "inputs" in kw:
			inputs = kw["inputs"]
		else:
			inputs = 1
		if "outputs" in kw:
			outputs = kw["outputs"]
		else:
			outputs = 1

		return StateSpace([], zeros((0, inputs)), zeros((outputs, 0)),
							sys * ones((outputs, inputs)))

	try:
		D = _ssmatrix(sys)
		return StateSpace([], [], [], D)
	except Exception:
		raise TypeError("Can't convert given type to StateSpace system.")

def mimo2simo(sys, input, warn_conversion=False):

	if not (isinstance(input, int)):
		raise TypeError("Parameter ``input`` be an integer number.")
	if not (0 <= input < sys.ninputs):
		raise ValueError("Selected input does not exist. "
						 "Selected input: {sel}, "
						 "number of system inputs: {ext}."
						 .format(sel=input, ext=sys.ninputs))

	if sys.ninputs > 1:
		if warn_conversion:
			warn("Converting MIMO system to SIMO system. "
				 "Only input {i} is used." .format(i=input))

		new_B = sys.B[:, input:input+1]
		new_D = sys.D[:, input:input+1]
		sys = StateSpace(sys.A, new_B, sys.C, new_D, sys.dt)

	return sys

def get_ss_simo(sys, input=None, output=None, squeeze=None):

	if squeeze is None:
		squeeze = config.defaults['control.squeeze_time_response']

	sys_ss = convert_to_statespace(sys)
	if sys_ss.issiso():
		return squeeze, sys_ss
	elif squeeze is None and (input is None or output is None):
		squeeze = False

	warn = False
	if input is None:
		warn = True
		input = 0

	if output is None:
		return squeeze, mimo2simo(sys_ss, input, warn_conversion=warn)
	else:
		return squeeze, mimo2siso(sys_ss, input, output, warn_conversion=warn)

def forced_response_mimo(sys, T=None, U=0., X0=0., input=None, output=None, T_num=None,
                  transpose=False, return_x=False, squeeze=None):

	# Create the time and input vectors
	if T is None or np.asarray(T).size == 1:
		T = default_time_vector(sys, N=T_num, tfinal=T, is_step=True)
	U = U

	# Convert to state space so that we can simulate
	sys = convert_to_statespace(sys)

	# Set up arrays to handle the output
	ninputs = sys.ninputs if input is None else 1
	noutputs = sys.noutputs if output is None else 1
	yout = np.empty((noutputs, ninputs, np.asarray(T).size))
	xout = np.empty((sys.nstates, ninputs, np.asarray(T).size))
	uout = np.empty((ninputs, ninputs, np.asarray(T).size))

	# Simulate the response for each input
	for i in range(sys.ninputs):
		# If input keyword was specified, only simulate for that input
		if isinstance(input, int) and i != input:
			continue

		# Create a set of single inputs system for simulation
		squeeze, simo = get_ss_simo(sys, i, output, squeeze=squeeze)

		response = forced_response(simo, T, U[i], X0, squeeze=True)
		inpidx = i if input is None else 0
		yout[:, inpidx, :] = response.y
		xout[:, inpidx, :] = response.x
		uout[:, inpidx, :] = U

	# Figure out if the system is SISO or not
	issiso = sys.issiso() or (input is not None and output is not None)

	return TimeResponseData(
		response.time, yout, xout, uout, issiso=issiso,
		transpose=transpose, return_x=return_x, squeeze=squeeze)

flag = 1
if flag == 0:
	response = step_response(test_system)

	fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

	ax1.plot(response.time, response.outputs[0][0])
	ax1.set_title('Input 1')

	ax2.plot(response.time, response.outputs[0][1])
	ax2.set_title('Input 2')

	plt.show()
elif flag == 1:
	T = np.arange(0, 30, 0.1, dtype=float).tolist()
	U = [np.ones_like(T).tolist(), np.ones_like(T).tolist()]

	response = forced_response_mimo(test_system, T=T, U=U)

	fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

	ax1.plot(response.time, response.outputs[0][0])
	ax1.set_title('Input 1')

	ax2.plot(response.time, response.outputs[0][1])
	ax2.set_title('Input 2')

	plt.show()