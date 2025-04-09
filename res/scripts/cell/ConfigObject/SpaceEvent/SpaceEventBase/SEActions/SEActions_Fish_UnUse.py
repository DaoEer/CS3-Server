# -*- coding: utf-8 -*-

# 副本事件行为
import random
import KBEDebug
import KBEngine
import csdefine
from ConfigObject.SpaceEvent.SpaceEventBase.SEActions.SEActionBase import SEActionBase

class SEAction71( SEActionBase ):
	"""
	进入钓鱼
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._smallFishFood = int(section["param1"])	#小鱼饵数量
		self._mediumFishFood = int(section["param2"])	#中鱼饵数量
		self._bigFishFood = int(section["param3"])		#大鱼饵数量

	def do( self, spaceEntity, triggerID, eventParams ):
		trigger = KBEngine.entities.get(triggerID,None)
		#spaceEntity.setTemp("fishScore",0)
		spaceEntity.getScript().spaceEvent_addCount( space,"fishScore",0 )
		spaceEntity.getScript().spaceEvent_addCount( space,"smallFishFood",self._smallFishFood )
		spaceEntity.getScript().spaceEvent_addCount( space,"mediumFishFood",self._mediumFishFood )
		spaceEntity.getScript().spaceEvent_addCount( space,"bigFishFood",self._bigFishFood )
		if trigger:
			#trigger.effectStateInc( csdefine.EFFECT_STATE_FIX )
			trigger.client.EnterFishState(self._smallFishFood,self._mediumFishFood,self._bigFishFood)

class SEAction72( SEActionBase ):
	"""
	开始钓鱼
	"""
	def init( self, section ):
		SEActionBase.init( self, section )

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		for e in spaceEntity._spaceRoles:
			e.client.StartFish()

class SEAction73( SEActionBase ):
	"""
	甩鱼竿
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._scriptID = section["param1"]	 	 	#怪物ScriptID
		self._moveTime = float(section["param2"])	#移动时间
		self._actionID = section["param3"]			#动作ID

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		dist = float(eventParams) * self._moveTime
		for e in spaceEntity._spaceRoles:
			entity = e.createEntityByScriptID(self._scriptID,e.position,e.direction,{"spawnPos":e.position, "spawnDir": e.direction})
			if entity:
				dstPos = e.direction.normalise() * dist + entity.position
				entity.moveToPosition(dstPos,True,True)
				e.allClients.CLIENT_OnPlayAction(self._actionID,-1.0)
				e.addTimerCallBack(self._moveTime,"startCheckFish",(entity.id,))

class SEAction74( SEActionBase ):
	"""
	计算上钩时间
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._fishTime = float(section["param1"])  #上钩时间
		self._smallFishRound = section["param2"].split("|")   #scriptID|距离小鱼
		self._mediumFishRound = section["param3"].split("|")
		self._bigFishRound = section["param4"].split("|")

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		fishFoodType = spaceEntity.queryTemp("fishFoodType")
		entityID = spaceEntity.queryTemp("fishFoodEntity")
		entityScr = KBEngine.entities.get( entityID,None )
		showTime = self._fishTime
		def getShowTime( showTime,scriptID, around,scriptIDScr,ratio ):
			idList = spaceEntity.getEntityRecord(scriptID)
			for id in idList:
				entity = KBEngine.entities.get( id,None )
				if entity:
					entityList = entity.entitiesInRangeExt(float(around),"Monster")
					for e in entitylist:
						if e.scriptID == scriptIDScr:
							showTime = ratio * showTime
			return showTime

		#if entityScr != None:
		if fishFoodType == csdefine.FISH_BSET_SMALL_TYPE:
			showTime = getShowTime(showTime,self,_smallFishRound[0],self._smallFishRound[1],entityScr.scriptID,0.3)
			spaceEntity.getScript().spaceEvent_addCount( space,"smallFishFood",-1 )
		elif fishFoodType == csdefine.FISH_BSET_MEDIUM_TYPE:
			showTime = getShowTime(showTime,self,_mediumFishRound[0],self._mediumFishRound[1],entityScr.scriptID,0.45)
			spaceEntity.getScript().spaceEvent_addCount( space,"mediumFishFood",-1 )
		elif fishFoodType == csdefine.FISH_BSET_BIG_TYPE:
			showTime = getShowTime(showTime,self,_bigFishRound[0],self._bigFishRound[1],entityScr.scriptID,0.6)
			spaceEntity.getScript().spaceEvent_addCount( space,"bigFishFood",-1 )
		for e in spaceEntity._spaceRoles:
			e.addTimerCallBack(showTime,"ChangeWrestlingWidget",())

class SEAction75( SEActionBase ):
	"""
	计算是否钓到鱼
	"""
	def init( self, section ):
		SEActionBase.init( self, section )
		self._dist = float(section["param1"]) # 离玩家多近可以钓到鱼

	def do( self, spaceEntity, triggerID, eventParams ):
		if not spaceEntity:
			return
		entityID = spaceEntity.queryTemp("fishFoodEntity")
		entity = KBEngine.entities.get(entityID,None )
		entity.stopMovingForType( csdefine.SYSTEM_MOVE )
		power = int(eventParams)
		if entity == None:
			KBEDebug.ERROR_MSG("----fish error----")
			return
		def check():
			for e in spaceEntity._spaceRoles:
				if (entity.flatDistTo(e.position) > self._dist) and power <= 0:
					e.statusMessage(csstatus.FISH_IS_MISS,"")
				else:
					e.statusMessage( csstatus.CATCH_FISH_SUCCESS,"" )
					foodType = spaceEntity.queryTemp("fishFoodType")
					if foodType == csdefine.FISH_BSET_SMALL_TYPE:
						spaceEntity.getScript().spaceEvent_addCount( space,"fishScore",10 )
					elif foodType == csdefine.FISH_BSET_SMALL_TYPE:
						spaceEntity.getScript().spaceEvent_addCount( space,"fishScore",25 )
					elif foodType == csdefine.FISH_BSET_SMALL_TYPE:
						spaceEntity.getScript().spaceEvent_addCount( space,"fishScore",40 )

		addSpeed = 0.0
		if power > 0:
			power -= 50
			addSpeed = ceil(power / 50 * 4) + power / 50
		else:
			check()
			return
		srcSpeed = entity.getSpeed()
		entity.setSpeed( srcSpeed + addSpeed )
		for e in spaceEntity._spaceRoles:
			entity.moveToPosition(e.position,True,True)
			#dist = entity.position.flatDistTo(e.position)
			#time = dist / entity.getSpeed()
			#e.addTimerCallBack( time,"check" )
			check()

SEActionBase.setActionClass("SEAction71", SEAction71)
SEActionBase.setActionClass("SEAction72", SEAction72)
SEActionBase.setActionClass("SEAction73", SEAction73)
SEActionBase.setActionClass("SEAction74", SEAction74)
SEActionBase.setActionClass("SEAction75", SEAction75)