from control import *
from scipy.integrate import simpson
import pygad

import matplotlib.pyplot as plt

# In this script

def fitness_func(solution, solution_idx):
	
	# define the control system for optimization

	s = tf('s')

	Kp, Ki, Kd = solution
	
	plant = 1 / (s**2 + 10*s + 20)
	controller = Kp + Ki/s + Kd*s
	system = feedback(plant, controller)

	# define the error criterion for the Genetic Algorithm
	
	error = abs(0 - step_response(system).outputs)**2

	# TODO GA parameter: error criterion
	J = simpson(error)
	
	# define fitness function

	# the following division is required because fitness score has to be
	# maximized in GAs
	fitness = 1.0 / J

	return fitness

ga_instance = pygad.GA(num_generations = 500,
					   sol_per_pop=15,
					   num_parents_mating=5,
					   fitness_func=fitness_func,
					   num_genes=3)

ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

ga_instance.plot_result()