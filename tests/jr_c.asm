	LD BC, $FFFF
	INC BC
	JR C, l
	
	LD E, 2
	
	HALT
	
l:
	LD E, 1
	
	HALT

