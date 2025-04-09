# -*- coding: utf-8 -*-

# 副本事件条件
import time
import csdefine
import KBEngine
import KBEDebug
import math
import random
from ConfigObject.SpaceEvent.SpaceEventBase.SEConditions.SEConditionBase import SEConditionBase

class SECondition1( SEConditionBase ):
	"""
	触发者血量低于某个百分比
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.param1 = float( section["param1"] )
	
	def check( self, entity, eventParams ):
		return float( entity.HP )/entity.HP_Max < self.param1

class SECondition2( SEConditionBase ):
	"""
	触发者scriptID为某些值
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")
	
	def check( self, entity, eventParams ):
		return entity.getScriptID() in self.scriptIDList

class SECondition3( SEConditionBase ):
	"""
	玩家世界区域改变事件中，判断进入的是哪个区域
	这种由客户端检测的条件，服务器端也必须有这个条件脚本，内部直接pass
	"""
	def __init__( self, dataDict = {} ):
		SEConditionBase.__init__( self, dataDict )
		self.isClientCon = True

class SECondition4( SEConditionBase ):
	"""
	副本开始/完成阶段为某阶段
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.param1 = int( section["param1"] )
	
	def check( self, entity, eventParams ):
		return eventParams["stageIndex"] == self.param1

class SECondition5( SEConditionBase ):
	"""
	副本某阶段是否已完成
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.stageIndex = int( section["param1"] )
	
	def check( self, spaceEntity, eventParams ):
		return self.stageIndex in spaceEntity.completeSpaceStages

class SECondition6( SEConditionBase ):
	"""
	副本某阶段是否未完成
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.stageIndex = int( section["param1"] )
	
	def check( self, spaceEntity, eventParams ):
		return self.stageIndex not in spaceEntity.completeSpaceStages

class SECondition7( SEConditionBase ):
	"""
	副本当前阶段进行时间大于/小于多少秒
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.time = int( section["param1"] )
		self.operator = int( section["param2"] )
	
	def check( self, spaceEntity, eventParams ):
		if self.operator == 1:
			return time.time() - spaceEntity.stageStartTime > self.time
		elif self.operator == 2:
			return time.time() - spaceEntity.stageStartTime < self.time
		return False

class SECondition8( SEConditionBase ):
	"""
	某timer到达
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.timerKey = section["param1"]
	
	def check( self, spaceEntity, eventParams ):
		return eventParams["timerKey"] == self.timerKey

class SECondition9( SEConditionBase ):
	"""
	副本收到通知事件中，判断发送者类型、发送者ID、通知ID
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.senderType = section["param1"]		# 发送者类型：AI填“AI”，镜头事件填“STORY”
		self.conditionKey = section["param3"]	# 通知ID：string类型
		self.senderID = ""
		if section["param2"]:
			self.senderID = section["param2"].split("|")		# 发送者ID：AI填发送者scriptID，镜头事件填镜头ID
	
	def check( self, spaceEntity, eventParams ):
		if self.senderType:
			if eventParams["senderType"] != self.senderType:
				return False
		
		if self.senderID:
			if eventParams["senderID"] not in self.senderID:
				return False
		
		if eventParams["conditionKey"] != self.conditionKey:
			return False
		
		return True

class SECondition10( SEConditionBase ):
	"""
	某一批怪物中的某些怪物的死亡或销毁数量达到某值
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.group = int( section["param1"] )
		self.idAndAmountDict = {}
		for tempStr in section["param2"].split( "|" ):
			id, amount = tempStr.split( ":" )
			self.idAndAmountDict[ id ] = int( amount )
	
	def check( self, spaceEntity, eventParams ):
		return spaceEntity.isGroupSomeEntityDie( self.group, self.idAndAmountDict )

class SECondition11( SEConditionBase ):
	"""
	某些批次怪全部死亡或销毁
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.groups = [ int(i) for i in section["param1"].split("|") ]
	
	def check( self, spaceEntity, eventParams ):
		return spaceEntity.isGroupEntityAllDie( self.groups )

class SECondition12( SEConditionBase ):
	"""
	所有批次怪物全部死亡或销毁
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
	
	def check( self, spaceEntity, eventParams ):
		return spaceEntity.isAllGroupEntityDie()

class SECondition13( SEConditionBase ):
	"""
	某几批怪物死亡或销毁总数量不少于某值
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.groups = [ int(i) for i in section["param1"].split("|") ]
		self.amount = int( section["param2"] )
	
	def check( self, spaceEntity, eventParams ):
		return spaceEntity.isSomeGroupEntityDie( self.groups, self.amount )

