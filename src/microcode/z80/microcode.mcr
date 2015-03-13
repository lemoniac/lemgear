.include macros.mcr
.include opcode_table.mcr

FETCH:
	PC > ADDR , load
	MBR > INSTR , jmp_instr

NOP: # 00
	inc+fetch
	
LD_BC_nn: ## 01 n n
	LD_R16_nn BC

LD_(BC)_A: # 02
	BC > ADDR
	A > MBR
	store_lo , inc+fetch

INC_BC: # 03
	INC BC

INC_B: # 04
	INC B

DEC_B: # 05
	DEC B

LD_B_n: # 06
	LD_R_n B

EX_AF_AFs: # 08
	SWAP AF AFs
	inc+fetch

DEC_BC: # 0B
	DEC BC

INC_C: # 0C
	INC C

DEC_C: # 0D
	DEC C

LD_C_n: # 0E
	LD_R_n C

DJNZ: # 10
	inc_pc , B > X , dec , Z > B , jmp_z DJNZ_0

	PC > ADDR , load
	PC > X , MBR > Y , add 8 , Z > PC

	inc+fetch

DJNZ_0:
	inc+fetch

LD_DE_nn: # 11 n n
	LD_R16_nn DE

LD_(DE)_A: # 12
	DE > ADDR
	A > MBR
	store_lo , inc+fetch

INC_DE: # 13
	INC DE

INC_D: # 14
	INC D

DEC_D: # 15
	DEC D

LD_D_n: # 16
	LD_R_n D

DEC_DE: # 1B
	DEC DE

INC_E: # 1C
	INC E

DEC_E: # 1D
	DEC E

LD_E_n: # 1E
	LD_R_n E

JR_NZ_e: # 20
	inc_pc , jmp_z JR_NZ_e_no_jmp

	PC > ADDR , load

	PC > X , MBR > Y , add 8 , Z > PC

	inc+fetch

JR_NZ_e_no_jmp:
	inc+fetch

LD_HL_nn: # 21
	LD_R16_nn HL

LD_(nn)_HL: # 22
	inc_pc
	PC > ADDR , load_lo
	inc_pc
	PC > ADDR , load_hi

	MBR > ADDR
	HL > MBR
	store_lo
	store_hi 1 , inc+fetch

INC_HL: # 23
	INC HL

INC_H: # 24
	INC H

DEC_H: # 25
	DEC H

LD_H_n: # 26
	LD_R_n H

JR_Z_e: # 28
	inc_pc , jmp_nz JR_Z_e_no_jmp

	PC > ADDR , load

	PC > X , MBR > Y , add 8 , Z > PC

	inc+fetch

JR_Z_e_no_jmp:
	inc+fetch

DEC_HL: # 2B
	DEC HL

INC_L: # 2C
	INC L

DEC_L: # 2D
	DEC L

LD_L_n: # 2E
	LD_R_n L

JR_NC_e: # 30
	inc_pc , jmp_c JR_NC_e_no_jmp

	PC > ADDR , load

	PC > X , MBR > Y , add 8 , Z > PC

	inc+fetch

JR_NC_e_no_jmp:
	inc+fetch

LD_SP_nn: # 31
	LD_R16_nn SP

LD_(nn)_A: # 32
	inc_pc
	PC > ADDR
	load_lo
	inc_pc
	PC > ADDR
	load_hi
	MBR > ADDR

	A > MBR
	store_lo , inc+fetch

JR_C_e: # 38
	inc_pc , jmp_nc JR_C_e_no_jmp

	PC > ADDR , load

	PC > X , MBR > Y , add 8 , Z > PC

	inc+fetch

JR_C_e_no_jmp:
	inc+fetch

LD_A_(nn): # 3A
	inc_pc
	PC > ADDR
	load_lo
	inc_pc
	PC > ADDR
	load_hi
	MBR > ADDR
	load

	MBR > A , inc+fetch

INC_SP: # 3e
	INC SP

DEC_SP: # 3B
	DEC SP

INC_A: # 3C
	INC A

DEC_A: # 3D
	DEC A

LD_A_n: # 3E
	LD_R_n A

LD_R_R B # 40

LD_R_R C # 48

LD_R_R D # 50

LD_R_R E # 58

LD_R_R H # 60

LD_R_R L # 68

LD_(HL)_B: # 70
	B > MBR , jmp LD_(HL)_r

LD_(HL)_C: # 71
	C > MBR , jmp LD_(HL)_r

LD_(HL)_D: # 72
	D > MBR , jmp LD_(HL)_r

LD_(HL)_E: # 73
	E > MBR , jmp LD_(HL)_r

LD_(HL)_H: # 74
	H > MBR , jmp LD_(HL)_r

LD_(HL)_L: # 75
	L > MBR , jmp LD_(HL)_r

HALT: # 76
	jmp HALT

LD_(HL)_A: # 77
	A > MBR , jmp LD_(HL)_r

LD_(HL)_r:
	HL > ADDR , store_lo , inc+fetch

LD_R_R A # 78

ALU_OP ADD add # 80-87

ALU_OP SUB sub # 90-97

ALU_OP AND and # A0-A7

ALU_OP XOR xor # A8-AF

ALU_OP OR or # B0-B7

POP_BC: # C1
	POP_R BC
	inc+fetch

JP: # C3
	inc_pc
	PC > ADDR
	load_lo
	inc_pc
	PC > ADDR
	load_hi
	MBR > PC , jmp FETCH

PUSH_BC: # C5
	PUSH_R BC
	inc+fetch

RET: # C9
	POP_R PC
	jmp FETCH

CALL: # CD
	inc_pc
	PC > ADDR
	load_lo , inc_pc
	PC > ADDR
	load_hi , inc_pc
	MBR > INSTR  # !!!
	PUSH_R PC
	INSTR > PC # !!!
	jmp FETCH

POP_DE: # D1
	POP_R DE
	inc+fetch

OUTA: # D3
	inc_pc
	load
	MBR > ADDR
	A > MBR
	out

	inc+fetch

PUSH_DE: # D5
	PUSH_R DE
	inc+fetch

EXX: # D9
	SWAP BC BCs
	SWAP DE DEs
	SWAP HL HLs
	inc+fetch

INA: # DB
	inc_pc
	load
	MBR > ADDR
	in
	MBR > A
	
	inc+fetch

POP_HL: # E1
	POP_R HL
	inc+fetch

PUSH_HL: # E5
	PUSH_R HL
	inc+fetch

EX_DE_HL: # EB
	SWAP DE HL
	inc+fetch

prefix_ED:
	inc_pc
	
	PC > ADDR
	load
	MBR > INSTR
	jmp_rel_instr

	.include ed_prefix.mcr
	
	jmp FETCH

LDIR: # ED B0
	HL > ADDR
	load
	DE > ADDR
	store_lo

	DE > X , inc , Z > DE

	HL > X , inc , Z > HL

	BC > X , dec , Z > BC

	jmp_nz LDIR

	inc+fetch

OTIR: # ED B3
	HL > ADDR
	load
	C > ADDR
	out

	HL > X , inc , Z > HL

	BC > X , dec , Z > BC

	jmp_nz OTIR

	inc+fetch

POP_AF: # F1
	POP_R AF
	inc+fetch

DI: # F3
	inc+fetch

PUSH_AF: # F5
	PUSH_R AF
	inc+fetch

EI: # FB
	inc+fetch

CP_n: # FE
	inc_pc
	PC > ADDR
	load
	A > X , MBR > Y , sub

	inc+fetch

