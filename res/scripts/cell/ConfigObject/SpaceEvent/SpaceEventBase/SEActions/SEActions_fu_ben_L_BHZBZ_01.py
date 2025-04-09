# -*- coding: utf-8 -*-
# 副本事件行为
import KBEDebug
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase
import random
import csdefine

class SEAction327( SEActionBase ):
	"""
	CST-7904 程序功能需求——（40级）帮会争霸第一场
	玩家被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.boxScriptID = section["param1"] #积分箱子的scriptID
		self.dropRateByTrap = float( section["param2"] ) # 被陷阱杀死掉的积分率
		self.dropRateByRole = float( section["param3"] ) # 被玩家杀死掉的积分率
		self.leastReduceIntegral = int( section["param4"] ) # 最少掉的积分

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()
		if killEntity == None:
			return
		dieEntityIntegral = spaceEntity.getMemberIntegral( dieEntity )
		if dieEntityIntegral <= 0:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_TRAP:
			boxEntity = spaceEntity.createEntityByScriptID( self.boxScriptID, dieEntity.position,dieEntity.direction,{} )
			if boxEntity:
				integral = math.ceil(self.dropRateByTrap * dieEntityIntegral)
				boxEntity.setTemp("integral",integral)
		elif killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE:
			integral = math.ceil( self.dropRateByRole * dieEntityIntegral )
			if integral < self.leastReduceIntegral:
				if self.leastReduceIntegral <= dieEntityIntegral:
					integral = self.leastReduceIntegral
				else:
					integral = dieEntityIntegral
			spaceEntity.addIntegral( killEntity,integral )
			spaceEntity.reduceIntegral( dieEntity, integral )

class SEAction328( SEActionBase ):
	"""
	CST-7904 程序功能需求——（40级）帮会争霸第一场
	怪物被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rewardIntegral = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		bossEntity = KBEngine.entities.get( triggerID, None )
		if not bossEntity:
			return
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if not killEntity:
			return
		if killEntity.getEntityFlag() == csdefine.ENTITY_FLAG_VEHICLEPET:
			killEntity = killEntity.getOwnerEntity()
		if killEntity == None:
			return
		spaceEntity.addIntegral( killEntity, self.rewardIntegral )

class SEAction329( SEActionBase ):
	"""
	CST-7904 程序功能需求——（40级）帮会争霸第一场
	每个帮会随机一名玩家获得守护之灵Buff
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffID = int( section["param1"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		tongs = spaceEntity.warInfos.getAllTongs()
		for tong in tongs:
			member = random.choice(tong.getMembers())
			member.mailbox.addBuff( member.mailbox, self.buffID )

SEActionBase.setActionClass("SEAction327", SEAction327)
SEActionBase.setActionClass("SEAction328", SEAction328)
SEActionBase.setActionClass("SEAction329", SEAction329)