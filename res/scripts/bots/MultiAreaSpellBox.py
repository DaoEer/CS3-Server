# -*- coding: utf-8 -*-
import KBEngine
from Interface.NPCBaseObject import NPCBaseObject
from Interface.SkillInterface import SkillInterface
class MultiAreaSpellBox(KBEngine.Entity, 
	NPCBaseObject, 
	SkillInterface, ):
	def __init__(self):
		NPCBaseObject.__init__(self) 
		SkillInterface.__init__(self) 
	def CLIENT_OnSwitchArea( self, p1 ):
		pass
