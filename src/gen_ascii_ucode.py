#!/usr/bin/python

from microinstr import MicroInstr
from parser import parse
from common import *

(microcode, labels, rlabels) = parse("microcode")

for mi in microcode:
	print mi.toAscii()

