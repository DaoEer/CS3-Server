# -*- coding: utf-8 -*-
#
import KBEngine
from KBEDebug import *
import CoreObject.NPCObject as NPCObject
import CoreInterface.NPCTalkInterface as NPCTalkInterface
import CoreInterface.NPCQuestInterface as NPCQuestInterface


class NPC(NPCObject.NPCObject, NPCTalkInterface.NPCTalkInterface, NPCQuestInterface.NPCQuestInterface ):
	"""
	"""
	def __init__(self):
		NPCObject.NPCObject.__init__(self)
		NPCTalkInterface.NPCTalkInterface.__init__(self)
		NPCQuestInterface.NPCQuestInterface.__init__(self)
