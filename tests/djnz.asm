	ld B, 10
	ld A, 0
	ld C, 1
l:
	add C
	djnz l

	halt
	
	ld A, 20
