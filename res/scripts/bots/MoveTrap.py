# -*- coding: utf-8 -*-
from Interface.NPCAmbulantInterface import NPCAmbulantInterface
from Trap import Trap
class MoveTrap(
	NPCAmbulantInterface,
	Trap,
	):
	def __init__(self):
		NPCAmbulantInterface.__init__(self)
		Trap.__init__(self)
		
	def ChangeProgressBar(self,time):
		pass
	def CLIENT_ChangeProgressBar( self, p1 ):
		pass
