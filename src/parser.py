import re

from common import *
from microinstr import MicroInstr

def parse(filename):
	base_path = filename[:filename.rfind("/")+1]
	# read file, split in lines and remove empty lines
	microcode_ascii = [ line for line in [ line.strip() for line in file(filename).read().split('\n') ] if line != "" ]

	# pass: include files
	out = []
	for line in microcode_ascii:
		if line.startswith(".include"):
			filename = base_path + line.split()[1]
			included_file = [ line for line in [ line.strip() for line in file(filename).read().split('\n') ] if line != "" ]
			for l in included_file:
				out.append(l)
		else:
			out.append(line)
	microcode_ascii = out

	# pass: read macros
	macros = dict()
	for line in microcode_ascii:
		if line.startswith(".macro"):
			macro_name = line.split()[1]
			macro_lines = []
		elif line.startswith(".end"):
			macros[macro_name] = macro_lines
		elif line[0] == ".":
			macro_lines.append(line[1:])


	# remove macros	
	microcode_ascii = [ line for line in microcode_ascii if line[0] != "." ]

	# pass: macro expansion
	out = []
	for line in microcode_ascii:
		macro = line.split()
		if macro[0] in macros:
			n_args = len(macro) - 1
			for macro_line in macros[macro[0]]:
				for i in xrange(n_args):
					macro_line = macro_line.replace("$" + str(i), macro[i + 1])
				out.append(macro_line)
		else:
			out.append(line)
	microcode_ascii = out

	#pprint.pprint(microcode_ascii)

	# pass: address calculator
	microPC = 0
	labels = dict()
	rlabels = dict()
	for line in microcode_ascii:
		m = re.search(r"^\s*([\w\(\)]+):", line)
		if m:
			labels[m.group(1)] = microPC
			rlabels[microPC] = m.group(1)
		elif line != "":
			instr = line.split()
			if len(instr) == 0:
				continue
			microPC += 1


	#for a, l in rlabels.iteritems():
	#	print format(a, "04x"), l


	# pass: microcode generation
	microPC = 0
	microcode = []
	for line in microcode_ascii:
		m = re.search(r"^\s*([\w\(\)]+):", line)
		if m:
			#print m.group(1) + ":"
			labels[m.group(1)] = microPC
		elif line != "":
			instrs = line.split(",")
			if len(instrs) == 0:
				continue

			uop = MicroInstr()
			
			for i in instrs:
				instr = i.split()
			
				if instr[0] in alu_ops:
					uop.alu = instr[0]
					if len(instr) > 1 and instr[1] == "8":
						uop.alu_bits = 8
				elif instr[0] == "jmp":
					uop.jmp = labels[instr[1]]
				elif instr[0] == "jmp_instr":
					uop.jmp_instr = True
				elif instr[0] == "jmp_rel_instr":
					uop.jmp_instr = True
					uop.jmp_rel = True
				elif instr[0].startswith("jmp_"):
					uop.jmp = labels[instr[1]]
					uop.jmp_cond = instr[0][instr[0].find("_")+1:].upper()
				elif instr[0] == "load":
					uop.load = True
					uop.size_out = Size.All
					if len(instr) > 1:
						uop.immediate = int(instr[1])
				elif instr[0] == "load_hi":
					uop.load = True
					uop.size_out = Size.High
					if len(instr) > 1:
						uop.immediate = int(instr[1])
				elif instr[0] == "load_lo":
					uop.load = True
					uop.size_out = Size.Low
					if len(instr) > 1:
						uop.immediate = int(instr[1])
				elif instr[0] == "store_hi":
					uop.store = True
					uop.size_out = Size.High
					if len(instr) > 1:
						uop.immediate = int(instr[1])
				elif instr[0] == "store_lo":
					uop.store = True
					uop.size_out = Size.Low
					if len(instr) > 1:
						uop.immediate = int(instr[1])
				elif instr[0] == "inc_pc":
					uop.inc_pc = True
				elif len(instr) >= 3 and instr[1] == ">":
					reg_in = None
					size_in = Size.All
					from_Z = False
					try:
						uop.immediate = int(instr[0])
					except ValueError:
						if instr[0] == "Z":
							from_Z = True
						else:
							if instr[0] in reg_names:	
								in_r = instr[0]
							else:
								in_r = reg_map[instr[0]][0]
								size_in = reg_map[instr[0]][1]
							reg_in = reg_names.index(in_r)

					if instr[2] == "X":
						uop.alu_X = reg_in
						uop.size_X = size_in
					elif instr[2] == "Y":
						uop.alu_Y = reg_in
						uop.size_Y = size_in
					else:
						if instr[2] in reg_names:
							out_r = instr[2]
						else:
							out_r = reg_map[instr[2]][0]
							uop.size_out = reg_map[instr[2]][1]

						if not from_Z:
							uop.alu_X = reg_in
							uop.size_X = size_in
						uop.out = reg_names.index(out_r)
				elif instr[0] == "IN":
					uop.io = "in"
				elif instr[0] == "OUT":
					uop.io = "out"

			microcode.append( uop )

			#print format(microPC, "04x"), instr, microcode[microPC]

			microPC += 1

	return (microcode, labels, rlabels)

