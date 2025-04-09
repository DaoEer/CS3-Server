# -*- coding: utf-8 -*-

from SpaceCopyLBCBase import SpaceCopyLBCBase
import csdefine
import KBEngine

class SpaceCopyLBCPVP(SpaceCopyLBCBase):
	"""
	高级练兵场-英雄王座玩法
	"""
	def __init__(self) :
		SpaceCopyLBCBase.__init__(self)
		self._init()
	
	def _init(self):
		"""
		"""
		self.offensiveScripts = self.getScript().getOffensiveScripts()
		self.defensiveScripts = self.getScript().getDefensiveScripts()
	
#------------------------------重载--------------------------------------------
	def addEntityMailBoxRecord( self, scriptID, entityMailBox ):
		"""
		增加 soldiersDict 记录
		"""
		SpaceCopyLBCBase.addEntityMailBoxRecord(self, scriptID, entityMailBox)
		if scriptID in self.offensiveScripts:
			entityMailBox.setBelongSide(csdefine.BELONG_SIDE_ATTACK)
		elif scriptID in self.defensiveScripts:
			entityMailBox.setBelongSide(csdefine.BELONG_SIDE_PROTECT)
		

	def getDynamicReviverInfo( self, camp = csdefine.BELONG_SIDE_ATTACK ):
		"""
		<Define method>
		获取副本动态复活点
		"""
		if camp == csdefine.BELONG_SIDE_ATTACK:
			return (self.dynamicTaosimReviverPos,self.dynamicTaosimReviverDir)
		elif camp == csdefine.BELONG_SIDE_PROTECT:
			return (self.dynamicDemonReviverPos,self.dynamicDemonReviverDir)
		else:
			return  (self.dynamicTaosimReviverPos,self.dynamicTaosimReviverDir)