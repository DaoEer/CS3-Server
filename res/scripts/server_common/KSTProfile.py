# -*- coding: utf-8 -*-
import cProfile
from KBEDebug import *

def KST_Profile(func):
	def wrapper(*args, **kwargs):
		pr = cProfile.Profile()
		pr.enable()
		res = func(*args, **kwargs)
		pr.disable()
		pr.print_stats(-1)
		return res
	return wrapper
	
def KST_DEBUG(func):
	def wrapper(*args, **kwargs):
		ERROR_MSG("BEFORE")
		ERROR_MSG(func)
		res = func(*args, **kwargs)
		ERROR_MSG("END")
		return res
	return wrapper