class SECondition14( SEConditionBase ):
	"""
	某怪物血量低于某个百分比
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptID = section["param1"]
		self.hpRatio = float( section["param2"] )
	
	def check( self, spaceEntity, eventParams ):
		for id in spaceEntity.getEntityRecord( self.scriptID ):
			entity = KBEngine.entities.get( id )
			if entity:
				return float( entity.HP )/entity.HP_Max < self.hpRatio
		return False

class SECondition15( SEConditionBase ):
	"""
	位面玩家对某任务的进行状态是否处于指定的任务状态列表中
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.questID = int(section["param1"])										#任务ID
		self.questStatusList = [ int(i) for i in section["param2"].split("|") ]		#任务状态列表
		self.taskIDList = []
		if section["param3"]:
			self.taskIDList = [ int(i) for i in section["param3"].split("|") ]			#任务目标ID列表
		self.taskStatusList = []
		if section["param4"]:
			self.taskStatusList = [ int(i) for i in section["param4"].split("|") ]		#任务目标状态列表
	
	def check( self, spaceEntity, eventParams ):
		if len(spaceEntity._spaceRoles) == 0:
			return False
		roleEntity = spaceEntity._spaceRoles[0]
		if roleEntity.queryQuestStatus( self.questID ) not in self.questStatusList:
			return False
		
		if len( self.taskIDList ) != 0:		#填了任务目标则还要判断任务目标状态
			for index, taskId in enumerate( self.taskIDList ):
				status = self.taskStatusList[ index ]
				if roleEntity.queryTaskStatus( self.questID, taskId ) != status:
					return False
		return True

class SECondition16( SEConditionBase ):
	"""
	触发者（必须是玩家）对某任务的进行状态是否处于指定的任务状态列表中
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.questID = int(section["param1"])										#任务ID
		self.questStatusList = [ int(i) for i in section["param2"].split("|") ]		#任务状态列表
		self.taskIDList = []
		if section["param3"]:
			self.taskIDList = [ int(i) for i in section["param3"].split("|") ]			#任务目标ID列表
		self.taskStatusList = []
		if section["param4"]:
			self.taskStatusList = [ int(i) for i in section["param4"].split("|") ]		#任务目标状态列表
	
	def check( self, entity, eventParams ):
		if entity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		if entity.queryQuestStatus( self.questID ) not in self.questStatusList:
			return False
		
		if len( self.taskIDList ) != 0:		#填了任务目标则还要判断任务目标状态
			for index, taskId in enumerate( self.taskIDList ):
				status = self.taskStatusList[ index ]
				if entity.queryTaskStatus( self.questID, taskId ) != status:
					return False
		return True

class SECondition17( SEConditionBase ):
	"""
	触发者属于某批次
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.group = int( section["param1"] )
	
	def check( self, entity, eventParams ):
		return hasattr( entity, "group" ) and entity.group == self.group

class SECondition18( SEConditionBase ):
	"""
	玩家进入(或者离开)某范围事件中，判断是否进入某范围
	这种由客户端检测的条件，服务器端也必须有这个条件脚本，内部直接pass
	"""
	def __init__( self, dataDict = {} ):
		SEConditionBase.__init__( self, dataDict )
		self.isClientCon = True

class SECondition19( SEConditionBase ):
	"""
	计数改变事件中，判断是某计数改变，并且满足数量关系
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.countKey = section["param1"]
		self.value = int( section["param2"] )
		self.relationFlags = [ int(i) for i in section["param3"].split("|") ]		#满足一个即可
	
	def check( self, entity, eventParams ):
		if eventParams["countKey"] != self.countKey:
			return False
		
		for flag in self.relationFlags:
			if flag == 0 and eventParams["newValue"] == self.value:
				return True
			if flag == 1 and eventParams["newValue"] < self.value:
				return True
			if flag == 2 and eventParams["newValue"] > self.value:
				return True
		return False

class SECondition20( SEConditionBase ):
	"""
	触发者（必须是玩家）是否有某物品时
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self._itemID = int( section["param1"] )
	
	def check( self, entity, eventParams ):
		if entity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		itemList = entity.getItemInstsByID( self._itemID )
		if len(itemList) > 0:
			return True
		return False

