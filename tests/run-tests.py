#!/usr/bin/python

import glob
import os
import subprocess

all_tests = []

for test in glob.glob("*.asm"):
	base = test[:test.find(".")]
	cmd = "z80asm " + base + ".asm -o " + base + ".bin"
	os.system(cmd)
	
	all_tests.append(base)

try:
	cwd = os.getcwd()
	os.chdir("../src")

	for test in all_tests:
		expected = open("../tests/" + test + ".out", "rt").readlines()
		cmd = ["./microengine.py", "../tests/" + test + ".bin"]
		output = subprocess.check_output(cmd)
		regs = output.split("\n")[-2:][0]
		for res in expected:
			res = res.strip()
			if regs.find(res) == -1:
				print "Test '" + test + "' failed"
				print res
				print regs
finally:
	os.chdir(cwd)
