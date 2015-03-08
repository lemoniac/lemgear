#!/usr/bin/python

import sys

data = open(sys.argv[1], "rt").read().split("\n")

for line in data:
	if line.startswith("#"):
		continue

	inst = line.split("-")

	if len(inst) != 3:
		continue

	opcodes = inst[0].split()

	if opcodes[0] == "00":
		print "\tif byte == 0x" + opcodes[0] + ":"
	else:
		print "\telif byte == 0x" + opcodes[0] + ":"

	if len(opcodes) > 1:
		if opcodes[1] == "nn":
			print "\t\tvalue = get_byte()"
		elif opcodes[1] == "nnnn":
			print "\t\tvalue = get_address()"

	fun = inst[2].split()

	f = fun[0] + "("
	
	if len(fun) > 1:
		for i in range(1, len(fun)):
			if i > 1:
				f += ", "
			if fun[i] == "nn" or fun[i] == "nnnn":
				f += "value"
			else:
				f += fun[i]
	
	f += ")"
	print "\t\tz80." + f

