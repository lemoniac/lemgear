#!/usr/bin/python

import array
import pygame
import sys

import Z80
from Z80 import PC, A, B, C, D, E, H, L, AF, BC, DE, HL, SP
from Z80 import F_Z

def addr2str(address):
	return format(address, "04X") + "h"

def get_byte():
	global z80

	byte = z80.read(z80.regs.r[PC])
	z80.regs.r[PC]+= 1

	return byte


def get_sbyte():
	global z80

	byte = z80.read(z80.regs.r[PC])
	z80.regs.r[PC]+= 1

	if byte > 127:
		byte = -(256 - byte)

	return byte

class BasicBlock:
	inst = []

	def __init__(self):
		pass

basic_blocks = []
basic_block_dict = dict()

current_basic_block = BasicBlock()
basic_block_dict[0] = current_basic_block


z80 = Z80.Z80()

entries = set([0])
exits = set([])

disasm = []

def entries_add(start, orig):
	if start in entries:
		entries[start].append(orig)
	else:
		entries[start] = [orig]

def out_disasm(address, opcode, extra = None, extra2 = None):
	global disasm
	code = opcode
	if extra:
		code += str(extra)
	if extra2:
		code += " " + str(extra2)
	disasm.append((address, code))


last_opcode = ""

def store_opcode(address, opcode, extra = None, extra2 = None):
	code = opcode
	if extra != None:
		code += str(extra)
	if extra2 != None:
		code += " " + str(extra2)
	global last_opcode
	last_opcode = format(address, "04x") + ": " +  code

def cmd_print(s):
	global cmd_history
	cmd_history.append(str(s))

def inst_print(s):
	global inst_history
	inst_history.append(str(s))
	if len(inst_history) > 100:
		inst_history.pop(0)

def print_opcode(address, opcode, extra = None, extra2 = None):
	store_opcode(address, opcode, extra, extra2)
	cmd_print( last_opcode )
	global z80
	cmd_print(z80.regs)


out = store_opcode


