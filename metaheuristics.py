import math, sys

import numpy as np
from copy import copy

def is_feasible(cols, lines, solution):
	sol_set = set()

	for pos in solution:
		sol_set.update(lines[pos])

	return set(cols) == sol_set

def update_solution(solution, new_solution):
	if solution[0] == None:
		return new_solution

	if new_solution[0] < solution[0]:
		return new_solution

	return solution

def constructive_phase(cols, lines, alpha):
	pass

def local_improvement(cols, lines, solution, p, max_flips):
	def best_flip(s):
		pass

	def random_flip(s):
		pass

	if max_flips == None:
		max_flips = 10*len(lines)

	best_solution = None

	for i in range(max_flips):
		if np.random.random() < p:
			solution = best_solution(solution)
		else:
			solution = random_solution(solution)

		best_solution = update_solution(best_solution, solution)

	return best_solution

def grasp(cols, lines, n_iterations=500, alpha=0.9, p=0.75, max_flips=None, seed=None):

	best_solution = (None, None)

	if not seed == None:
		np.random.seed(seed)

	for k in range(n_iterations):
		solution = constructive_phase(cols, lines, alpha)
		solution = local_improvement(cols, lines, solution, p, max_flips)

		best_solution = update_solution(best_solution, solution)

	return best_solution
