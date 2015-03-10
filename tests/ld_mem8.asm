ld BC, heap
ld A, $ce
ld (BC), A
ld A, 0
ld A, (heap)
ld H, A

ld A, $ec
ld (heap), A
ld A, 0
ld A, (BC)
ld L, A

halt

	nop
	nop
heap:
	nop
	nop