def step():
	global z80
	def read_address():
		global i
		global z80
		address = z80.read(z80.regs.r[PC]) | (z80.read(z80.regs.r[PC]+1)<<8)
		z80.regs.r[PC] += 2
		return address
	z80.interrupt = False
	start = z80.regs.r[PC]
	
	byte = get_byte()
	if byte == 0xf3:
		out(start, "DI")
		z80.di()
	elif byte == 0:
		out(start, "NOP")
	elif byte == 1:
		address = read_address()
		out(start, "LD BC, ", addr2str(address))
		z80.ld_r16_i(BC, address)
	elif byte == 4:
		out(start, "INC B")
		z80.inc8(B)
	elif byte == 0x06:
		value = get_byte()
		out(start, "LD B, ", value)
		z80.ld8_reg_i(B, value)
	elif byte == 0x08:
		z80.ex_r(AF)
	elif byte == 0x0b:
		out(start,  "DEC BC")
		z80.dec16(BC)
	elif byte == 0x0c:
		out(start, "INC C")
		z80.inc8(C)
	elif byte == 0x0d:
		out(start, "DEC C")
		z80.dec8(C)
	elif byte == 0x0e:
		value = get_byte()
		out(start, "LD C,", value)
		z80.ld8_reg_i(C, value)
	elif byte == 0x10:
		value = get_sbyte()
		address = z80.regs.r[PC] + value
		out(start, "DJNZ ", value, addr2str(address))
		entries.add(address)
		entries.add(z80.regs.r[PC])
		exits.add(start)
		z80.djnz(address)
	elif byte == 0x11:
		address = read_address()
		out(start, "LD DE, " + addr2str(address))
		z80.ld_r16_i(DE, address)
	elif byte == 0x13:
		out(start, "INC DE")
		z80.inc16(DE)
	elif byte == 0x16:
		value = get_byte()
		out(start, "LD D, ", value)
	elif byte == 0x18:
		value = get_sbyte()
		address = z80.regs.r[PC] + value
		out(start, "JR ", value,addr2str(address))
		entries.add(address)
		exits.add(start)
		z80.jp(address)
	elif byte == 0x1a:
		out(start, "LD A, (DE)")
		z80.ld8_r_rm(A, DE)
	elif byte == 0x1b:
		out(start, "DEC DE")
		z80.dec16(DE)
	elif byte == 0x1d:
		out(start, "DEC E")
		z80.dec8(E)
	elif byte == 0x1f:
		out(start, "RRA")
	elif byte == 0x20:
		value = get_sbyte()
		address = z80.regs.r[PC] + value
		out(start, "JR NZ,", value)
		entries.add(address)
		entries.add(z80.regs.r[PC])
		exits.add(start)
		z80.jnz(address)
	elif byte == 0x21:
		address = read_address()
		out(start, "LD HL, " + addr2str(address))
		z80.ld_r16_i(HL, address)
	elif byte == 0x22:
		address = read_address()
		out(start, "LD (" + addr2str(address)+"), HL")
		z80.ld_mi_r16(address, HL)
	elif byte == 0x23:
		out(start, "INC HL")
		z80.inc16(HL)
	elif byte == 0x28:
		value = get_sbyte()
		out(start, "JR Z, ", value)
		entries.add(z80.regs.r[PC] + value)
		entries.add(z80.regs.r[PC])
		exits.add(start)
	elif byte == 0x2b:
		out(start, "DEC HL")
		z80.dec16(HL)
	elif byte == 0x2c:
		out(start, "INC L")
		z80.inc8(L)
	elif byte == 0x2e:
		value = get_byte()
		out(start, "LD L, ", value)
		z80.ld8_reg_i(L, value)
	elif byte == 0x31:
		address = read_address()
		out(start, "LD SP, ", addr2str(address))
		z80.ld_r16_i(SP, address)
	elif byte == 0x32:
		address = read_address()
		out(start, "LD ("+addr2str(address)+"), A")
	elif byte == 0x35:
		z80.dec8_rad(HL)
		out(start, "DEC (HL)")
	elif byte == 0x36:
		value = get_byte()
		out(start, "LD (HL), ", value)
	elif byte == 0x38:
		value = get_sbyte()
		out(start, "JR C, ", value)
	elif byte == 0x3a:
		address = read_address()
		out(start, "LD A, ("+addr2str(address)+")")
		z80.ld8_r_m(A, address)
	elif byte == 0x3c:
		out(start, "INC A")
		z80.inc8(A)
	elif byte == 0x3d:
		out(start, "DEC A")
		z80.dec8(A)
	elif byte == 0x3e:
		value = get_byte()
		out(start, "LD A, ", value)
		z80.ld8_reg_i(A, value)
	elif byte == 0x40:
		out(start, "LD B, B")
		z80.ld8_reg_reg(B, B)
	elif byte == 0x41:
		out(start, "LD B, C")
		z80.ld8_reg_reg(B, C)
	elif byte == 0x42:
		out(start, "LD B, D")
		z80.ld8_reg_reg(B, D)
	elif byte == 0x43:
		out(start, "LD B, E")
		z80.ld8_reg_reg(B, E)
	elif byte == 0x46:
		out(start, "LD B, (HL)")
		#z80.ld8_reg_reg(C, A)
	elif byte == 0x47:
		out(start, "LD B, A")
		z80.ld8_reg_reg(B, A)
	elif byte == 0x4e:
		out(start, "LD C, (HL)")
		#z80.ld8_reg_reg(C, A)
	elif byte == 0x4f:
		out(start, "LD C, A")
		z80.ld8_reg_reg(C, A)
	elif byte == 0x54:
		out(start, "LD D, H")
		z80.ld8_reg_reg(D, H)
	elif byte == 0x5f:
		out(start, "LD E, A")
		z80.ld8_reg_reg(E, A)
	elif byte == 0x62:
		out(start, "LD H, D")
		z80.ld8_reg_reg(H, D)
	elif byte == 0x67:
		out(start, "LD H, A")
		z80.ld8_reg_reg(H, A)
	elif byte == 0x6B:
		out(start, "LD L, E")
		z80.ld8_reg_reg(L, E)
	elif byte == 0x75:
		out(start, "LD (HL), L")
		z80.ld_mr_r8(HL, L)
	elif byte == 0x76:
		out(start, "HALT")
	elif byte == 0x77:
		out(start, "LD (HL), A")
		z80.ld_mr_r8(HL, A)
	elif byte == 0x78:
		out(start, "LD A, B")
		z80.ld8_reg_reg(A, B)
	elif byte == 0x79:
		out(start, "LD A, C")
		z80.ld8_reg_reg(A, C)
	elif byte == 0x7a:
		out(start, "LD A, D")
		z80.ld8_reg_reg(A, D)
	elif byte == 0x7b:
		out(start, "LD A, E")
		z80.ld8_reg_reg(A, E)
	elif byte == 0x7c:
		out(start, "LD A, H")
		z80.ld8_reg_reg(A, H)
	elif byte == 0x7d:
		out(start, "LD A, L")
		z80.ld8_reg_reg(A, L)
	elif byte == 0x7e:
		out(start, "LD A, (HL)")
		z80.ld8_r_rm(A, HL)
	elif byte == 0x87:
		out(start, "ADD A, A")
		z80.add8_r_r(A, A)
	elif byte == 0x90:
		out(start, "SUB B")
	elif byte == 0xaf:
		out(start, "XOR A")
		z80.xor_r(A)
	elif byte == 0xb0:
		out(start, "OR B")
		z80.or_r(B)
	elif byte == 0xb1:
		out(start, "OR C")
		z80.or_r(C)
	elif byte == 0xb4:
		out(start, "OR H")
		z80.or_r(H)
	elif byte == 0xb5:
		out(start, "OR L")
		z80.or_r(L)
	elif byte == 0xb3:
		out(start, "OR E")
		z80.or_r(E)
	elif byte == 0xb7:
		out(start, "OR A")
		z80.or_r(A)
	elif byte == 0xbc:
		out(start, "CP H")
	elif byte == 0xbe:
		out(start, "CP (HL)")
	elif byte == 0xc0:
		out(start, "RETNZ")
		entries.add(z80.regs.r[PC])
		exits.add(start)
		z80.ret_flag(F_Z, False)
	elif byte == 0xc1:
		out(start, "POP BC")
		z80.pop(BC)
	elif byte == 0xc2:
		address = read_address()
		out(start, "JP NZ,", addr2str(address))
		entries.add(address)
		exits.add(start)
	elif byte == 0xc3:
		address = read_address()
		out(start, "JP ", addr2str(address))
		entries.add(address)
		exits.add(start)
		z80.jp(address)
	elif byte == 0xc5:
		out(start, "PUSH BC")
		z80.push(BC)
	elif byte == 0xc6:
		value = get_byte()
		out(start, "ADD A, ", value)
		z80.add8_r_i(A, value)
	elif byte == 0xc7:
		out(start, "RST 0")
		z80.interrupt = True
	elif byte == 0xc8:
		out(start, "RETZ")
		exits.add(start)
		entries.add(z80.regs.r[PC])
		z80.ret_flag(F_Z, True)
	elif byte == 0xc9:
		exits.add(start)
		out(start, "RET")
		z80.ret()
	elif byte == 0xcb:
		value = get_byte()
		out(start, "RES ", value)
		z80.res(A, (value >> 3) & 7)
	elif byte == 0xcd:
		address = read_address()
		out(start, "CALL ", addr2str(address))
		entries.add(z80.regs.r[PC])
		exits.add(start)
		z80.call(address)
	elif byte == 0xd1:
		out(start, "POP DE")
		z80.pop(DE)
	elif byte == 0xd3:
		value = get_byte()
		out(start, "OUTA ", format(value, "02x"))
		z80.outa(value)
	elif byte == 0xd5:
		out(start, "PUSH DE")
		z80.push(DE)
	elif byte == 0xd7:
		out(start, "RST 10h")
		z80.call(0x10)
	elif byte == 0xd9:
		out(start, "EXX")
	elif byte == 0xdb:
		value = get_byte()
		out(start, "INA ", format(value, "02x"))
		z80.ina(value)
	elif byte == 0xe7:
		out(start, "RST 20h")
		z80.call(0x20)
	elif byte == 0xef:
		out(start, "RST 28h")
		z80.call(0x28)
	elif byte == 0xed:
		byte2 = get_byte()
		if byte2 == 0x44:
			out(start, "NEG")
		elif byte2 == 0x45:
			out(start, "RETN")
			exits.add(start)
			z80.ret()
		elif byte2 == 0x47:
			out(start, "LD I, A")
		elif byte == 0x4d:
			out(start, "RETI")
			exits.add(start)
			z80.ret()
		elif byte2 == 0x51:
			out(start, "OUT (C), D")
		elif byte2 == 0x56:
			out(start, "IM 1")
		elif byte2 == 0x79:
			out(start, "OUT (C), A")
		elif byte2 == 0xa3:
			out(start, "OUTI")
			z80.outi()
		elif byte2 == 0xb0:
			out(start, "LDIR")
			z80.ldir()
		elif byte2 == 0xb3:
			out(start, "OTIR")
			z80.otir()
		else:
			print format(byte, "02x"), format(byte2, "02x"), "unsupported"
			z80.interrupt = True
	elif byte == 0xf1:
		out(start, "POP AF")
		z80.pop(AF)
	elif byte == 0xf2:
		address = read_address()
		out(start, "JP P, ", addr2str(address))
		entries.add(address)
		exits.add(start)
	elif byte == 0xf5:
		out(start, "PUSH AF")
		z80.push(AF)
	elif byte == 0xf6:
		value = get_byte()
		out(start, "OR", value)
	elif byte == 0xfa:
		address = read_address()
		out(start, "JP M ", addr2str(address))
		entries.add(address)
		exits.add(start)
	elif byte == 0xfb:
		out(start, "EI")
		z80.ei()
	elif byte == 0xfd:
		byte2 = get_byte()
		if byte2 == 0x21:
			value = read_address()
			out(start, "LD IY, ", value)
		else:
			print format(byte, "02x"), format(byte2, "02x"), "unsupported"
			z80.interrupt = True
	elif byte == 0xfe:
		value = get_byte()
		out(start, "CP ", value)
		z80.cp_i8(value)
	else:
		out(start, format(byte, "02x"), "unsupported" )
		z80.interrupt = True


last_command = ""
command = ""

breakpoints = set([])

pygame.init()

screen = pygame.display.set_mode( (640, 480) )

font = pygame.font.SysFont("freemono", 16)

def printable(c):
	return (c >= ord('a') and c <= ord('z')) or c == ord(' ') or (c >= ord('0') and c <= ord('9'))


command = ""
tmp_command = ""
command_surface = font.render("(db) " + tmp_command, True, (255, 0, 0) )

cmd_history = ["LemGear Interactive Debugger", "(db) "]
inst_history = []

def execute_command(c):
	global last_command
	global inst_history
	global command
	global z80
	last_command = command

	if c != "":
		command = c

	if command == "st":
		z80.vdp.print_state()
	elif command == "s":
		step()
		inst_print(last_opcode)
	elif command[0] == 's':
		s = command.split()
		for i in xrange(int(s[1])):
			step()
			if z80.interrupt or z80.regs.r[PC] in breakpoints:
				break
		inst_print(last_opcode)
	elif command == "r":
		try:
			if z80.regs.r[PC] in breakpoints:
				step()
			while not z80.interrupt and z80.regs.r[PC] not in breakpoints:
				step()
		except:
			print "EXCEPTION"
		inst_print(last_opcode)
	elif command == "q":
		return True
	elif command[0] == "b":
		b = command.split()
		breakpoints.add(int(b[1], 16))
	elif command[0] == "d":
		b = command.split()
		breakpoints.discard(int(b[1], 16))
	elif command == "m":
		cmd_print(z80.dump_mem())
	elif command[0] == "m":
		s = command.split()
		cmd_print(z80.dump_mem(int(s[1], 16), 16))
	elif command == "rst":
		z80 = Z80.Z80()
		inst_history = []
	elif command == "c":
		print z80.cycles
	elif command == "regs":
		print "VDP: " + z80.vdp.regs()
	elif command == "pal":
		print z80.vdp.palette()
	elif command == "v":
		z80.vdp.dump_mem()
	elif command[0] == "v":
		s = command.split()
		z80.vdp.dump_mem(int(s[1], 16), 16)
	elif command == "list":
		print "list"
	
	return False


