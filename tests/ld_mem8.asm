ld BC, heap
ld A, $ce
ld (BC), A
ld A, 0
ld A, (heap)
ld D, A

ld A, $ec
ld (heap), A
ld A, 0
ld A, (BC)
ld E, A

ld HL, heap
ld (HL), $aa
ld A, (heap)

halt

	nop
	nop
heap:
	nop
	nop

