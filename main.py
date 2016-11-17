import argparse, math, sys, glob

import numpy as np

from copy import copy
from time import time

from constructive_heuristic import greedy_selection, first_fit_selection

if (__name__ == '__main__'):

	### Arguments Treatment ###
	parser = argparse.ArgumentParser()

	parser.add_argument("-p","--folder_path", type=str, default='instances/clean',
						help="Folder where SCP instances are located (Default: instances).")

	parser.add_argument("-f","--file_format", type=str, default='txt',
						help="Format of file where SCP instances are stored (Default: txt).")

	# Parsing args
	args = parser.parse_args()

	path = args.folder_path
	file_format = args.file_format

	files = sorted(glob.glob(path+"/*."+file_format))

	print "filename", "," , "greedy", "," , "time (seg)", "," , "first_fit", "," , "time (seg)", "," , "error"

	for file in files:
		f = open(file, 'r')

		data = f.read().splitlines()

		problem_name = file.split("/")[-1].split(".")[0]
		number_instances, max_value = map(int,data[0].split(" "))

		print problem_name, "," ,

		cols = set(range(1,max_value+1))

		lines = []

		error = 0

		for line in data[1:]:
			lines.append(set(map(int,line.split(" "))))

		t0 = time()

		condition, n = greedy_selection(copy(cols),copy(lines))
		print n, "," ,(time() - t0), "," ,

		if not condition:
			error+=1

		t0 = time()

		condition, n = first_fit_selection(copy(cols),copy(lines))
		print n, "," , (time() - t0), "," ,

		if not condition:
			error+=1

		print error