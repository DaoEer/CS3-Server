# -*- coding: utf-8 -*-
from Interface.NPCAmbulantInterface import NPCAmbulantInterface
from Trap import Trap
class MoveTrapByTrigger(
	NPCAmbulantInterface,
	Trap,
	):
	def __init__(self):
		NPCAmbulantInterface.__init__(self)
		Trap.__init__(self)
