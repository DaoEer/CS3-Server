# -*- coding: utf-8 -*-
#
import random
import Const
import time
import NPC

from ConfigObject.Trade.TradeMgr import g_tradeMgr


class NPCNeuralShop( NPC.NPC ):
	"""
	英雄联盟 中立商店NPC
	"""
	def __init__(self):
		NPC.NPC.__init__(self)
		self.mScriptIDs = {}				# { scriptID : 购买次数 }
		self.level = 1
		self.initNeuralShop()
		
	def initNeuralShop( self ):
		""""""
		scriptIDs = list(g_tradeMgr.LMNeuralItem)
		space = self.getCurrentSpace()
		if space:
			if space.getEntityRecord(Const.NOTDUPLICATE_MONSTER_SCRIPTID):
				if Const.NOTDUPLICATE_MONSTER_SCRIPTID in scriptIDs:
					scriptIDs.remove( Const.NOTDUPLICATE_MONSTER_SCRIPTID )
					
			scriptIDs = random.sample( scriptIDs, 2 )
			for scriptID in scriptIDs:
				self.mScriptIDs[scriptID] = 1
			passTime = int( (time.time() - space.lifeStartTime)/60 )
			self.level = g_tradeMgr.getGuardLevelsByTime( scriptIDs[0], passTime )
		
	def canCallMonster( self, scriptID ):
		"""是否能召唤怪物"""
		if scriptID in self.mScriptIDs:
			return self.mScriptIDs[scriptID] >= 1
		return False
		
	def onCallMonster( self, scriptID ):
		"""召唤怪物"""
		if scriptID in self.mScriptIDs:
			self.mScriptIDs[scriptID] -= 1
