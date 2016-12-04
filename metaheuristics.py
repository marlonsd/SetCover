import math, sys

import numpy as np
from copy import copy

def is_feasible(cols, lines, solution):
	sol_set = set()

	for pos in solution:
		sol_set.update(lines[pos])

	return set(cols) == sol_set

def update_solution(solution, new_solution):
	if solution == None:
		return new_solution, True

	if len(new_solution) < len(solution):
		return new_solution, True

	return solution, False

# Randomized greed algorithm
def constructive_phase(cols, lines, alpha):
	in_set = set()

	cover_set = []

	candidates = copy(lines)

	while(not (in_set == cols) and len(candidates) > 0):
		uniques = []

		for line in candidates:
			unique = len(set(line) - in_set)
			uniques.append(unique)

		uniques = np.argsort(uniques)

		# Select alpha best
		possible_selection = uniques[len(uniques) - int(len(uniques)*alpha):]

		# Picks one randomly
		chosen = np.random.choice(possible_selection)

		cover_set.append(lines.index(candidates[chosen]))

		in_set.update(candidates[chosen])

		candidates.pop(chosen)

	return sorted(cover_set)

def local_improvement(cols, lines, solution, p, max_flips):

	# Given a solution, finds the best solution (smallest)
	# reachable from the given solution
	def best_flip(cols, lines, s):
		best_solutions = [copy(s)]
		best_solution = copy(s)

		while (len(best_solutions) > 0):
			local_solution = best_solutions.pop(0)

			for i in range(len(local_solution)):
				short_solution = copy(local_solution)
				short_solution.pop(i)

				if (is_feasible(cols, lines, short_solution)):
					if (len(short_solution) < len(best_solution)):
						# print "\t\tBest Solution size", len(short_solution)
						# best_solutions.insert(0, copy(short_solution))
						best_solutions.append(copy(short_solution))
						best_solution = copy(short_solution)

		return sorted(best_solution)


	# Randomly selects a set and either add or remove it from solution
	# Until new_solution is feasible
	def random_flip(cols, lines, s):
		new_solution = copy(s)
		feasible = False

		possibilites = range(len(lines))

		saved_solution = copy(s)

		while (not feasible):
			chosen = np.random.choice(possibilites)

			if (chosen in new_solution):
				new_solution.pop(new_solution.index(chosen))
			else:
				new_solution.append(chosen)

			feasible = is_feasible(cols, lines, new_solution)
			saved_solution = copy(new_solution)
			new_solution = copy(s)

		return saved_solution

	if max_flips == None:
		max_flips = 10*len(lines)

	best_solution = None

	for i in range(max_flips):
		# print "\tImproviment Iteration", i,
		if np.random.random() < p:
			# print "Best Flip"
			solution = best_flip(cols, lines, solution)
		else:
			# print "Random Flip"
			solution = random_flip(cols, lines, solution)

		best_solution, cond = update_solution(best_solution, solution)
		if not cond:
			return best_solution

	return best_solution

def grasp(cols, lines, n_iterations=500, alpha=0.9, p=0.75, max_flips=None, seed=None):

	best_known_solution = None

	if not seed == None:
		np.random.seed(seed)

	print 

	for k in range(n_iterations):
		print "Grasp Iteration", k
		solution = constructive_phase(cols, lines, alpha)
		solution = local_improvement(cols, lines, solution, p, max_flips)

		best_known_solution, _ = update_solution(best_known_solution, solution)

	return len(best_known_solution)
