from os import exists
from sys import platform
from ctypes import *

class Downoloader:

	def __init__(self):
		if exists(f'statter.{"so" if platform in ["linux", "linux2"] else "dll"}'):
			statter = cdll.LoadLibrary(f'./plugins/statter.{"so" if platform in ["linux", "linux2"] else "dll"}')
			self.stat = statter.statistic
			self.stat.argtypes = [c_char_p] # path_to_database
			self.stat.restypes = None # writing to file "stat.json"