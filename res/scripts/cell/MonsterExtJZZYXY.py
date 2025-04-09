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


class MonsterExtJZZYXY( Monster.Monster ):
	"""
	真言虚影(九字真言)
	"""
	def __init__( self ):
		"""
		"""
		Monster.Monster.__init__( self )
		self.monsterZYType = Define.MONSTER_JZZY_XY
		
	def recordSelfToSpace(self):
		"""
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.recordZYMonster(self.monsterZYType, self.zhenyanGroupID, self.id)
			
	def onTreadZYPoint(self, srcEntityID):
		"""
		Exposed method
		玩家踩虚影上的点完成
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, "OCCUPYZY", "1|{}".format(str(self.zhenyanGroupID)))
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, Define.MONSTER_JZZY_COMMOND_DICT.get(self.getScript().zhenYanType), "")
		
	def onTreadZYXY(self, srcEntityID):
		"""
		Exposed method
		玩家踩在某个真言对应的虚影上
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onConditionChange( spaceEntity, "", spaceEntity.id, str(self.zhenyanGroupID), "")
	
	def onAddCorrupt(self, speed):
		"""
		"""
		pass
		
	def startOccupy(self):
		"""
		开始
		"""
		try:
			self.allClients.onStartOccupy()
		except:
			pass
		
	def endCorrupt(self, isPlayerOccupy):
		"""
		结束
		"""
		try:
			self.allClients.onEndOccupy(isPlayerOccupy)
			#如果不是玩家占领，那么已经点亮的要全部熄灭
			if not isPlayerOccupy: self.allClients.onExtinguishLight(0)
		except:
			pass
	
		
	
