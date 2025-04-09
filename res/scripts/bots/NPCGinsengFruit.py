# -*- coding: utf-8 -*-
#
from NPC import NPC
from Interface.NPCAmbulantInterface import NPCAmbulantInterface
from Interface.StateInterface import StateInterface
class NPCGinsengFruit(NPC, StateInterface,
	NPCAmbulantInterface,
	):
	pass
