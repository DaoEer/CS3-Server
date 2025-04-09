# -*- coding: utf-8 -*-


#python
#engine
import KBEDebug
import KBEngine
#script
import Monster
import csstatus
import csdefine
import Define

class MonsterExtJiuZiZhenYan( Monster.Monster ):
	"""
	九字真言副本(真言)
	"""
	def __init__( self ):
		"""
		"""
		Monster.Monster.__init__( self )
		self.monsterZYType = Define.MONSTER_JZZY_ZY
		self.zhenyanType = self.getScript().zhenYanType
		
	def recordSelfToSpace(self):
		"""
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.recordZYMonster(self.monsterZYType, self.zhenyanGroupID, self.id)
			
	def setMaxCorrupt(self, value):
		"""
		"""
		self.maxCorrupt = value
		
	def onAddCorrupt(self, speed):
		"""
		"""
		self.curCorrupt += speed
		if self.curCorrupt >= self.maxCorrupt:
			self.curCorrupt = self.maxCorrupt
		
	def startOccupy(self):
		"""
		开始腐化
		"""
		try:
			self.addBuff(self, 14033501)
			self.allClients.onStartOccupy()
		except:
			pass
		
	def endCorrupt(self, isPlayerOccupy):
		"""
		结束腐化
		"""
		try:
			self.removeBuff(self, 14033501)
			if not isPlayerOccupy:
				self.addBuff(self, 14033502)
			else:
				self.addBuff(self, 14033503)
			self.allClients.onEndOccupy(isPlayerOccupy)
		except:
			pass
		
	
		
	
		
	
