LD HL, src
LD DE, dst
LD BC, 4
LDIR

HALT

src:
	DI
	EI
	EI
	DI
	XOR A
	
dst:
	NOP
	NOP
	NOP
	NOP
	NOP
