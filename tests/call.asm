ld SP, stack

call a

ld B, 5

halt

a:
	ld A, 10
	ret


	nop
	nop
	nop
	nop
	nop
	nop		
stack:

