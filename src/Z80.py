import array
import sys

import VDP

AF = 0
BC = 1
DE = 2
HL = 3
IX = 4
IY = 5
SP = 6
I  = 7
R  = 8
PC = 9

A = 0
F = 1
B = 2
C = 3
D = 4
E = 5
H = 6
L = 7

F_S = 1 << 7
F_Z = 1 << 6
F_h = 1 << 4
F_p = 1 << 2
F_s = 1 << 1
F_c = 1

def addr2str(address):
	return format(address, "04X") + "h"


class Z80:
	class Registers:
		def __init__(self):
			self.r = array.array("H", [0] * 10)
			self.sr = array.array("H", [0] * 10)
		
			self.names = ["AF", "BC", "DE", "HL", "IX", "IY", "SP", " I", " R", "PC"] 

		def __str__(self):
			s = ""
			for i in xrange(len(self.names)):
				s+=  self.names[i] + ": " + format(self.r[i], "04x") + "h\n"

			return s

	class Disassemble:
		def DI(start):
			print ""

	def __init__(self):
		self.regs = Z80.Registers()
		self.rom = array.array('B', open(sys.argv[1], "rb").read())
		self.cycles = 0
		self.mem = array.array('B', [0] * 8 * 1024)
		self.vdp = VDP.VDP()
		self.interrupt = False
		self.interrupt_mode = 0

	def read(self, address):
		if address >= 0xe000:
			return self.mem[address - 0xe000]
		if address >= 0xc000:
			return self.mem[address - 0xc000]
		return self.rom[address]

	def write(self, address, byte):
		if address >= 0xe000:
			self.mem[address - 0xe000] = byte
		elif address >= 0xc000:
			self.mem[address - 0xc000] = byte
		else:
			raise RuntimeError("read ONLY memory " + addr2str(address))

	def dump_mem(self, start = 0xc800, size = 8 * 1024):
		s = ""
		for i in xrange(start, start + size):
			if i > 0xffff:
				break
			if i % 16 == 0:
				s +=  "\n" + addr2str(i) + ": "
			s+= format(self.read(i), "02x") + " "
		return s

	def get_z(self):
		f = self.get_r8(F)
		return (f & F_Z) == F_Z 

	def set_flag(self, f, v):
		if v:
			self.regs.r[AF] |= f
		else:
			self.regs.r[AF] &= ~f  | 0xff00

	def get_r8(self, r):
		s = r / 2
		t = r % 2

		if t == 1:
			return self.regs.r[s] & 0xff
		return self.regs.r[s] >> 8

	def add8_r_i(self, r, value):
		v = self.get_r8(r)
		v += value
		if v > 255:
			self.set_flag(F_c, True)
			v -= 256
			
		if v == 0:
			self.set_flag(F_Z, True)
			
		self.set_flag(F_s, False)
		
	def add8_r_r(self, r, s):
		value = self.get_r8(s)
		self.add8_r_i(r, value)

	def ld8_reg_i(self, r, value):
		s = r / 2
		t = r % 2

		if t == 1:
			self.regs.r[s] = (self.regs.r[s] & 0xff00) | value
		else:
			self.regs.r[s] = (self.regs.r[s] & 0xff) | (value << 8)
		self.cycles += 7

	def ld8_r_m(self, r, address):
		self.ld8_reg_i(r, self.read(address))

	def ld8_r_rm(self, r, rs):
		value = self.read(self.regs.r[rs])
		self.ld8_reg_i(r, value)

	def ld_r16_i(self, r, n):
		self.regs.r[r] = n
		self.cycles += 10

	def ld8_reg_reg(self, r, s):
		self.ld8_reg_i(r, self.get_r8(s))
		self.cycles += 4

	def ld_mi_r16(self, address, r):
		self.write(address, self.regs.r[r] & 0xff)
		self.write(address + 1, self.regs.r[r] >> 8)

	def ld_mr_r8(self, r, s):
		v = self.get_r8(s)
		self.write(self.regs.r[r], v)

	def in_(self, port):
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

	def ina(self, n):
		self.ld8_reg_i(A, self.in_(n))

	def out(self, port, value):
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

	def outa(self, n):
		self.out(n, self.get_r8(A))

	def otir(self):
		while self.get_r8(B) != 0:
			self.outi()

	def outi(self):
		self.out(self.get_r8(C), self.read(self.regs.r[HL]))	
		self.inc16(HL)
		self.dec8(B)

	def inc8(self, r):
		v = self.get_r8(r)
		v += 1
		self.ld8_reg_i(r, v)

	def inc16(self, r):
		self.regs.r[r] += 1
		#self.cycles += 6

	def call(self, address):
		self.push(PC)
		self.regs.r[PC] = address

	def cp_i8(self, value):
		if self.get_r8(A) == value:
			self.set_flag(F_Z, 1)
		else:
			self.set_flag(F_Z, 0)

	def cp_r8(self, r):
		self.cp_i8(self.get_r8(r))

	def di(self):
		self.interrupt = False

	def ei(self):
		self.interrupt = True

	def im(self, mode):
		self.interrupt_mode = mode

	def dec8(self, r):
		v = self.get_r8(r)
		z = 0
		if v == 0:
			v = 0xff
		else:
			v-= 1
			if v == 0:
				z = 1
		self.set_flag(F_Z, z)
		self.ld8_reg_i(r, v)
		self.set_flag(F_s, 1)

	def dec16(self, r):
		if self.regs.r[r] > 0:
			self.regs.r[r] -= 1
		else:
			self.regs.r[r] = 0xffff
		#self.cycles += 6

	def dec8_rad(self, rad):
		"""decreases the value hold in the address pointed by a register"""
		addr = self.regs.r[rad]
		v = self.read(addr)
		z = 0
		if v == 0:
			v = 0xff
		else:
			v -= 1
			if v == 0:
				z = 1
				
		self.set_flag(F_Z, z)
		self.write(addr, v)

	def djnz(self, address):
		self.dec8(B)
		if not self.get_z():
			self.regs.r[PC] = address
			self.cycles += 13
		else:
			self.cycles += 8

	def jp(self, address):
		self.regs.r[PC] = address
		self.cycles += 10

	def jnz(self, address):
		if not self.get_z():
			self.regs.r[PC] = address
	
	def ldi(self):
		self.write(self.regs.r[DE], self.read(self.regs.r[HL]))
		self.inc16(HL)
		self.dec16(BC)
		self.inc16(DE)
		
		#self.cycles += 16

	def ldir(self):
		while self.regs.r[BC] != 0:
			self.ldi()

	def pop(self, r):
		self.regs.r[SP] += 2
		self.regs.r[r] = self.read(self.regs.r[SP]) | (self.read(self.regs.r[SP] + 1) << 8)
 
	def push(self, r):
		self.write(self.regs.r[SP], self.regs.r[r] & 0xff)
		self.write(self.regs.r[SP] + 1, self.regs.r[r] >> 8)
		self.regs.r[SP] -= 2

	def res(self, r, bit):
		value = self.get_r8(r) & (~(1 << bit))
		self.ld8_reg_i(r, value)

	def ret(self):
		self.pop(PC)

	def ret_flag(self, flag, value):
		if flag == F_Z and self.get_z() == value:
			self.ret()

	def or_r(self, r):
		a = self.get_r8(A)
		rhs = self.get_r8(r)
		res = a | rhs
		self.ld8_reg_i(A, res)
		self.set_flag(F_s, 0)
		self.set_flag(F_c, 0)
		self.set_flag(F_Z, 1 if res == 0 else 0)

	def xor_r(self, r):
		if r == A:
			self.ld8_reg_i(A, 0)

	def ex_r(self, r):
		tmp = self.regs.r[r]
		self.regs.r[r] = self.regs.sr[r]
		self.regs.sr[r] = tmp

	def exx(self):
		self.ex_r(BC)
		self.ex_r(DE)
		self.ex_r(HL)

