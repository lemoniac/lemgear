import cmd

class Dbg(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = "(db) "
		self.intro = "LemGear Interactive Debugger"

	def do_breakpoint(self, s):
		pass

	def do_memory(self, s):
		pass

	def do_step(self, s):
		pass

	def do_regs(self, s):
		pass

	def do_reset(self, s):
		pass
		
	def do_run(self, s):
		print "run"
		pass

	def do_list(self, s):
		pass

	def do_quit(self, s):
		return True	

	def default(self, s):
		print "Syntax Error: " + s

idbg = Dbg()
idbg.cmdloop()

