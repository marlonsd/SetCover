import argparse, math, sys, glob

import numpy as np

from copy import copy
from time import time

from alg_x import *

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

		lines = {}

		error = 0

		i = 0
		for line in data[1:]:
			# lines.append(set(map(int,line.split(" "))))
			lines[i] = set(map(int,line.split(" ")))
			i+=1

		print lines[0]
		sys.exit()

		t0 = time()
		solver = DancingLinks(lines)
		solution = solver.solve()

		sets = [n.row for n in solution]

		n = len(sets)
		print n, "," ,(time() - t0)

# if __name__ == '__main__':
# 	mat = [
# 			[0,1,1,0],
# 			[1,1,0,0],
# 			[1,1,1,0],
# 			[0,0,1,1]
# 	]

# 	solver = DancingLinks(mat)
# 	solution = solver.solve()

# 	sets = [n.row for n in solution]
# 	sets.sort()

# 	print sets