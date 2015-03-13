	ld A, 5
	ex AF, AF'
	cp 0
	jr z, l
	halt
l:
	ld A, 10
	ld B, 3
	ex AF, AF'
	
	ld DE, $1234
	ld HL, $5678
	ex DE, HL

	halt
	
	
	

