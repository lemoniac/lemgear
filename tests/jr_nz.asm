	LD A, 10
l:
	DEC A
	CP 0
	JR NZ, l
	
	LD B, 2
	
	HALT