class SECondition21( SEConditionBase ):
	"""
	玩家是否死亡
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )

	def check( self, entity, eventParams ):
		if entity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		if entity.isState( csdefine.ENTITY_STATE_DEAD ):
			return True
		return False

class SECondition22( SEConditionBase ):
	"""
	某些scriptID的怪物是否死亡(会记录到副本中)
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")
		self.amount = section["param2"].split("|")

	def check( self, spaceEntity, eventParams ):
		if len(self.scriptIDList) != len(self.amount):
			KBEDebug.ERROR_MSG("SECondition22 config is error")
			return	
		for scriptID in self.scriptIDList:
			idList = spaceEntity.getEntityRecord(scriptID)
			tempAmount = spaceEntity.queryTemp((scriptID + "dead"))
			if tempAmount == None:
				tempAmount = 0
			for id in idList:
				entity = KBEngine.entities.get( id )
				if entity and entity.getState() == csdefine.ENTITY_STATE_DEAD:
					tempAmount += 1
			spaceEntity.setTemp((scriptID+ "dead"),tempAmount)
		for scriptID in self.scriptIDList:
			index = self.scriptIDList.index(scriptID)
			needAmount = self.amount[index]
			if needAmount == "":
				needAmount = 1
			else:
				needAmount = int(needAmount)
			tempAmount = spaceEntity.queryTemp((scriptID + "dead"))
			if tempAmount < needAmount:
				return False
		return True

class SECondition23( SEConditionBase ):
	"""
	某些entity是否销毁
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")
		self.amount = section["param2"].split("|")

	def check( self, spaceEntity, eventParams ):
		if len(self.scriptIDList) != len(self.amount):
			KBEDebug.ERROR_MSG("SECondition23 config is error")
			return		
		for scriptID in self.scriptIDList:
			idList = spaceEntity.getEntityRecord(scriptID)
			index = self.scriptIDList.index(scriptID)
			needAmount = self.amount[index]
			if needAmount == "":
				needAmount = 1
			else:
				needAmount = int(needAmount)
			tempAmount = spaceEntity.queryTemp((scriptID + "destroy"))
			if tempAmount == None:
				tempAmount = 0
			for id in idList:
				entity = KBEngine.entities.get( id )
				if entity and entity.isDestroySelf == True:
					tempAmount += 1
					spaceEntity.setTemp((scriptID+ "destroy"),tempAmount)
			if tempAmount < needAmount:
				return False
		return True

class SECondition24( SEConditionBase ):
	"""
	是否创建了足够的欢乐鼎
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")
		self.baseCount = int(section["param2"])
		
	def check( self, spaceEntity, eventParams ):
		count += spaceEntity.queryTemp( "Round",0 )
		entitiesCount = 0
		for scriptID in self.scriptIDList:
			entitiesCount = len(spaceEntity.getEntityRecord(scriptID)) + entitiesCount
			if entitiesCount >= count:
					return True	
		return False

class SECondition25( SEConditionBase ):
	"""
	循环timer检测副本时间是否剩余n秒
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.timerKey = section["param1"]
		self.remainTime = int(section["param2"])
	
	def check( self, spaceEntity, eventParams ):
		if eventParams["timerKey"] == self.timerKey:
			_time = int(time.time() - spaceEntity.lifeStartTime) + 1
			if (spaceEntity.lifeTime + spaceEntity.dynamicTime - _time) == self.remainTime:
				return True
		return False	

class SECondition26( SEConditionBase ):
	"""
	判断副本阶段某计数改变，并且满足数量关系
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.countKey = section["param1"]
		self.value = int( section["param2"] )
		self.relationFlags = [ int(i) for i in section["param3"].split("|") ]		#满足一个即可

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		if self.countKey not in spaceEntity.spaceEventCountInt:
			return False
		for flag in self.relationFlags:
			if flag == 0 and spaceEntity.spaceEventCountInt[self.countKey] == self.value:
				return True
			if flag == 1 and spaceEntity.spaceEventCountInt[self.countKey] < self.value:
				return True
			if flag == 2 and spaceEntity.spaceEventCountInt[self.countKey] > self.value:
				return True
		return False
		
class SECondition27( SEConditionBase ):
	"""
	环任务某个副本统计数量不足某数
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.entryIndex = int( section["param1"].strip() ) - 1
		self.num = int( section["param2"] )
		
	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		num = spaceEntity.getSpaceStatisticsNum( self.entryIndex )
		return self.num > num
		
class SECondition28( SEConditionBase ):
	"""
	环任务某个副本统计数量大于等于某数
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.entryIndex = int( section["param1"].strip() ) - 1
		self.num = int( section["param2"] )
		
	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		num = spaceEntity.getSpaceStatisticsNum( self.entryIndex )
		return self.num <= num
		
