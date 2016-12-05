import argparse, math, sys, glob

import numpy as np

from copy import copy
from time import time

from metaheuristics import grasp

if (__name__ == '__main__'):

	### Arguments Treatment ###
	parser = argparse.ArgumentParser()

	parser.add_argument("-fp","--folder_path", type=str, default='instances/clean',
						help="Folder where SCP instances are located (Default: instances).")

	parser.add_argument("-f","--file_format", type=str, default='txt',
						help="Format of file where SCP instances are stored (Default: txt).")

	# n_iterations=500, alpha=0.9, p=0.75, max_flips=None, seed=None)

	parser.add_argument("-n","--n_iterations", type=int, default=500,
						help="Maximum number of iteration executed by the metaheuristics (Default: 500).")

	parser.add_argument("-a","--alpha", type=float, default=0.9,
						help="Alpha parameter for the randomized greedy algorithm (Default: 0.9).")

	parser.add_argument("-p","--prob", type=float, default=0.75,
						help="Chance to choose best fit instead of random fit for the GRASP local improviment (Default: 0.75).")

	parser.add_argument("-m","--max_flips", type=int, default=0,
						help="Maximum number of flips in GRASP's local improviment; 0 means it is 10 times the size of sets set (Default: 0).")

	parser.add_argument("-s","--seed", type=int, default=0,
						help="Seed for the random algorithms; 0 means no seed being used (Default: 0).")

	parser.add_argument("-l","--log", action="store_true",
						help="Enable logging ")

	parser.add_argument("-lf","--log_file", type=str, default='log.txt',
						help="Filename for logging (Default: log.txt).")	

	# Parsing args
	args = parser.parse_args()

	path = args.folder_path
	file_format = args.file_format

	n_iterations = args.n_iterations
	alpha = args.alpha
	p = args.prob
	max_flips = args.max_flips
	seed = args.seed

	if max_flips <= 0:
		max_flips = None

	if seed <= 0:
		seed = None

	files = sorted(glob.glob(path+"/*."+file_format))

	print "filename", "," , "grasp", "," , "time (seg)"#, "," , "first_fit", "," , "time (seg)", "," , "error"

	log = None

	if args.log:
		log = open(args.log_file, 'w')
		log.close()

	for file in files:
		f = open(file, 'r')

		data = f.read().splitlines()

		problem_name = file.split("/")[-1].split(".")[0]
		number_instances, max_value = map(int,data[0].split(" "))

		cols = set(range(1,max_value+1))

		lines = []

		error = 0

		for line in data[1:]:
			lines.append(set(map(int,line.split(" "))))

		print problem_name, "," ,

		if args.log:
			log = open(args.log_file, 'w+')
			log.write(problem_name+'\n')

		t0 = time()

		n = grasp(copy(cols),copy(lines), n_iterations=n_iterations, alpha=alpha, p=p, max_flips=max_flips, seed=seed, log_file=log)
		print n, "," ,(time() - t0), "," ,

		print
		# t0 = time()
		# condition, n = first_fit_selection(copy(cols),copy(lines))
		# print n, "," , (time() - t0), "," ,

		f.close()

		if args.log:
			log.write("\n")
			log.close()
