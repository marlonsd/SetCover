import argparse, math, sys, glob

import numpy as np

def args_check(args):
	if(args.universe_max_value <= 0):
		print "Error: Biggest value must be a integer bigger than zero."
		sys.exit(1)

	if(args.universe_max_value < args.universe_size):
		print "Error: Can't have biggest value smaller than universe set size."
		sys.exit(1)

	if (args.subset_max_size == 0):
		print "Error: Subset maximum size can't be zero."
		sys.exit(1)

	if(args.subset_max_size > args.universe_size):
		print "Error: Can't have subset maximum size bigger than universe set size."
		sys.exit(1)

	if (args.universe_min_size > args.universe_size):
		print "Error: Inferior Limit can't be bigger than superior limit."
		sys.exit(1)

	if (args.percentage > 1 or args.percentage < 0):
		print "Error: Percentage is not a float value between 0 and 1."
		sys.exit(1)


if (__name__ == '__main__'):

	### Arguments Treatment ###
	parser = argparse.ArgumentParser()

	parser.add_argument("-us","--universe_size", type=int, default=1000,
						help="Number of elements in universe set (Default: 1000).")

	parser.add_argument("-f","--fixed_size", type=bool, default=False,
						help="If True, universe set size will be exactly universe_size; \
						otherwise it will at most universe_size (Default: False).")	

	parser.add_argument("-umin","--universe_min_size", type=int, default=10,
						help="In case fixed_size is set False, this will be the inferior \
						limit to the universe set size (Default: 10).")

	parser.add_argument("-umv","--universe_max_value", type=int, default=10000000,
						help="Biggest value in universe set (Default: 10000000).")

	parser.add_argument("-sms","--subset_max_size", type=int, default=-1,
						help="Sets a maximum size to the subsets, -1 to consider \
						a random limit such that limit < universe_size (Default: -1).")	

	parser.add_argument("-p","--percentage", type=float, default=0.4,
						help="Minimun size of subsets, percentage from universe_size -- \
						float between 0 and 1 (Default: 0.4).")

	# Parsing args
	args = parser.parse_args()

	args_check(args)

	if (args.fixed_size):
		universe_max_size = args.universe_size
	else:
		universe_max_size = np.random.random_integers(args.universe_min_size, args.universe_size+1)
		subset_max_size = args.subset_max_size
		if (subset_max_size > universe_max_size):
			subset_max_size = universe_max_size
		else:
			if (subset_max_size < 0):
				subset_max_size = np.random.random_integers(universe_max_size/2, universe_max_size)

	universe = set()

	while (len(universe) < universe_max_size):
		value = np.random.random_integers(0,args.universe_max_value)
		universe.add(value)

	subsets = [[]]

	while (not (set.union(*map(set,subsets)) == universe) and not (len(subsets)-1 >= universe_max_size*args.percentage)):
		subset_size = np.random.random_integers(1,subset_max_size+1)

		temp_universe = np.array(list(universe))
		np.random.shuffle(temp_universe)

		subset = sorted(temp_universe[:subset_size])

		subsets.append(subset)

	subsets.pop(0)

	print 'Universe:', universe

	for s in subsets:
		print s