class SECondition29( SEConditionBase ):
	"""
	Space临时值记录是否大于等于某数
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.tempKey = section["param1"]
		self.num = int( section["param2"] )
		
	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		value = spaceEntity.queryTemp( "cehua_" + self.tempKey, 0 )
		return value >= self.num
		
class SECondition30( SEConditionBase ):
	"""
	是否某个统计已完成
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.index = int( section["param1"] )
		
	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		return self.index == eventParams["entryIndex"]

class SECondition31( SEConditionBase ):
	"""
	副本是否不存在某个timerKey
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.timerKey = section["param1"]

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		if self.timerKey not in spaceEntity.spaceEventTimers:
			return True
		return False

class SECondition32( SEConditionBase ):
	"""
	副本当前为某阶段
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.stageIndex = int(section["param1"])

	def check( self, spaceEntity, eventParams ):
		if len(spaceEntity.completeSpaceStages) == 0: #为什么会用completeSpaceStages来判断？因为spaceEntity.spaceStage在每完成一个阶段时会变为None,为了这个条件的通用性
			return self.stageIndex == 1
		maxStageIndex = max(spaceEntity.completeSpaceStages)
		stage = spaceEntity.getScript().getStageByIndex(maxStageIndex + 1)
		if not stage:
			return False
		return self.stageIndex == (maxStageIndex + 1)

class SECondition33( SEConditionBase ):
	"""
	玩家状态改变
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.state = int(section["param1"])

	def check( self, spaceEntity, eventParams ):
		if spaceEntity.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		if spaceEntity.getState() == self.state:
			return True
		return False

class SECondition34( SEConditionBase ):
	"""
	副本是否有空画卷（CST-3790）
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")	#画卷ScriptID列表

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		for scriptID in self.scriptIDList:
			for id in spaceEntity.getEntityRecord(scriptID):
				entity = KBEngine.entities.get(id, None)
				if entity and not entity.queryTemp("attributeType", None):
					return True
		return False

class SECondition35( SEConditionBase ):
	"""
	副本分身是否全部被消灭（CST-3790）
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.pictureScrollList = section["param1"].split("|")	#画卷scriptID
		self.avatarList = section["param2"].split("|")	#分身scriptID

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		for scriptID in self.pictureScrollList:
			for id in spaceEntity.getEntityRecord(scriptID):
				entity = KBEngine.entities.get(id, None)
				if entity and entity.queryTemp("attributeType", None):
					return False
		for scriptID in self.avatarList:
			idList = spaceEntity.getEntityRecord(scriptID)
			for id in idList:
				entity = KBEngine.entities.get(id, None)
				if entity.getState() != csdefine.ENTITY_STATE_DEAD:
					return False
		return True

class SECondition36( SEConditionBase ):
	"""
	副本某些怪物数量满足某个数量
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDs = list(set(section["param1"].split("|")))	#scriptID
		self.amount = int(section["param2"])	#数量
		self.relationFlags = [ int(i) for i in section["param3"].split("|") ]		#满足一个即可

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		count=0
		for scriptID in self.scriptIDs:
			count+=len(spaceEntity.getEntityRecord(scriptID))

		for flag in self.relationFlags:
			if flag == 0 and  count == self.amount:
				return True
			if flag == 1 and count < self.amount:
				return True
			if flag == 2 and count > self.amount:
				return True
		return False

class SECondition37( SEConditionBase ):
	"""
	副本某scriptID怪的某buffID的buff数量达到某个值
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self._scriptID = section["param1"]		#scriptID
		self._buffID = int(section["param2"])	#buffID
		self._amount = int(section["param3"])	#数量

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False

		amount = 0
		entityIDList = spaceEntity.getEntityRecord(self._scriptID)
		for entityID in entityIDList:
			_entity = KBEngine.entities.get(entityID, None)
			if _entity:
				buffs = _entity.findBuffsByBuffID( self._buffID )
				amount += len(buffs)

		return amount == self._amount

class SECondition38( SEConditionBase ):
	"""
	判断触发者是否有某Buff
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self._buffID = [ int(i) for i in section["param1"].split("|") ]		#buffID

	def check( self, entity, eventParams ):
		if not entity:
			return False

		amount = 0
		for buffID in self._buffID:
			buffs = entity.findBuffsByBuffID( buffID )
			amount += len(buffs)

		return amount == len(self._buffID)

