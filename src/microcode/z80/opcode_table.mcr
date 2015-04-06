00:
    jmp NOP
01:
    jmp LD_BC_nn
02:
    jmp LD_(BC)_A
03:
    jmp INC_BC
04:
    jmp INC_B
05:
    jmp DEC_B
06:
    jmp LD_B_n
07:
    jmp NOP
08:
    jmp EX_AF_AFs
09:
    jmp NOP
0a:
    jmp NOP
0b:
    jmp DEC_BC
0c:
    jmp INC_C
0d:
    jmp DEC_C
0e:
    jmp LD_C_n
0f:
    jmp NOP
10:
    jmp DJNZ
11:
    jmp LD_DE_nn
12:
    jmp LD_(DE)_A
13:
    jmp INC_DE
14:
    jmp INC_D
15:
    jmp DEC_D
16:
    jmp LD_D_n
17:
    jmp NOP
18:
    jmp NOP
19:
    jmp NOP
1a:
    jmp NOP
1b:
    jmp DEC_DE
1c:
    jmp INC_E
1d:
    jmp DEC_E
1e:
    jmp LD_E_n
1f:
    jmp NOP
20:
    jmp JR_NZ_e
21:
    jmp LD_HL_nn
22:
    jmp LD_(nn)_HL
23:
    jmp INC_HL
24:
    jmp INC_H
25:
    jmp INC_L
26:
    jmp LD_H_n
27:
    jmp NOP
28:
    jmp JR_Z_e
29:
    jmp NOP
2a:
    jmp NOP
2b:
    jmp DEC_HL
2c:
    jmp INC_L
2d:
    jmp INC_L
2e:
    jmp LD_L_n
2f:
    jmp NOP
30:
    jmp JR_NC_e
31:
    jmp LD_SP_nn
32:
    jmp LD_(nn)_A
33:
    jmp INC_SP
34:
    jmp NOP
35:
    jmp NOP
36:
    jmp LD_(HL)_n
37:
    jmp NOP
38:
    jmp JR_C_e
39:
    jmp NOP
3a:
    jmp LD_A_(nn)
3b:
    jmp DEC_SP
3c:
    jmp INC_A
3d:
    jmp DEC_A
3e:
    jmp LD_A_n
3f:
    jmp NOP
40:
    jmp LD_B_B
41:
    jmp LD_B_C
42:
    jmp LD_B_D
43:
    jmp LD_B_E
44:
    jmp LD_B_H
45:
    jmp LD_B_L
46:
    jmp LD_B_(HL)
47:
    jmp LD_B_A
48:
    jmp LD_C_B
49:
    jmp LD_C_C
4a:
    jmp LD_C_D
4b:
    jmp LD_C_E
4c:
    jmp LD_C_H
4d:
    jmp LD_C_L
4e:
    jmp LD_C_(HL)
4f:
    jmp LD_C_A
50:
    jmp LD_D_B
51:
    jmp LD_D_C
52:
    jmp LD_D_D
53:
    jmp LD_D_E
54:
    jmp LD_D_H
55:
    jmp LD_D_L
56:
    jmp LD_D_(HL)
57:
    jmp LD_D_A
58:
    jmp LD_E_B
59:
    jmp LD_E_C
5a:
    jmp LD_E_D
5b:
    jmp LD_E_E
5c:
    jmp LD_E_H
5d:
    jmp LD_E_L
5e:
    jmp LD_E_(HL)
5f:
    jmp LD_E_A
60:
    jmp LD_H_B
61:
    jmp LD_H_C
62:
    jmp LD_H_D
63:
    jmp LD_H_E
64:
    jmp LD_H_H
65:
    jmp LD_H_L
66:
    jmp LD_H_(HL)
67:
    jmp LD_H_A
68:
    jmp LD_L_B
69:
    jmp LD_L_C
6a:
    jmp LD_L_D
6b:
    jmp LD_L_E
6c:
    jmp LD_L_H
6d:
    jmp LD_L_L
6e:
    jmp LD_L_(HL)
6f:
    jmp LD_L_A
70:
    jmp LD_(HL)_B
71:
    jmp LD_(HL)_C
72:
    jmp LD_(HL)_D
73:
    jmp LD_(HL)_E
74:
    jmp LD_(HL)_H
75:
    jmp LD_(HL)_L
76:
    jmp HALT
77:
    jmp LD_(HL)_A
