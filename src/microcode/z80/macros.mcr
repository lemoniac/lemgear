.macro inc+fetch
.	inc_pc , jmp FETCH
.end

.macro DEC
.	$0 > X , dec , Z > $0 , inc_pc , jmp FETCH
.end

.macro INC
.	$0 > X , inc , Z > $0 , inc_pc , jmp FETCH
.end

.macro LD_R16_nn
.	inc_pc
.	PC > ADDR
.	load_lo
.	inc_pc
.	PC > ADDR
.	load_hi
.	MBR > $0 , inc_pc , jmp FETCH
.end

.macro LD_R_n
.	inc_pc
.	PC > ADDR
.	load
.	MBR > $0 , inc_pc , jmp FETCH
.end

.macro LD_R_R
.LD_$0_B:
.	B > $0 , inc_pc , jmp FETCH
.LD_$0_C:
.	C > $0 , inc_pc , jmp FETCH
.LD_$0_D:
.	D > $0 , inc_pc , jmp FETCH
.LD_$0_E:
.	E > $0 , inc_pc , jmp FETCH
.LD_$0_H:
.	H > $0 , inc_pc , jmp FETCH
.LD_$0_L:
.	L > $0 , inc_pc , jmp FETCH
.LD_$0_(HL):
.	inc_pc , jmp FETCH
.LD_$0_A:
.	A > $0 , inc_pc , jmp FETCH
.end

.macro ALU_OP
.$0_B:
.	A > X , B > Y , $1 , Z > A , inc_pc , jmp FETCH
.$0_C:
.	A > X , C > Y , $1 , Z > A , inc_pc , jmp FETCH
.$0_D:
.	A > X , D > Y , $1 , Z > A , inc_pc , jmp FETCH
.$0_E:
.	A > X , E > Y , $1 , Z > A , inc_pc , jmp FETCH
.$0_H:
.	A > X , H > Y , $1 , Z > A , inc_pc , jmp FETCH
.$0_L:
.	A > X , L > Y , $1 , Z > A , inc_pc , jmp FETCH
.$0_(HL):
.	jmp $0
.$0_A:
.	A > X , A > Y , $1 , Z > A , inc_pc , jmp FETCH
.$0:
.	inc_pc , jmp FETCH
.end

.macro CP_R
.CP_B:
.	A > X , B > Y , sub , inc_pc , jmp FETCH
.CP_C:
.	A > X , C > Y , sub , inc_pc , jmp FETCH
.CP_D:
.	A > X , D > Y , sub , inc_pc , jmp FETCH
.CP_E:
.	A > X , E > Y , sub , inc_pc , jmp FETCH
.CP_H:
.	A > X , H > Y , sub , inc_pc , jmp FETCH
.CP_L:
.	A > X , L > Y , sub , inc_pc , jmp FETCH
.CP_(HL):
.	jmp CP
.CP_A:
.	A > X , A > Y , sub , inc_pc , jmp FETCH
.CP:
.	inc_pc , jmp FETCH
.end


.macro PUSH_R
.	SP > ADDR
.	$0 > MBR
.	store_lo -2
.	store_hi -1
.	SP > X , 2 > Y , sub , Z > SP
.end

.macro POP_R
.	SP > ADDR
.	load_lo
.	load_hi 1
.	MBR > $0
.	SP > X , 2 > Y , add , Z > SP
.end

.macro SWAP
.	$0 > TMP
.	$1 > $0
.	TMP > $1
.end

