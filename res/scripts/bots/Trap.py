# -*- coding: utf-8 -*-
import KBEngine
from Interface.NPCBaseObject import NPCBaseObject
from Interface.StateInterface import StateInterface
from Interface.SkillInterface import SkillInterface
class Trap(KBEngine.Entity,
	SkillInterface,
	StateInterface,
	NPCBaseObject,
	):
	def __init__(self):
		SkillInterface.__init__(self)
		StateInterface.__init__(self)
		KBEngine.Entity.__init__(self)
		NPCBaseObject.__init__(self)
		
	def CLIENT_PlayDeadEffect( self, p1 ):
		pass
	def CLIENT_DelayToAddTrap( self, p1 ):
		pass
