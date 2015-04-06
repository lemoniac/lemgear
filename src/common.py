alu_ops = ["add", "sub", "inc", "dec", "and", "or", "xor", "shr", "shl"]

reg_names = ["PC", "INSTR", "ADDR", "MBR", "AF", "BC", "DE", "HL", "SP", "IX", "IY", "IR", "AFs", "BCs", "DEs", "HLs", "TMP"]

regs = [0 for i in xrange(len(reg_names))]

PC = 0
INSTR = 1
ADDR = 2
MBR = 3
AF = 4
BC = 5
DE = 6
HL = 7
SP = 8
IX = 9
IY = 10
IR = 11
AFs = 12
BCs = 13
DEs = 14
HLs = 15
TMP = 16

class Size:
	All = 1
	High = 2
	Low = 3

reg_map = {
	"A" : ("AF", Size.High),
	"F" : ("AF", Size.Low),
	"B" : ("BC", Size.High),
	"C" : ("BC", Size.Low),
	"D" : ("DE", Size.High),
	"E" : ("DE", Size.Low),
	"H" : ("HL", Size.High),
	"L" : ("HL", Size.Low),
	"I" : ("IR", Size.High),
	"R" : ("IR", Size.Low),
	}

def get_reg(r, size):
	global regs
	if size == Size.All:
		return regs[r]
	elif size == Size.Low:
		return regs[r] & 0xff
	elif size == Size.High:
		return regs[r] >> 8
