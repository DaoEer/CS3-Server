# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
import random
import KBEMath
import Math
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction234( SEActionBase ):
	"""
	环任务消灭影妖 收到打开照妖镜的通知
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.high = float( section["param1"] )
		self.radius = float(section["param2"] )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityID = eventParams["senderID"]
		entity = KBEngine.entities.get( entityID,None )
		if not entity:
			return
		if entity.getClient():
			entity.client.CLIENT_OpenMonsterMirror( self.high,self.radius )

class SEAction235( SEActionBase ):
	"""
	环任务消灭影妖  玩家离开副本清除数据 触发者是玩家
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffID = int(section["param1"]) #照妖镜环绕玩家Buff

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get( triggerID,None )
		if not entity:
			return
		entity.removeBuffByID( self.buffID )
		entity.removeTemp("curLingEnergyValue")
		entity.removeTemp("maxLingEnergyValue")
		entity.removeTemp("reduceLingEnergyValue")
		entity.removeTemp("isPlaySound")
		entity.CELL_closeMonsterMirror(entity.id)
		if entity.getClient():
			entity.client.CLIENT_HideLingEnergyBar()

class SEAction238( SEActionBase ):
	"""
	环任务消灭影妖  随机鼎发亮
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.buffID = int( section["param1"] )	# 移除鼎的Buff 为了能交互
		self.scriptID = section["param2"] # 鼎的scriptID
		self.addBuffAmount = int( section["param3"] )	#取鼎发亮的数量

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityList = spaceEntity.getEntityMailBoxRecord( self.scriptID )
		if not entityList:
			return
		for entity in entityList:
			entity.addBuff(entity,self.buffID)
		indexList = list(range(0,len(entityList)))
		random.shuffle( indexList )
		if self.addBuffAmount > len(indexList):
			return
		randomIndexList = random.sample( indexList, self.addBuffAmount )
		for index in randomIndexList:
			entityList[index].removeBuffByID( self.buffID )

SEActionBase.setActionClass("SEAction234", SEAction234)
SEActionBase.setActionClass("SEAction235", SEAction235)
SEActionBase.setActionClass("SEAction238", SEAction238)
