# -*- coding: utf-8 -*-
import KBEngine
from Interface.NPCBaseObject import NPCBaseObject
from Interface.NPCAmbulantInterface import NPCAmbulantInterface
from Interface.NPCTalkInterface import NPCTalkInterface
from Interface.NPCQuestInterface import NPCQuestInterface
class NPCExtGuide(KBEngine.Entity, 
	NPCBaseObject, 
	NPCAmbulantInterface,
	NPCTalkInterface,
	NPCQuestInterface):
	pass
