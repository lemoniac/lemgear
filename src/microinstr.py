from common import *

class MicroInstr:
	def __init__(self, jmp = None, jmp_instr = False, jmp_rel = False, alu = None, load = False, store = False, 
			alu_X = None, alu_Y = None, out = None, inc_pc = False, size_X = Size.All, size_Y = Size.All, size_out = Size.All, jmp_cond = None,
			alu_bits = 16, immediate = None, carry = False, io = None):
		self.jmp = jmp
		self.jmp_instr = jmp_instr
		self.jmp_rel = jmp_rel
		self.jmp_cond = jmp_cond
		self.alu = alu
		self.load = load
		self.store = store
		self.alu_X = alu_X
		self.alu_Y = alu_Y
		self.out = out
		self.inc_pc = inc_pc
		self.size_X = size_X
		self.size_Y = size_Y
		self.size_out = size_out
		self.alu_bits = alu_bits
		self.immediate = immediate
		self.carry = carry
		self.io = io

	def __repr__(self):
		return "jmp:" + repr(self.jmp) + " jmp_instr:" + repr(self.jmp_instr) + " " + str(self.jmp_cond) + \
			" alu:" + repr(self.alu) + " load:" + repr(self.load) + " store:" + repr(self.store) + \
			" X:" + repr(self.alu_X) + " Y:" + repr(self.alu_Y) + " out:" + repr(self.out) + " inc_pc:" + repr(self.inc_pc) + \
			" immediate: " + repr(self.immediate)


	def toAscii(self):
		def n(value):
			return str(value) + "\t" if value != None  else  "-\t"

		def b(value):
			return "1\t" if value else  "0\t"

		def i(value):
			return str(value) + "\t"
	
		ascii = ""
		
		ascii += n(self.jmp)
		ascii += b(self.jmp_instr)
		ascii += b(self.jmp_rel)
		ascii += n(self.jmp_cond)
		ascii += n(self.alu)
		ascii += i(self.alu_bits)
		ascii += b(self.carry)
		ascii += n(self.immediate)
		ascii += b(self.load)
		ascii += b(self.store)
		ascii += n(self.alu_X)
		ascii += n(self.alu_Y)
		ascii += n(self.out)
		ascii += b(self.inc_pc)
		ascii += n(self.size_X)
		ascii += n(self.size_Y)
		ascii += n(self.size_out)
		ascii += n(self.io)

		return ascii

