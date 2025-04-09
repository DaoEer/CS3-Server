# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_Pet import CPetAI
from PlayerAI.State.CStateInterface import eAIState

class PetAI( AIBase ):
	"""
	宠物AI
	"""
	def __init__(self):
		AIBase.__init__(self)
		self.actionStatus[eAIState.Pet] = CPetAI(self)
	
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.enterDefaultMap:
			#设置玩家等级
			self.owner.GMCommand(self.owner, "setLevel", "30")
			self.enterDefaultSpace()
			return
		
		self.think()
		
	def think(self):
		"""
		"""
		#宠物数据是否已经完成初始化
		if not self.owner.isInitPets:
			KBEngine.callback(5, self.think)
			return
		
		self.changeAIState(eAIState.Pet)

AIBase.setClass("PetAI", PetAI)		
	