def draw_register_panel():
	global screen
	global font
	global z80

	y = 20	
	regs = str(z80.regs).split("\n")
	for reg in regs:
		reg_surface = font.render(reg, True, (255, 0, 0) )
		screen.blit(reg_surface, (640 - 220, y) )
		y += 16

	y = 20

	regs = str(z80.vdp.regs()).split("\n")
	for reg in regs:
		reg_surface = font.render(reg, True, (255, 0, 0) )
		screen.blit(reg_surface, (640 - 100, y) )
		y += 16
	

def draw_inst_panel():
	global screen
	global font
	global inst_history

	l = len(inst_history)
	lines = min(24, l)

	y = 5
	for i in range(l - lines, l):
		command_surface = font.render(inst_history[i], True, (255, 0, 0) )
		screen.blit(command_surface, (5, y) )
		y += 16


quit = False
tmp_command = ""
while z80.regs.r[PC] < 0xffff and not quit:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if printable(event.key):
				tmp_command += chr(event.key)
				cmd_history[-1] = "(db) " + tmp_command
			elif event.key == 8: # backspace
				tmp_command = tmp_command[:-1]
				cmd_history[-1] = "(db) " + tmp_command
			elif event.key == 13 or event.key == 271:
				quit = execute_command(tmp_command)
				cmd_history.append("(db) ")
				tmp_command = ""
			else:
				print event.key
			

	screen.fill( (0, 0, 0) )

	lines = min(5, len(cmd_history))

	for i in range(lines):
		command_surface = font.render(cmd_history[len(cmd_history)-i-1], True, (0, 255, 0) )
		screen.blit(command_surface, (0, 464 - i * 16) )

	pygame.draw.line(screen, (255, 0, 0), (0, 395), (640, 395) )

	pygame.draw.rect(screen, (0, 0, 32), ((635 - 256, 390 - 192), (256, 192)) )

	draw_register_panel()
	draw_inst_panel()

	pygame.display.flip()


for line in disasm:
	if line[0] in entries:
		print "-- START BLOCK --"
	print format(line[0], "08x")+":", line[1]
	if line[0] in exits:
		print "-- END BLOCK --"
"""
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
"""
