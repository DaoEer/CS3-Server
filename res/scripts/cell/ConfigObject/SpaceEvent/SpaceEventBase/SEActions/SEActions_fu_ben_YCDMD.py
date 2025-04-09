# -*- coding: utf-8 -*-

# 副本事件行为
import random
import csdefine
import ItemTypeEnum
import KBEngine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction346( SEActionBase ):
	"""
	CST-8726 勇闯夺命岛 玩家进入副本随机出生点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		trigger = KBEngine.entities.get(triggerID, None)
		if not trigger:
			return
		birthInfos = spaceEntity.getBirthInfos()
		if not birthInfos:
			return
		trigger.gotoSpace( spaceEntity.scriptID,birthInfos[0],birthInfos[1] )

class SEAction347( SEActionBase ):
	"""
	CST-8726 勇闯夺命岛 玩家被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.minDropItemAmount = int( section["param1"] )
		self.maxDropItemAmount = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		amount = random.randint( self.minDropItemAmount, self.maxDropItemAmount )
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		
		spaceEntity.onRoleBeKill( killEntity, dieEntity, amount )

class SEAction348( SEActionBase ):
	"""
	CST-8726 勇闯夺命岛 玩家进入副本随机出生点
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.bossScriptIDs = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		bossEntitys = []
		for bossScriptID in self.bossScriptIDs:
			bossEntitys.extend(spaceEntity.getEntityMailBoxRecord( bossScriptID ))
		if not len(bossEntitys):
			return
		for bossEntity in bossEntitys:
			if bossEntity.isBossCanUpLevel():
				bossEntity.setYCJMDBossLevel((bossEntity.getYCJMDBossLevel() + 1))

class SEAction349( SEActionBase ):
	"""
	CST-8726 勇闯夺命岛 小怪被击杀
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.itemIDs = [ int(i) for i in section["param1"].split("|") ] #奖励的物品ID
		self.amounts = [ int(i) for i in section["param2"].split("|") ]	#物品对应的数量
		self.rates = [ float(i) for i in section["param3"].split("|") ]	#物品对应的概率

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dieEntity = KBEngine.entities.get(triggerID,None)
		killEntity = KBEngine.entities.get( eventParams["killerID"],None )
		if dieEntity == None or killEntity == None:
			return
		tempItemDict = {}
		for itemID in self.itemIDs:
			index = self.itemIDs.index(itemID)
			rate = random.uniform(0,1)
			if rate < self.rates[index]:
				tempItemDict[itemID] = self.amounts[index]
		if killEntity.getEntityFlagExt() == csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_YCJMD:
			killEntity.addBossItemDictData( tempItemDict )

class SEAction350( SEActionBase ):
	"""
	CST-8726 勇闯夺命岛 随机概率 某个Boss提升至高级
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.rate = float( section["param1"] )
		self.bossScriptIDs = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		bossEntitys = []
		for bossScriptID in self.bossScriptIDs:
			bossEntitys.extend(spaceEntity.getEntityMailBoxRecord( bossScriptID ))
		if not len(bossEntitys):
			return
		rate = random.uniform(0,1)
		if rate < self.rate:
			bossEntity = random.choice( bossEntitys )
			bossEntity.setYCJMDBossMaxLevel()

class SEAction356( SEActionBase ):
	"""
	CST-8726 勇闯夺命岛 随机小Boss 找大Boss
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.searchBossScriptIDs = section["param1"].split("|") 	#搜索的大BossScriptID
		self.smallBossScriptIDs = section["param2"].split("|")		#小BossScriptID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return

		for smallBossScriptID in self.smallBossScriptIDs:
			smallBossEntitys = spaceEntity.getEntityMailBoxRecord( smallBossScriptID )
			if not len( smallBossEntitys ):
				continue
			bossEntity = random.choice( smallBossEntitys )
			searchBossScriptID = self.searchBossScriptIDs[ self.smallBossScriptIDs.index(smallBossScriptID) ]
			bossEntity.setTemp( "searchBossID",searchBossScriptID )


SEActionBase.setActionClass("SEAction346", SEAction346)
SEActionBase.setActionClass("SEAction347", SEAction347)
SEActionBase.setActionClass("SEAction348", SEAction348)
SEActionBase.setActionClass("SEAction349", SEAction349)
SEActionBase.setActionClass("SEAction350", SEAction350)
SEActionBase.setActionClass("SEAction356", SEAction356)
