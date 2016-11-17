import argparse, math, sys, glob

from time import time

from dlx import *

from itertools import chain, combinations

import numpy as np

if (__name__ == '__main__'):

	### Arguments Treatment ###
	parser = argparse.ArgumentParser()

	parser.add_argument("-p","--folder_path", type=str, default='instances/clean',
						help="Folder where TSP instances are located (Default: instances).")

	parser.add_argument("-f","--file_format", type=str, default='txt',
						help="Format of file where TSP instances are stored (Default: txt).")

	# Parsing args
	args = parser.parse_args()

	path = args.folder_path
	file_format = args.file_format

	files = sorted(glob.glob(path+"/*."+file_format))

	for file in files:
		f = open(file, 'r')

		print file,

		data = f.read().splitlines()

		problem_name = file.split("/")[-1].split(".")[0]
		number_instances, max_value = map(int,data[0].split(" "))

		cols = set(range(1,max_value+1))

		lines = []

		for line in data[1:]:
			lines.append(set(map(int,line.split(" "))))

		