78:
    jmp LD_A_B
79:
    jmp LD_A_C
7a:
    jmp LD_A_D
7b:
    jmp LD_A_E
7c:
    jmp LD_A_H
7d:
    jmp LD_A_L
7e:
    jmp LD_A_(HL)
7f:
    jmp LD_A_A
80:
    jmp ADD_B
81:
    jmp ADD_C
82:
    jmp ADD_D
83:
    jmp ADD_E
84:
    jmp ADD_H
85:
    jmp ADD_L
86:
    jmp ADD_(HL)
87:
    jmp ADD_A
88:
    jmp NOP
89:
    jmp NOP
8a:
    jmp NOP
8b:
    jmp NOP
8c:
    jmp NOP
8d:
    jmp NOP
8e:
    jmp NOP
8f:
    jmp NOP
90:
    jmp SUB_B
91:
    jmp SUB_C
92:
    jmp SUB_D
93:
    jmp SUB_E
94:
    jmp SUB_H
95:
    jmp SUB_L
96:
    jmp SUB_(HL)
97:
    jmp SUB_A
98:
    jmp NOP
99:
    jmp NOP
9a:
    jmp NOP
9b:
    jmp NOP
9c:
    jmp NOP
9d:
    jmp NOP
9e:
    jmp NOP
9f:
    jmp NOP
a0:
    jmp OR_B
a1:
    jmp OR_C
a2:
    jmp OR_D
a3:
    jmp OR_E
a4:
    jmp OR_H
a5:
    jmp OR_L
a6:
    jmp OR_(HL)
a7:
    jmp OR_A
a8:
    jmp XOR_B
a9:
    jmp XOR_C
aa:
    jmp XOR_D
ab:
    jmp XOR_E
ac:
    jmp XOR_H
ad:
    jmp XOR_L
ae:
    jmp XOR_(HL)
af:
    jmp XOR_A
b0:
    jmp NOP
b1:
    jmp NOP
b2:
    jmp NOP
b3:
    jmp NOP
b4:
    jmp NOP
b5:
    jmp NOP
b6:
    jmp NOP
b7:
    jmp NOP
b8:
    jmp CP_B
b9:
    jmp CP_C
ba:
    jmp CP_D
bb:
    jmp CP_E
bc:
    jmp CP_H
bd:
    jmp CP_L
be:
    jmp CP_(HL)
bf:
    jmp CP_A
c0:
    jmp NOP
c1:
    jmp POP_BC
c2:
    jmp NOP
c3:
    jmp JP
c4:
    jmp NOP
c5:
    jmp PUSH_BC
c6:
    jmp NOP
c7:
    jmp NOP
c8:
    jmp NOP
c9:
    jmp RET
ca:
    jmp NOP
cb:
    jmp NOP
cc:
    jmp NOP
cd:
    jmp CALL
ce:
    jmp NOP
cf:
    jmp NOP
d0:
    jmp NOP
d1:
    jmp POP_DE
d2:
    jmp NOP
d3:
    jmp OUTA
d4:
    jmp NOP
d5:
    jmp PUSH_DE
d6:
    jmp NOP
d7:
    jmp NOP
d8:
    jmp NOP
d9:
    jmp EXX
da:
    jmp NOP
db:
    jmp INA
dc:
    jmp NOP
dd:
    jmp NOP
de:
    jmp NOP
df:
    jmp NOP
e0:
    jmp NOP
e1:
    jmp POP_HL
e2:
    jmp NOP
e3:
    jmp NOP
e4:
    jmp NOP
e5:
    jmp PUSH_HL
e6:
    jmp NOP
e7:
    jmp NOP
e8:
    jmp NOP
e9:
    jmp NOP
ea:
    jmp NOP
eb:
    jmp EX_DE_HL
ec:
    jmp NOP
ed:
    jmp prefix_ED
ee:
    jmp NOP
ef:
    jmp NOP
f0:
    jmp NOP
f1:
    jmp POP_AF
f2:
    jmp NOP
f3:
    jmp DI
f4:
    jmp NOP
f5:
    jmp PUSH_AF
f6:
    jmp NOP
f7:
    jmp NOP
f8:
    jmp NOP
f9:
    jmp NOP
fa:
    jmp NOP
fb:
    jmp EI
fc:
    jmp NOP
fd:
    jmp NOP
fe:
    jmp CP_n
ff:
    jmp NOP

