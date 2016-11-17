import math, sys, glob

from time import time

import numpy as np

def greedy_selection(cols, lines):
	in_set = set()

	n_sets_chosen = 0

	while(not (in_set == cols) and len(lines) > 0):
		uniques = []

		for line in lines:
			unique = len(set(line) - in_set)
			uniques.append(unique)

		uniques = np.argsort(uniques)

		chosen = uniques[-1]

		in_set.update(lines[chosen])

		lines.pop(chosen)

		n_sets_chosen+=1

	return (in_set == cols), n_sets_chosen

def first_fit_selection(cols, lines):
	in_set = set()

	n_sets_chosen = 0

	lines = sorted(lines,key=lambda x : len(x))[::-1]

	while(not (in_set == cols) and len(lines) > 0):

		i = 0
		condition = not (len(lines[i] - in_set))
		while (condition):
			i+=1

			if (i >= len(lines)):
				condition = False
				i = len(lines) - 1
			else:
				condition = not (len(lines[i] - in_set))

		# print lines[i] - in_set
		in_set.update(lines[i])

		lines.pop(i)

		n_sets_chosen+=1

	return (in_set == cols), n_sets_chosen