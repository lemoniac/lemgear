#!/usr/bin/python

import pprint
import sys

from microinstr import MicroInstr
from parser import parse
from common import *
import VDP

#print "microengine"


(microcode, labels, rlabels) = parse("microcode/z80/microcode.mcr")

"""
for mi in microcode:
	print mi.toAscii()
"""
#sys.exit(0)

class SmsMemoryMapper:
	def __init__(self):
		self.slot = [0 for i in xrange(0xC000)]
		self.work_ram = [0 for i in xrange(8 * 1024)]
	
	def write(self, address, value):
		if address < 0xC000:
			self.slot[address] = value
		elif address < 0xE000:
			self.work_ram[address - 0xC000] = value
		elif address < 0x10000:
			self.work_ram[address - 0xE000] = value
		else:
			raise "bad address"

	def read(self, address):
		if address < 0xC000:
			return self.slot[address]
		elif address < 0xE000:
			return self.work_ram[address - 0xC000]
		elif address < 0x10000:
			return self.work_ram[address - 0xE000]
		
		raise "bad address"


class SmsIo:
	def __init__(self):
		self.vdp = VDP.VDP()

	def IN(self, port):
		if port == 0x7e: # V Counter , scanline
			return 0xb0
		elif port == 0x7f: # H Counter
			return 0
		elif port == 0xbe:
			return self.vdp.read_data()
		elif port == 0xbf:
			return self.vdp.read_control()
		elif port == 2:
			return self.port2
		print "INPORT", format(port, "02x"), "unsupported"
		return 0

	def OUT(self, port, value):
		if port == 0xbe: # VRAM data write
			self.vdp.write_data(value)
		elif port == 0xbf: # VDP control write
			self.vdp.write_control(value)
		elif port == 0x2:
			self.port2 = value
		elif port == 0x7f: # SN76489 PSG sound chip
			print "PSG sound chip", format(value, "02x")
		else:
			print "OUTPORT", format(port, "02x"), "unsupported"


rom = [ ord(a) for a in file(sys.argv[1], "rb").read() ]

memory = SmsMemoryMapper()
io = SmsIo()

rom_len = len(rom)

for i in xrange(rom_len):
	memory.write(i, rom[i])

def run(memory):
	global microcode
	flag_z = False
	flag_c = False # carry
	flag_s = False # sub

	# regs
	PC = 0 # program counter

	# microengine
	microPC = labels["FETCH"]

	while regs[PC] < rom_len and regs[INSTR] != 0x76:
		mi = microcode[microPC]
		print

		if microPC in rlabels:
			l = rlabels[microPC]
			print "##", l
		else:
			l = format(microPC, "04x")
		print "uPC:", l, "mem_pc:",format(memory.read(regs[PC]), "02X")
		print mi
		for i in xrange(len(regs)):
			print reg_names[i], ":", format(regs[i], "04X"), "   " ,
		print
		#for i in xrange(rom_len):
		#	print format(memory.read(i), "02X"),
		#print
		
		x = None
		if mi.alu_X != None:
			x = get_reg(mi.alu_X, mi.size_X)

		y = None
		if mi.alu_Y != None:
			y = get_reg(mi.alu_Y, mi.size_Y)

		result = None
		
		if not mi.alu and mi.alu_X != None and mi.out != None:
			if mi.size_out == Size.All:
				regs[mi.out] = x
			elif mi.size_out == Size.Low:
				regs[mi.out] = (regs[mi.out] & 0xff00) | (x & 0xff)
			elif mi.size_out == Size.High:
				regs[mi.out] = (regs[mi.out] & 0xff) | ((x & 0xff) << 8)

		if not mi.alu and mi.immediate != None and mi.out != None:
			if mi.size_out == Size.All:
				regs[mi.out] = mi.immediate
			elif mi.size_out == Size.Low:
				regs[mi.out] = (regs[mi.out] & 0xff00) | (mi.immediate & 0xff)
			elif mi.size_out == Size.High:
				regs[mi.out] = (regs[mi.out] & 0xff) | ((mi.immediate & 0xff) << 8)

		if mi.alu:
			if mi.immediate != None:
				y = mi.immediate
			
			if mi.alu_bits == 8:
				if y > 127:
					y -= 256

			result = 0
			if mi.alu == "inc":
				result = x + 1
				flag_s = False
			elif mi.alu == "dec":
				result = x - 1
				flag_s = True
			elif mi.alu == "add":
				result = x + y
				if mi.carry:
					result += 1
				flag_s = False
			elif mi.alu == "sub":
				result = x - y
				if mi.carry:
					result -= 1
				flag_s = True

			flag_z = result == 0
			
			if result > 0xffff:
				flag_c = True
				result &= 0xffff
			else:
				flag_c = False
			
			if mi.out != None:
				if mi.size_out == Size.All:
					regs[mi.out] = result
				elif mi.size_out == Size.Low:
					regs[mi.out] = (regs[mi.out] & 0xff00) | (result & 0xff)
				elif mi.size_out == Size.High:
					regs[mi.out] = (regs[mi.out] & 0xff) | ((result & 0xff) << 8)

		if mi.load:
			addr = regs[ADDR]
			if mi.immediate:
				addr += mi.immediate
			if mi.size_out == Size.All:
				regs[MBR] = memory.read(regs[ADDR])
			elif mi.size_out == Size.Low:
				regs[MBR] = (regs[MBR] & 0xff00) | memory.read(addr)
			elif mi.size_out == Size.High:
				regs[MBR] = (regs[MBR] & 0x00ff) | (memory.read(addr) << 8)

		if mi.store:
			addr = regs[ADDR]
			if mi.immediate:
				addr += mi.immediate

			if mi.size_out == Size.Low:
				memory.write(addr, regs[MBR] & 0xff)
			elif mi.size_out == Size.High:
				memory.write(addr, (regs[MBR] >> 8) & 0xff)

		if mi.io == "in":
			regs[MBR] = vdp.IN(regs[ADDR])
		if mi.io == "out":
			vdp.IN(regs[ADDR], regs[MBR])

			
		if mi.inc_pc:
			regs[PC] += 1

		cond = False
		if mi.jmp_cond == "Z" and flag_z:
			cond = True
		elif mi.jmp_cond == "NZ" and not flag_z:
			cond = True

		if mi.jmp_cond == "C" and flag_c:
			cond = True
		elif mi.jmp_cond == "NC" and not flag_c:
			cond = True

		if mi.jmp:
			if mi.jmp_cond == None or cond:
				microPC = mi.jmp
			else:
				microPC += 1
		elif mi.jmp_instr:
			if mi.jmp_cond == None or cond:
				if mi.jmp_rel:
					microPC += regs[INSTR] + 1
				else:
					microPC = regs[INSTR]
			else:
				microPC += 1
		else:
			microPC += 1 


run(memory)

for i in xrange(rom_len):
	print format(memory.read(i), "02X"),
print