class SECondition39( SEConditionBase ):
	"""
	判断触发者是否没某Buff
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self._buffID = [ int(i) for i in section["param1"].split("|") ]		#buffID

	def check( self, entity, eventParams ):
		if not entity:
			return False

		amount = 0
		for buffID in self._buffID:
			buffs = entity.findBuffsByBuffID( buffID )
			amount += len(buffs)

		return amount == 0
		
class SECondition40( SEConditionBase ):
	"""
	entity销毁总数达到某个值
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")
		self.amount = int(section["param2"])

	def check( self, spaceEntity, eventParams ):
		totalAmount = 0
		for scriptID in self.scriptIDList:
			idList = spaceEntity.getEntityRecord(scriptID)
			index = self.scriptIDList.index(scriptID)
			tempAmount = spaceEntity.queryTemp((scriptID + "destroy"))
			if tempAmount == None:
				tempAmount = 0
			for id in idList:
				entity = KBEngine.entities.get( id )
				if entity and entity.isDestroySelf == True:
					tempAmount += 1
					spaceEntity.setTemp((scriptID+ "destroy"),tempAmount)
			totalAmount += tempAmount
		if totalAmount < self.amount:
			return False
		return True

class SECondition41( SEConditionBase ):
	"""
	判断触发者（玩家）是否移除或增加某物品
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.itemID = int(section["param1"])

	def check( self, entity, eventParams ):
		return self.itemID == eventParams["itemID"]

class SECondition42( SEConditionBase ):
	"""
	判断触发者（玩家） 是否没有该物品
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.itemID = int(section["param1"])

	def check( self, entity, eventParams ):
		itemList = entity.getItemInstsByID( self.itemID )
		if len(itemList) <= 0:
			return True
		return False

class SECondition43( SEConditionBase ):
	"""
	某阶段下的某阶段目标已完成
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.stageIndex = int(section["param1"]) 	#阶段ID
		self.taskIndexList = [int(i) for i in section["param2"].split("|") ] #阶段目标ID；支持多个，以（|）竖号分隔，表示“且”的关系。

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity.spaceStage:
			return False

		if spaceEntity.spaceStage.stageIndex != self.stageIndex:
			return False

		for taskIndex in self.taskIndexList:
			task = spaceEntity.spaceStage.getTaskByTaskIndex(taskIndex)
			if not task or not task.isCompleted():
				return False
		return True

class SECondition44( SEConditionBase ):
	"""
	副本是否存在某个timerKey
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.timerKey = section["param1"]

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		if self.timerKey in spaceEntity.spaceEventTimers:
			return True
		return False

class SECondition45( SEConditionBase ):
	"""
	环任务晶石洞窟统计数量大于等于某数
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		
	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		if spaceEntity.crystalCount1 <= spaceEntity.redCounts and spaceEntity.crystalCount2 <= spaceEntity.yellowCounts and spaceEntity.crystalCount3 <= spaceEntity.blueCounts:
			return True
		return False

class SECondition46( SEConditionBase ):
	"""
	环任务晶石洞窟统计数量小于等于某数
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		
	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		if spaceEntity.crystalCount1 > spaceEntity.redCounts or spaceEntity.crystalCount2 > spaceEntity.yellowCounts or spaceEntity.crystalCount3 > spaceEntity.blueCounts:
			return True
		return False

class SECondition47( SEConditionBase ):
	"""
	触发者血量高于某个百分并且比于低于某个百分比
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.param1 = float( section["param1"] )
		self.param2 = float( section["param2"] )
	
	def check( self, entity, eventParams ):
		return self.param1 < float( entity.HP )/entity.HP_Max < self.param2

class SECondition48( SEConditionBase ):
	"""
	触发者血量每减少某个百分比
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.param1 = float( section["param1"] )
		self.beforeHP = 0
	
	def check( self, entity, eventParams ):
		if  self.beforeHP < int ((entity.HP_Max - entity.HP ) / (self.param1 * entity.HP_Max)):
			self.beforeHP =  int ((entity.HP_Max - entity.HP ) / (self.param1 * entity.HP_Max))	
			return True
		else:
			self.beforeHP =  int ((entity.HP_Max - entity.HP ) / (self.param1 * entity.HP_Max))	
			return False

