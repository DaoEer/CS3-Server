# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
from ObjectScript.NPC import NPC

class NPCFastTeam( NPC.NPC ):
	def __init__( self ):
		NPC.NPC.__init__( self )

	def gossipWith(self, selfEntity, srcEntityID):
		"""
		处理玩家请求与NPC对话的信息
		"""
		pass