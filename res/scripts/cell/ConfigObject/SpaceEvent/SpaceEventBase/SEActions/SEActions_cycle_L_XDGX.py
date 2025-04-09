# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
import random
import csdefine
import Math
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction251( SEActionBase ):
	"""
	环任务仙岛归墟 随机位置随机概率刷怪
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDList = [i for i in section["param1"].split("|")] # 怪物的scriptID
		self.probabilityList = [float(i) for i in section["param2"].split("|") ] # 概率

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		def random_pick(tempList,probabilityList):
			temp = random.uniform(0,1)
			tempProbability = 0.0
			for item,item_probability in zip(tempList,probabilityList):
				if item_probability == "":
					item_probability = 0
				tempProbability += float(item_probability)
				if temp < tempProbability:break
			return item
		scriptID = random_pick( self.scriptIDList,self.probabilityList )
		if not len(spaceEntity.floorIDList):
			return
		random.shuffle(spaceEntity.floorIDList)
		floorIDList = random.sample( spaceEntity.floorIDList,1)
		position = spaceEntity.getFloorPositionByFloorID(floorIDList[0])
		spaceEntity.createEntityByScriptID( scriptID, position, Math.Vector3(0,0,0),{"spawnPos":position} )

class SEAction252( SEActionBase ):
	"""
	环任务仙岛归墟 击杀土魔
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.probability = float(section["param1"]) #概率
		self.amount = int( section["param2"] ) #充能次数
		self.itemID = int( section["param3"] ) #息土物品ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		temp = random.uniform(0,1)
		if temp > self.probability:
			return
		killer = KBEngine.entities.get(eventParams["killerID"],None)
		if not killer or killer.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		itemInstList = killer.getItemInstsByID( self.itemID )
		for itemInst in itemInstList:
			itemInst.addUseNumber( self.amount, killer )

class SEAction253( SEActionBase ):
	"""
	环任务仙岛归墟 随机获得道具
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.itemIDList = [int(i) for i in section["param1"].split("|")]

	def do( self, spaceEntity, triggerID, eventParams ):
		killer = KBEngine.entities.get(eventParams["killerID"],None)
		if not killer or killer.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return
		itemIDList = random.sample( self.itemIDList, 1)
		killer.addItemByID(itemIDList[0])

class SEAction275( SEActionBase ):
	"""
	环任务仙岛归墟 已销毁格子刷出怪物
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptID = section["param1"]
		self.probability = float(section["param2"]) #概率
		self.amount = 0
		if section["param3"]:
			self.amount = int( section["param3"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		temp = random.uniform(0,1)
		if temp > self.probability:
			return
		refreshAmout = 0
		if self.amount == 0 or self.amount >= len(spaceEntity.destroyFloorIDList):
			refreshAmout = len( spaceEntity.destroyFloorIDList )
		else:
			refreshAmout = self.amount
		floorIDList = random.sample(spaceEntity.destroyFloorIDList,refreshAmout)
		for floorID in floorIDList:
			position = spaceEntity.getFloorPositionByFloorID( floorID )
			position = Math.Vector3( position.x, position.y -5.0,position.z )
			spaceEntity.createEntityByScriptID( self.scriptID,position,Math.Vector3(0,0,0),{"spawnPos":position} )

class SEAction278( SEActionBase ):
	"""
	环任务仙岛归墟 停止仙岛崩溃
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if spaceEntity.randomDestroyFloorTimerID:
			spaceEntity.popTimer( spaceEntity.randomDestroyFloorTimerID )
			spaceEntity.randomDestroyFloorTimerID = 0

class SEAction279( SEActionBase ):
	"""
	环任务仙岛归墟 随机销毁格子
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.delyTime = float( section["param1"] )
		self.destroyGrideNum = int( section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		if spaceEntity.stopTime > spaceEntity.alreadyStopTime:
			spaceEntity.addTimerCallBack( spaceEntity.stopTime - spaceEntity.alreadyStopTime, "startRandomDestroyFloor",(self.delyTime,self.destroyGrideNum)  )
		else:
			spaceEntity.startRandomDestroyFloor( self.delyTime, self.destroyGrideNum )

SEActionBase.setActionClass("SEAction251", SEAction251)
SEActionBase.setActionClass("SEAction252", SEAction252)
SEActionBase.setActionClass("SEAction253", SEAction253)
SEActionBase.setActionClass("SEAction275", SEAction275)
SEActionBase.setActionClass("SEAction278", SEAction278)
SEActionBase.setActionClass("SEAction279", SEAction279)