class SECondition49( SEConditionBase ):
	"""
	触发者血量满足某个百分比关系(大于、小于、等于、大于等于、小于等于)
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.hpPercent = float( section["param1"] )
		self.relationFlags = int(section["param2"])

	def check( self, entity, eventParams ):
		hp = math.ceil( entity.HP_Max * self.hpPercent )
		if self.relationFlags == 1 and entity.HP > hp:
			return True
		elif self.relationFlags == 2 and entity.HP < hp:
			return True
		elif self.relationFlags == 3 and entity.HP == hp:
			return True
		elif self.relationFlags == 4 and entity.HP >= hp:
			return True
		elif self.relationFlags == 5 and entity.HP <= hp:
			return True
		return False	

class SECondition52( SEConditionBase ):
	"""
	CST-7699 判断某语音是否播放结束
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.soundID = section["param1"]
		
	def check( self, entity, eventParams ):
		soundID = eventParams["soundID"]
		return soundID == self.soundID

class SECondition53( SEConditionBase ):
	"""
	某些scriptID的怪物是否存在(不存在则条件通过)
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")

	def check( self, spaceEntity, eventParams ):
		for scriptID in self.scriptIDList:
			idList = spaceEntity.getEntityRecord(scriptID)
			if len(idList) > 0:
				return False
		return True

class SECondition54( SEConditionBase ):
	"""
	某些scriptID的怪物是否存在(存在则条件通过)
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.scriptIDList = section["param1"].split("|")

	def check( self, spaceEntity, eventParams ):
		for scriptID in self.scriptIDList:
			idList = spaceEntity.getEntityRecord(scriptID)
			if len(idList) > 0:
				return True
		return False

class SECondition55( SEConditionBase ):
	"""
	概率条件
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.number = int(float(section["param1"])*10000) if section["param1"] else 0

	def check( self, spaceEntity, eventParams ):
		randomNumber = random.randint(0, 10000)
		if self.number <= randomNumber:
			return True
		return False
		
class SECondition59( SEConditionBase ):
	"""
	判断副本通关时间是否满足某个条件
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.time = int(section["param1"]) * 60
		self.mark = section["param2"]

	def check( self, spaceEntity, eventParams ):
		if not self.mark:
			KBEDebug.ERROR_MSG("mark is None")
			return False
		
		lifeTime = int( spaceEntity.lifeStopTime - spaceEntity.lifeStartTime ) + spaceEntity.dynamicTime
		if self.mark == "1":
			return lifeTime > self.time
		elif self.mark == "2":
			return lifeTime < self.time
		elif self.mark == "3":
			return lifeTime == self.time
		elif self.mark == "4":
			return lifeTime >= self.time
		elif self.mark == "5":
			return lifeTime <= self.time
		else:
			KBEDebug.ERROR_MSG("mark[%s] error" %(self.mark))
			return False

class SECondition60( SEConditionBase ):
	"""
	判断副本计数key1与key2的数量关系
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.countKey1 = section["param1"]
		self.countKey2 = section["param2"]
		self.relationFlags = [ int(i) for i in section["param3"].split("|") ]		#满足一个即可

	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		if not(self.countKey1 in spaceEntity.spaceEventCountInt and self.countKey2 in spaceEntity.spaceEventCountInt):
			return False
		for flag in self.relationFlags:
			if flag == 0 and spaceEntity.spaceEventCountInt[self.countKey1] == spaceEntity.spaceEventCountInt[self.countKey2]:
				return True
			if flag == 1 and spaceEntity.spaceEventCountInt[self.countKey1] < spaceEntity.spaceEventCountInt[self.countKey2]:
				return True
			if flag == 2 and spaceEntity.spaceEventCountInt[self.countKey1] > spaceEntity.spaceEventCountInt[self.countKey2]:
				return True
		return False
		
class SECondition61( SEConditionBase ):
	"""
	判断经验副本层数
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.bunchStage = int(section["param1"])
		
	def check( self, entity, eventParams ):
		if not entity:
			return False
			
		spaceEntity = entity.getCurrentSpace()
		if not spaceEntity or not spaceEntity.getScript().getBunchSpaceObj():
			return False
		
		return spaceEntity.bunchStage == self.bunchStage
		
