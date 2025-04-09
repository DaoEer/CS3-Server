# -*- coding: utf-8 -*-
import KBEngine
from Interface.NPCBaseObject import NPCBaseObject
from Interface.SystemDropBoxPickUpInterface import SystemDropBoxPickUpInterface
class TeamDropBox(
	KBEngine.Entity,
	NPCBaseObject,
	SystemDropBoxPickUpInterface
	):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		NPCBaseObject.__init__(self)
		
	def onPickUpByLeader(self, p1, p2, p3):
		pass
		