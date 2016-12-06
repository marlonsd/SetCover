import math, sys

import numpy as np
from copy import copy

def is_feasible(cols, lines, solution):
	sol_set = set()

	for pos in solution:
		sol_set.update(lines[pos])

	return set(cols) == sol_set

"""
GRAPS
"""

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

def local_improvement(cols, lines, solution, p, max_flips):

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

def grasp(cols, lines, n_iterations=500, alpha=0.9, p=0.75, max_flips=None, seed=None, log_file=None):

	best_known_solution = None

	if not seed == None:
		np.random.seed(seed)

	for k in range(n_iterations):
		if log_file:
			log_file.write("Grasp Iteration "+str(k)+'\n')
		solution = constructive_phase(cols, lines, alpha)
		solution = local_improvement(cols, lines, solution, p, max_flips)

		best_known_solution, _ = update_solution(best_known_solution, solution)

	return len(best_known_solution)

"""
Genetic Algorithm
"""

def best_fit(cols, lines, s):
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
					best_solutions.insert(0, copy(short_solution))
					best_solution = copy(short_solution)
				else:
					best_solutions.append(copy(short_solution))

	return sorted(best_solution)

def mutation(cols, lines, s):
	new_solution = copy(s)
	feasible = False

	possibilites = list(set(range(len(lines))) - set(s))

	saved_solution = copy(s)

	while (not feasible):
		chosen = np.random.choice(possibilites)

		new_solution.append(chosen)

		feasible = is_feasible(cols, lines, new_solution)
		saved_solution = copy(new_solution)
		new_solution = copy(s)

	return sorted(saved_solution)

def reproduction(cols, lines, p, m):

	if (len(p) == 1):
		return p

	if (len(p) % 2):
		p.pop(-1)

	offspring = []

	i = 0 
	while(len(p) > 0):
		# print "\tReprodution", i
		parent1 = p.pop(np.random.randint(len(p)))
		offspring.append(parent1)

		parent2 = p.pop(np.random.randint(len(p)))
		offspring.append(parent2)
		child = best_fit(cols, lines, sorted(list(set(parent1+parent2))))

		if (np.random.random() < m):
			child = mutation(cols, lines, child)

		offspring.append(child)
		i+=1

	return sorted(offspring)

def genetic_algorithm(cols, lines, n_iterations=100, alpha=0.9, population_size=100, cross_over_ration = 0.5,
					  mutation_ratio=0.2, seed=None, log_file=None):

	if not seed == None:
		np.random.seed(seed)

	population = []

	for k in range(population_size):
		solution = constructive_phase(cols, lines, alpha)
		population.append(solution)

	# Evaluation of fitness
	population = sorted(population, key=lambda x : len(x))

	for k in range(n_iterations):
		if log_file:
			log_file.write("Generation "+str(k+1)+'\n')

		# Selection of parents
		parents_selection = int(len(population)*cross_over_ration)

		# Make sure to have an even number of parents
		if (parents_selection % 2):
			parents_selection += 1

		population = population[:parents_selection]

		population = reproduction(cols, lines, population, mutation_ratio)

		# Evaluation of fitness
		population = sorted(population, key=lambda x : len(x))

		# Selection of the fittest
		population = population[:population_size]

	return len(population[0])