class SECondition62( SEConditionBase ):
	"""
	判断洞府 是否开启活动(1：掠夺战，2：争夺战)
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.activeType = int(section["param1"])
		
	def check( self, entity, eventParams ):
		if KBEngine.globalData.get( "LHMJ_PlunderActive", 0 ) and self.activeType == 1:
			return True
		elif KBEngine.globalData.get("LHMJ_ChallengeActive", 0) and self.activeType == 2:
			return True
		elif self.activeType == 0:
			return True
		
		return False
		
class SECondition63( SEConditionBase ):
	"""
	判断玩家 攻守方（0：攻方，1：守方）
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.belongSide = int(section["param1"])
		
	def check( self, entity, eventParams ):
		if "playerID" in eventParams:
			player = KBEngine.entities.get( eventParams["playerID"] )
			if player:
				return player.isBelongSide( self.belongSide )
		return False
		
class SECondition64( SEConditionBase ):
	"""
	副本火炮都被摧毁了
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
				
	def check( self, entity, eventParams ):
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
			return len(spaceEntity.batteryScriptIDList) <= 1					# 因为ai取消注册，要比剧情慢？
		return False
		
class SECondition66( SEConditionBase ):
	"""
	洞府建筑是否被摧毁
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.isDestroy = int(section["param1"])
		
	def check( self, entity, eventParams ):
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity and spaceEntity.getScript().getSpaceType() == csdefine.SPACE_TYPE_DONG_FU:
			if self.isDestroy and len(spaceEntity.isDestroyBuild) > 0:
				return True
			if not self.isDestroy and len( spaceEntity.isDestroyBuild) == 0:
				return True
		return False

class SECondition68( SEConditionBase ):
	"""
	判断副本内玩家人数是否满足某个数量关系
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.relationFlags = [ int(i) for i in section["param1"].split("|") ]		#满足一个即可
		self.value = int( section["param2"] )
	
	def check( self, spaceEntity, eventParams ):
		if not spaceEntity:
			return False
		roleAmount = len(spaceEntity._spaceRoles)
		for flag in self.relationFlags:
			if flag == 0 and roleAmount == self.value:
				return True
			if flag == 1 and roleAmount < self.value:
				return True
			if flag == 2 and roleAmount > self.value:
				return True
		return False
				
class SECondition69( SEConditionBase ):
	"""
	判断副本是否有某个临时标记(entity触发)
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.key = section["param1"]
		self.value = section["param2"]
		
	def check( self, entity, eventParams ):
		spaceEntity = entity.getCurrentSpace()
		if spaceEntity and spaceEntity.queryTemp("SPACE_{}".format(self.key)) == self.value:
			return True
		return False
		
class SECondition70( SEConditionBase ):
	"""
	判断副本是否有某个临时标记(space事件触发)
	"""
	def init( self, section ):
		SEConditionBase.init( self, section )
		self.key = section["param1"]
		self.value = section["param2"]
		
	def check( self, spaceEntity, eventParams ):
		if spaceEntity and spaceEntity.queryTemp("SPACE_{}".format(self.key)) == self.value:
			return True
		return False


class SECondition71(SEConditionBase):
	"""
	金枝玉庭副本获取到的金币数量小于初档
	"""

	def init(self, section):
		SEConditionBase.init(self, section)

	def check(self, spaceEntity, eventParams):
		if not spaceEntity:
			return False
		if spaceEntity.integralToolAmount < spaceEntity.getScript().goldNumAboutGrade[1]:
			return True
		return False

class SECondition72(SEConditionBase):
	"""
	金枝玉庭副本获取到的金币数量大于或等于初档
	"""

	def init(self, section):
		SEConditionBase.init(self, section)

	def check(self, spaceEntity, eventParams):
		if not spaceEntity:
			return False
		if spaceEntity.integralToolAmount >= spaceEntity.getScript().goldNumAboutGrade[1]:
			return True
		return False
		
class SECondition73(SEConditionBase):
	"""
	帮会掠夺 判断玩家是否已经获得过器械兑换券
	"""
	def init(self, section):
		SEConditionBase.init(self, section)

	def check(self, spaceEntity, eventParams):
		if not spaceEntity:
			return False
		if "playerID" not in eventParams:
			return False
		player = KBEngine.entities.get( eventParams["playerID"] )
		if not player:
			return False
		if player.playerDBID in spaceEntity.getVoucherRecord:
			return False
		return True
	
	
