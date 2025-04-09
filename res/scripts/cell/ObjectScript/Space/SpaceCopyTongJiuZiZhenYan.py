# -*- coding: utf-8 -*-


import KBEDebug
import KBEngine
import Math
import KBEMath
import Functions
import csdefine
import Define
from ObjectScript.Space.SpaceCopyTong import SpaceCopyTong

class SpaceCopyTongJiuZiZhenYan( SpaceCopyTong ):
	"""
	帮会副本(九字真言)
	"""
	def __init__( self ):
		SpaceCopyTong.__init__( self )
	
	def initData( self, configData ):
		"""
		virtual method
		"""
		SpaceCopyTong.initData( self, configData )
		self.bossID = configData["SpaceData"].get("bossID","")
		self.buffID = int(configData["SpaceData"].get("buffID", "0"))
		
	def initEntity( self, selfEntity ):
		"""
		virtual method
		初始化space entity要做的事情
		"""
		SpaceCopyTong.initEntity( self, selfEntity )
		
	def onEnterZYDBScope( self, selfEntity, role, groupID ):
		"""
		"""
		lastScopeID = role.queryTemp("JZZYDBSCOPID", None)
		role.setTemp("JZZYDBSCOPID", groupID)
		if not selfEntity.isOpenDamage:
			return
		
		if lastScopeID == groupID: return
		if groupID in selfEntity.playerOccupyZhenYan:
			role.onReduceShangHaiBuff()
			return
		
		role.onAddShangHaiBuff(self.buffID)
		
	def onLeaveZYDBScope( self, selfEntity, role, groupID ):
		"""
		"""
		pass
		
	def onSetOpenDamage(self, selfEntity):
		"""
		"""
		for role in selfEntity._spaceRoles:
			groupID = role.queryTemp("JZZYDBSCOPID", None)
			if groupID is None: continue
			
			if groupID in selfEntity.playerOccupyZhenYan or not selfEntity.isOpenDamage:
				role.onReduceShangHaiBuff()
			else:
				role.onAddShangHaiBuff(self.buffID)
			
	def onStartOccupy(self, selfEntity, groupID):
		"""
		"""
		temp = selfEntity.zhenYanMonster[groupID]
		for entityID in list(temp.values()):
			e = KBEngine.entities.get(entityID)
			if e: e.startOccupy()
		
	def onEndOccupy(self, selfEntity, groupID, isPlayerOccupy):
		"""
		"""
		self.onSetOpenDamage(selfEntity)
		temp = selfEntity.zhenYanMonster[groupID]
		for entityID in list(temp.values()):
			entity = KBEngine.entities.get(entityID)
			if entity:entity.endCorrupt(isPlayerOccupy)
			if entity.monsterZYType != Define.MONSTER_JZZY_ZY:
				continue
			
			buffInfo = entity.getScript().getBuffInfo()
			if not buffInfo: 
				continue
			
			if not isPlayerOccupy: 
				self.onBossAddBuff(selfEntity, buffInfo[2])
				continue
			
			if entity.zhenyanType in [Define.MONSTER_JZZY_TYPE_JIE, Define.MONSTER_JZZY_TYPE_ZHEN]:
				buffList = selfEntity.queryTemp("BOSSGAILVBUFF", [])
				buffList.append(int(buffInfo[1]))
				selfEntity.setTemp("BOSSGAILVBUFF", buffList)
			
	def onBossAddBuff(self, selfEntity, buffID):
		"""
		"""
		bossIDList = selfEntity.getEntityRecord(self.bossID)
		if len(bossIDList) > 0:
			for id in bossIDList:
				entity = KBEngine.entities.get(id)
				if entity:entity.addBuff(entity, buffID)
				
	def onRoleAddBuff(self, selfEntity, buffID):
		"""
		"""
		for role in selfEntity._spaceRoles:
			role.addBuff(role, buffID)
		
	def onAddCorrupt(self, selfEntity, groupID):
		"""
		"""
		temp = selfEntity.zhenYanMonster[groupID]
		for entityID in list(temp.values()):
			e = KBEngine.entities.get(entityID)
			if e: e.onAddCorrupt(selfEntity.occupySpeed)
		
		#到这里意味着已经全部腐化
		selfEntity.curCorrupt += selfEntity.occupySpeed
		if selfEntity.curCorrupt >= selfEntity.maxCorrupt:
			self.onConditionChange( selfEntity, "", selfEntity.id, "OCCUPYZY", "0|{}".format(str(groupID)))
			
	def onExtinguishLight(self, selfEntity, amount):
		"""
		"""
		#已经结束占领了，没必要再回溯了
		if len(selfEntity.hasOccupyZhenYan) >= len(selfEntity.zhenYanMonster):
			return
		
		for role in selfEntity._spaceRoles:
			if role.getClient():
				role.getClient().onExtinguishLight(amount)
				
	def onLeave( self, selfEntity, playerRole, packArgs ):
		"""
		virtual method
		玩家离开副本
		"""
		playerRole.clearJZZYData()
		SpaceCopyTong.onLeave(self, selfEntity, playerRole, packArgs )