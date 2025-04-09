# -*- coding: utf-8 -*-

import random
import KBEDebug
from SpaceCopyTong import SpaceCopyTong
import Math
import KBEngine
import csdefine
import csstatus
import Const

class SpaceCopyTongJiuZiZhenYan( SpaceCopyTong ):
	"""
	帮会副本(九字真言)
	"""
	def __init__( self ) :
		SpaceCopyTong.__init__( self )
		self.zhenYanMonster = {}		#真言
		self.occupySpeed = 0			#腐化速度
		self.curCorrupt	 = 0			#当前值
		self.maxCorrupt = 0				#真言最大腐化值
		self.hasOccupyZhenYan = []		#已被boss/玩家占领的真言
		self.playerOccupyZhenYan = []	#玩家占领的真言
		self.isOpenDamage = False		#是否开启增加伤害buff
		self.corruptTimerID = 0
		self.curGroupID = -1
		
	def recordZYMonster(self, type, groupID, entityID):
		"""
		"""
		if groupID not in self.zhenYanMonster:	
			self.zhenYanMonster[groupID] = {}
		if type not in self.zhenYanMonster[groupID]:
			self.zhenYanMonster[groupID][type] = entityID
		
	def setOpenDamage(self, isOpen):
		"""
		"""
		self.isOpenDamage = isOpen
		self.getScript().onSetOpenDamage(self)
		
	def recordOccupyScope(self, groupID, isPlayerOccupy):
		"""
		"""
		if isPlayerOccupy: 
			self.playerOccupyZhenYan.append(groupID)
		self.hasOccupyZhenYan.append(groupID)
		self.getScript().onSetOpenDamage(self)
			
	def onStartOccupy(self, groupID):
		"""
		"""
		if groupID < 0 or groupID in self.hasOccupyZhenYan:
			return
		
		self.curCorrupt = 0
		self.curGroupID = groupID
		self.getScript().onStartOccupy(self, groupID)
		self.corruptTimerID = self.addTimerRepeat( 1.0, "onAddCorrupt", () )
		
	def onEndOccupy(self, groupID, isPlayerOccupy):
		"""
		"""
		if groupID < 0 or groupID in self.hasOccupyZhenYan:
			return
		
		if groupID == self.curGroupID:
			self.popTimer(self.corruptTimerID)
			self.corruptTimerID = 0
			self.curCorrupt = self.maxCorrupt
			self.curGroupID = -1
		 
		self.recordOccupyScope(groupID, isPlayerOccupy)
		self.getScript().onEndOccupy(self, groupID, isPlayerOccupy)
		
	def onAddCorrupt(self):
		"""
		"""
		if self.curGroupID < 0: return
		self.getScript().onAddCorrupt(self, self.curGroupID)
		
	def setMaxCorrupt(self, value):
		"""
		"""
		self.maxCorrupt = value
		