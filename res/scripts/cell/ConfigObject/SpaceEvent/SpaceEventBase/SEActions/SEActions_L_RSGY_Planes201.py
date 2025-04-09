# -*- coding: utf-8 -*-

# 副本事件行为
import KBEDebug
import KBEngine
import Math
import random
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction57( SEActionBase ):
	"""
	人参果:通知触发者(人参果)向下
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(eventParams["entityID"],None)
		if entity == None:
			return
		dstPos = Math.Vector3(entity.position.x,entity.position.y - 100.0,entity.position.z) #和策划商量默认向下移动100米
		entity.startMove(dstPos)

class SEAction64( SEActionBase ):
	"""
	人参果 通知所有Entity往下落
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs = section["param1"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for scriptID in self.scriptIDs:
			idList = spaceEntity.getEntityRecord(scriptID)
			for id in idList:
				entity = KBEngine.entities.get(id,None)
				if entity == None:
					return
				dstPos = Math.Vector3(entity.position.x,entity.position.y - 100.0,entity.position.z) #和策划商量默认向下移动100米
				entity.startMove( dstPos )

class SEAction65( SEActionBase ):
	"""
	人参果：副本收到通知事件中的发送者位置，重新刷一个Entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.srcScriptIDs = section["param1"].split("|") #发送者的scripID列表
		self.scriptIDs = section["param2"].split("|") #所要对应创建的Entity列表


	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(eventParams["entityID"],None)
		if entity == None:
			return
		if entity.scriptID in self.srcScriptIDs:
			index = self.srcScriptIDs.index(entity.scriptID)
			entity.createEntityByScriptID(self.scriptIDs[index],entity.position,entity.direction,{"spawnPos":entity.position, "spawnDir": entity.direction})

class SEAction66( SEActionBase ):
	"""
	人参果：在触发者出生位置，重新随机刷一个Entity
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self.scriptIDs = section["param1"].split("|")
		self.delayTimeList = [ float(i) for i in section["param2"].split("|") ]

	def do( self, spaceEntity, triggerID, eventParams ):
		entity = KBEngine.entities.get(eventParams["entityID"],None)
		index = random.randint(0,len(self.scriptIDs) - 1)
		if entity and spaceEntity:
			position = entity.spawnPos
			direction = entity.direction
			spaceEntity.addTimerCallBack(self.delayTimeList[index],"createEntityByScriptID",(self.scriptIDs[index],position,direction,{"spawnPos":position, "spawnDir": direction}))

SEActionBase.setActionClass("SEAction57", SEAction57)
SEActionBase.setActionClass("SEAction64", SEAction64)
SEActionBase.setActionClass("SEAction65", SEAction65)
SEActionBase.setActionClass("SEAction66", SEAction66)