SEConditionBase.setConditionClass("SECondition1", SECondition1)
SEConditionBase.setConditionClass("SECondition2", SECondition2)
SEConditionBase.setConditionClass("SECondition3", SECondition3)
SEConditionBase.setConditionClass("SECondition4", SECondition4)
SEConditionBase.setConditionClass("SECondition5", SECondition5)
SEConditionBase.setConditionClass("SECondition6", SECondition6)
SEConditionBase.setConditionClass("SECondition7", SECondition7)
SEConditionBase.setConditionClass("SECondition8", SECondition8)
SEConditionBase.setConditionClass("SECondition9", SECondition9)
SEConditionBase.setConditionClass("SECondition10", SECondition10)
SEConditionBase.setConditionClass("SECondition11", SECondition11)
SEConditionBase.setConditionClass("SECondition12", SECondition12)
SEConditionBase.setConditionClass("SECondition13", SECondition13)
SEConditionBase.setConditionClass("SECondition14", SECondition14)
SEConditionBase.setConditionClass("SECondition15", SECondition15)
SEConditionBase.setConditionClass("SECondition16", SECondition16)
SEConditionBase.setConditionClass("SECondition17", SECondition17)
SEConditionBase.setConditionClass("SECondition18", SECondition18)
SEConditionBase.setConditionClass("SECondition19", SECondition19)
SEConditionBase.setConditionClass("SECondition20", SECondition20)
SEConditionBase.setConditionClass("SECondition21", SECondition21)
SEConditionBase.setConditionClass("SECondition22", SECondition22)
SEConditionBase.setConditionClass("SECondition23", SECondition23)
SEConditionBase.setConditionClass("SECondition24", SECondition24)
SEConditionBase.setConditionClass("SECondition25", SECondition25)
SEConditionBase.setConditionClass("SECondition26", SECondition26)
SEConditionBase.setConditionClass("SECondition27", SECondition27)
SEConditionBase.setConditionClass("SECondition28", SECondition28)
SEConditionBase.setConditionClass("SECondition29", SECondition29)
SEConditionBase.setConditionClass("SECondition30", SECondition30)
SEConditionBase.setConditionClass("SECondition31", SECondition31)
SEConditionBase.setConditionClass("SECondition32", SECondition32)
SEConditionBase.setConditionClass("SECondition33", SECondition33)
SEConditionBase.setConditionClass("SECondition34", SECondition34)
SEConditionBase.setConditionClass("SECondition35", SECondition35)
SEConditionBase.setConditionClass("SECondition36", SECondition36)
SEConditionBase.setConditionClass("SECondition37", SECondition37)
SEConditionBase.setConditionClass("SECondition38", SECondition38)
SEConditionBase.setConditionClass("SECondition39", SECondition39)
SEConditionBase.setConditionClass("SECondition40", SECondition40)
SEConditionBase.setConditionClass("SECondition41", SECondition41)
SEConditionBase.setConditionClass("SECondition42", SECondition42)
SEConditionBase.setConditionClass("SECondition43", SECondition43)
SEConditionBase.setConditionClass("SECondition44", SECondition44)
SEConditionBase.setConditionClass("SECondition45", SECondition45)
SEConditionBase.setConditionClass("SECondition46", SECondition46)
SEConditionBase.setConditionClass("SECondition47", SECondition47)
SEConditionBase.setConditionClass("SECondition48", SECondition48)
SEConditionBase.setConditionClass("SECondition49", SECondition49)
SEConditionBase.setConditionClass("SECondition52", SECondition52)
SEConditionBase.setConditionClass("SECondition53", SECondition53)
SEConditionBase.setConditionClass("SECondition54", SECondition54)
SEConditionBase.setConditionClass("SECondition55", SECondition55)
SEConditionBase.setConditionClass("SECondition59", SECondition59)
SEConditionBase.setConditionClass("SECondition60", SECondition60)
SEConditionBase.setConditionClass("SECondition61", SECondition61)
SEConditionBase.setConditionClass("SECondition62", SECondition62)
SEConditionBase.setConditionClass("SECondition63", SECondition63)
SEConditionBase.setConditionClass("SECondition64", SECondition64)
SEConditionBase.setConditionClass("SECondition66", SECondition66)
SEConditionBase.setConditionClass("SECondition68", SECondition68)
SEConditionBase.setConditionClass("SECondition69", SECondition69)
SEConditionBase.setConditionClass("SECondition70", SECondition70)
SEConditionBase.setConditionClass("SECondition71", SECondition71)
SEConditionBase.setConditionClass("SECondition72", SECondition72)
SEConditionBase.setConditionClass("SECondition73", SECondition73)