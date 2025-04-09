# -*- coding: utf-8 -*-
import KBEngine
from Interface.NPCBaseObject import NPCBaseObject
from Interface.NPCTalkInterface import NPCTalkInterface
from Interface.NPCQuestInterface import NPCQuestInterface
class NPC(
	NPCQuestInterface,
	KBEngine.Entity,
	NPCBaseObject,
	NPCTalkInterface,
	):
	def __init__(self):
		NPCQuestInterface.__init__(self)
		KBEngine.Entity.__init__(self)
		NPCBaseObject.__init__(self)
		NPCTalkInterface.__init__(self)
	def SetQuestSign(self, questStatus):
		pass
