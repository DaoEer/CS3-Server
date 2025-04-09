# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import csstatus
import csdefine
import Define


class MonsterExtJZZYDB( Monster.Monster ):
	"""
	真言地板(九字真言)
	"""
	def __init__( self ):
		"""
		"""
		Monster.Monster.__init__( self )
		self.monsterZYType = Define.MONSTER_JZZY_DB
		
	def recordSelfToSpace(self):
		"""
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.recordZYMonster(self.monsterZYType, self.zhenyanGroupID, self.id)
		
	def onAddCorrupt(self, speed):
		"""
		"""
		self.curCorrupt += speed
		if self.curCorrupt >= self.maxCorrupt:
			self.curCorrupt = self.maxCorrupt
	
	def onEnterZYDBScope(self, srcEntityID):
		"""
		Exposed method
		玩家进入某个真言对应的地板
		"""
		role = KBEngine.entities.get(srcEntityID)
		if not role or role.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onEnterZYDBScope( spaceEntity, role, self.zhenyanGroupID )
		
	def onLeaveZYDBScope(self, srcEntityID):
		"""
		Exposed method
		玩家离开某个真言对应的地板
		"""
		role = KBEngine.entities.get(srcEntityID)
		if not role or role.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			spaceEntity.getScript().onLeaveZYDBScope( spaceEntity, role, self.zhenyanGroupID)	
	
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
			if not isPlayerOccupy:
				self.addBuff(self, 14033503)
			self.allClients.onEndOccupy(isPlayerOccupy)
		except:
			pass