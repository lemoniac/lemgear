#!/usr/bin/python

from parser import parse

(microcode, labels, rlabels) = parse("microcode/z80/microcode.mcr")

for mi in microcode:
    print mi.to_ascii()

