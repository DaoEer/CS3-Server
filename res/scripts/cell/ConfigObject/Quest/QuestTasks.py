# -*- coding: utf-8 -*-
#

import ItemTypeEnum
import QuestEventDefine
from ConfigObject.Quest.QuestBase.QuestTask import QuestTask
import Quest.QuestConfigs.WhisperQuestConfig as WhisperQuestConfig
import KBEDebug
import random
import time
import Functions

# ----------------------------------------------------------
# 任务目标类型扩展 继承父类QuestTask
# ----------------------------------------------------------
class QuestTaskKillMonster( QuestTask ):
	"""击杀怪物(可支持配置多种怪物)"""

	quest_event = [ QuestEventDefine.EVENT_MONSTER_DIE ]

	def __init__(self):
		QuestTask.__init__(self)
		self._killTarget = []

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		params = data["param1"].split("|")
		for i in params:
			if i != "":
				self._killTarget.append(int(i))

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and (int(param) in self._killTarget):
			self._progress += 1
			return True
		else:
			return False

class QuestTaskGetItem( QuestTask ):
	"""获取物品"""

	quest_event = [ QuestEventDefine.EVENT_GET_ITEM, QuestEventDefine.EVENT_REMOVE_ITEM ]

	def __init__(self):
		QuestTask.__init__(self)
		self._getItemID = None

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._getItemID = int(data["param1"])
		
	def refreshProgress( self, player ):
		if self.isDone():return False
		itemList = player.getItemInstsByID( self._getItemID )
		for item in itemList:
			self._progress +=  item.getAmount()
			return True
		return False

	def updateProgress(self, player, eventID, param):
		itemdID, itemAmount = param
		if eventID == QuestEventDefine.EVENT_GET_ITEM:
			if self._getItemID == itemdID:
				self._progress += itemAmount
				return True
		elif eventID == QuestEventDefine.EVENT_REMOVE_ITEM:
			if self._getItemID == itemdID:
				self._progress += itemAmount
				self._progress = max( self._progress, 0 )
				return True
		return False

class QuestTaskCommitItem( QuestTask ):
	"""物品提交达成任务目标"""

	quest_event = [ QuestEventDefine.EVENT_COMMIT_ITEM ]

	def __init__(self):
		QuestTask.__init__(self)
		self._commitItemID = None

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._commitItemID = int(data["param1"])

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and self._commitItemID == param:
			self._progress += 1
			return True
		else:
			return False

class QuestUseCommitItem( QuestTask ):
	"""使用物品达成任务目标"""

	quest_event = [ QuestEventDefine.EVENT_USE_ITEM ]
	def __init__(self):
		QuestTask.__init__(self)
		self._useItemID = None

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._useItemID = int(data["param1"])

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and self._useItemID == param:
			self._progress += 1
			return True
		else:
			return False

class QuestRemoveUseItem( QuestTask ):
	"""因使用而移除物品时达成任务目标"""

	quest_event = [ QuestEventDefine.EVENT_REMOVE_ITEM_ON_USE ]
	def __init__(self):
		QuestTask.__init__(self)
		self._useItemID = None

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._useItemID = int(data["param1"])

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and self._useItemID == param:
			self._progress += 1
			return True
		else:
			return False

class QuestTaskLearnSkill( QuestTask ):
	"""学习技能"""

	quest_event = [ QuestEventDefine.EVENT_LEARN_SKILL ]

	def __init__(self):
		QuestTask.__init__(self)
		self._skillID = None
		
	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._skillID = int(data["param1"])
		
	def refreshProgress( self, player ):
		if not self.isDone():
			#
			preSkill = int(self._skillID / 1000)
			for id in player.attrSkills:
				if int(id / 1000) == preSkill:
					# 有可能，玩家身上的技能等级小于任务目标的
					if id % 100 >= self._skillID % 100:
						self._progress += 1
						return True
		return False

	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			if self._skillID == param:
				self._progress += 1
				return True
			else:
				return False
		else:
			return False

class QuestTaskGetTo( QuestTask ):
	"""到达某地"""

	quest_event = [ QuestEventDefine.EVENT_GET_TO ]

	def __init__(self):
		QuestTask.__init__(self)

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and self.id == int(param):
			self._progress += 1
			return True
		else:
			return False

class QuestTaskXiuweiLevel( QuestTask ):
	"""达到修为层次"""

	quest_event = [ QuestEventDefine.EVENT_XIUWEI_LEVEL ]

	def __init__(self):
		QuestTask.__init__(self)
		self._xiuweiLevel = 1

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._xiuweiLevel = int(data["param1"])
		
	def refreshProgress( self, player ):
		if not self.isDone() and player.xiuweiLevel >= self._xiuweiLevel:
			self._progress += 1
			return True
		return False

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and self._xiuweiLevel <= param:
			self._progress += 1
			return True
		else:
			return False

class QuestTaskEventTrigger( QuestTask ):
	"""触发类任务目标"""

	quest_event = [ QuestEventDefine.EVENT_EVENT_TRIGGER ]

	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			self._progress += 1
			return True
		else:
			return False
			
class QuestTaskEnterPotentialCopy( QuestTask ):
	"""进入潜能副本"""

	quest_event = [ QuestEventDefine.EVENT_ENTER_POTENTIAL_COPY ]

	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			self._progress += 1
			return True
		else:
			return False

class QuestTaskEnterChuanChengCopy( QuestTask ):
	"""进入传承副本"""

	quest_event = [ QuestEventDefine.EVENT_ENTER_CHUAN_CHENG_COPY ]

	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			self._progress += 1
			return True
		else:
			return False
			
class QuestTaskUseSkill( QuestTask ):
	"""使用技能"""

	quest_event = [ QuestEventDefine.EVENT_USE_SKILL ]

	def __init__(self):
		QuestTask.__init__(self)
		self._skillID = None
		self._scriptID = 0

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._skillID = int(data["param1"])
		self._scriptID = int(data["param2"]) if data["param2"] else 0

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and self._skillID == param[0]:
			if not self._scriptID or self._scriptID == param[1]:
				self._progress += 1
				return True
		else:
			return False
			
class QuestTaskConjurePet( QuestTask ):
	"""某幻兽出战"""
	quest_event =  [ QuestEventDefine.EVENT_CONJURE_PET ]

	def __init__(self):
		QuestTask.__init__(self)
		self._scriptID = ""

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		if data["param1"]:
			self._scriptID = data["param1"]

	def updateProgress(self, player, eventID, param):
		if self._progress >= self._goal:
			return False
		if self._scriptID:
			if self._scriptID == param[0]:
				self._progress += 1
				return True
		else:
			self._progress += 1
			return True
		return False
		
class QuestTaskMountPet( QuestTask ):
	"""骑宠状态"""
	quest_event = [ QuestEventDefine.EVENT_MOUNT_PET ]

	def __init__(self):
		QuestTask.__init__(self)
		self._scriptID = ""

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		if data["param1"]:
			self._scriptID = data["param1"]

	def updateProgress(self, player, eventID, param):
		if self._progress >= self._goal:
			return False
		if self._scriptID:
			if self._scriptID == param[0]:
				self._progress += 1
				return True
		else:
			self._progress += 1
			return True
		return False
#------------------------环任务 任务目标----------------------------------------------
class QuestTaskGuessGame( QuestTask ):
	"""猜大小"""
	quest_event = [ QuestEventDefine.EVENT_GUESS_GAME ]
	
	def updateProgress(self, player, eventID, param):
		if self._progress < self._goal:
			self._progress += 1
			return True
		return False
		
class QuestTaskHuanComonEventTrigger( QuestTask ):
	"""环任务与NPC交互通用事件"""

	quest_event = [ QuestEventDefine.EVENT_HUAN_COMMON_TASK ]

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		if data["param1"]:
			self._scriptID = data["param1"]

	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			if self._scriptID == param[0]:
				self._progress += 1
				return True
		else:
			return False
		return False

class QuestTaskTalkWithNPC( QuestTask ):
	"""与NPC对话"""
	quest_event = [ QuestEventDefine.EVENT_TALK_WITH_NPC ]

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._scriptID = int(data["param1"].strip())

	def updateProgress(self, player, eventID, param):	
		if self.isDone():return False
		if self._scriptID == int(param):
			self._progress += 1
			return True
	
		return False

class QuestTaskPlayerLevel( QuestTask ):
	"""满足等级"""
	quest_event = [ QuestEventDefine.EVENT_PLAYER_LEVEL ]

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self._playerLevel = int(data["param1"])

	def refreshProgress( self, player ):
		if not self.isDone() and player.level >= self._playerLevel:
			self._progress += 1
			return True
		return False

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and self._playerLevel <= param:
			self._progress += 1
			return True
		else:
			return False

class QuestTaskPlayerrAnswer( QuestTask ):
	"""玩家答题"""
	quest_event = [ QuestEventDefine.EVENT_ANSWER_QUESTION ]
	
	def updateProgress(self, player, eventID, param):
		if self._progress < self._goal:
			self._progress += 1
			return True
		return False

class QuestTaskJSZZFirstStage( QuestTask ):
	"""
	金树种子第一阶段
	"""
	quest_event =  [ QuestEventDefine.EVENT_GET_TO ]

	def __init__(self):
		QuestTask.__init__(self)
		self.spaceScriptID = ""
		self.number = 0
		self.pos = ""
		self.radius = 0.0
		self.startTime = 0.0 # 暂时写定

	def initFromStream(self, data):
		QuestTask.initFromStream( self, data )
		if self.param.get("number",None) != None:
			self.number = self.param["number"]
		if self.param.get("spaceScriptID",None) != None:
			self.spaceScriptID = self.param["spaceScriptID"]
		if self.param.get("pos","") != "":
			self.pos = self.param["pos"]
		if self.param.get("radius",None) != None:
			self.radius = self.param["radius"]
		if self.param.get( "startTime",None ) != None:
			self.startTime = self.param["startTime"]

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		spaceScriptIDs = [i for i in data["param1"].split("|")]
		self.spaceScriptID = random.choice( spaceScriptIDs )
		index = spaceScriptIDs.index( self.spaceScriptID )
		self.radius = float(data["param2"].split(":")[1])
		posStrList = (data["param2"].split(":")[0]).split("|") #每个地图所有中点坐标
		posStr = posStrList[index]
		centerStrList = posStr.split(";") #该地图的所有中点坐标
		centerIndex = random.choice(list(range(len(centerStrList))))
		centerPosStr = centerStrList[centerIndex]
		self.pos = centerPosStr
		areaNumberStrList = data["param3"].split("|") #每个地图所有区域编号
		areaNumberStr = areaNumberStrList[index]
		numberStrList = areaNumberStr.split(";") #该地图所有区域的编号 MonsterScriptID
		self.number = numberStrList[centerIndex]
		self.setTempData("number",self.number)
		self.setTempData("spaceScriptID", self.spaceScriptID )
		self.setTempData("pos",self.pos)
		self.setTempData("radius",self.radius)
		self.startTime = time.time()
		self.setTempData("startTime",self.startTime)

	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			self._progress += 1
			return True
		else:
			return False

class QuestTaskJSZZSecondStage( QuestTask ):
	"""
	金树种子第二阶段
	"""
	quest_event =  [ QuestEventDefine.EVENT_EVENT_TRIGGER ]

	def __init__(self):
		QuestTask.__init__(self)
		self.data = {}
		self.plantCenterPos = None #种植中心点
		self.plantRadius = 0.0 #种植的半径
		self.spaceScriptID = ""
		self.number = -1
		self.searchSkillID = 0

	def setPlantData( self, spaceScriptID, number ):
		"""
		设置种植的数据
		"""
		self.spaceScriptID = spaceScriptID
		self.number = number
		if self.plantCenterPos != None and self.plantRadius != 0.0:
			return
		spaceScriptIDs = (self.data["param1"].split(":")[0]).split("|")   # 地图spaceScriptID|地图spaceScriptID.....
		if self.spaceScriptID not in spaceScriptIDs:
			KBEDebug.ERROR_MSG("QuestTaskJSZZSecondStage spaceScriptID = %s not in param1"%(self.spaceScriptID)  )
			return
		index = spaceScriptIDs.index(self.spaceScriptID)
		areaNumberStrList = self.data["param2"].split("|") #所有地图的编号 # 编号1;编号2;...|编号1;编号2;.....
		numberStrList = areaNumberStrList[index]
		numberList = numberStrList.split(";")
		if self.number not in numberList:
			KBEDebug.ERROR_MSG(" QuestTaskJSZZSecondStage param2 index = %i  number = %i not in param2[index] "%( index, self.number ))
			return
		numberIndex = numberList.index( self.number )
		allPlantStrList = self.data["param3"].split("|")  # 所有种植点 pos:半径,pos:半径,...;pos:半径,pos:半径,..;....|pos:半径,pos:半径,...;pos:半径,pos:半径,..;....
		mapPlantDataStr = allPlantStrList[index]
		mapPlantCenterPosStrList = mapPlantDataStr.split(";")
		plantCenterPosDataStr = mapPlantCenterPosStrList[numberIndex]
		plantCenterPosStrList = plantCenterPosDataStr.split(",")
		plantCenterPosStr = random.choice( plantCenterPosStrList )
		self.plantCenterPos = Functions.vector3TypeConvert(plantCenterPosStr.split(":")[0])
		self.plantRadius = float( plantCenterPosStr.split(":")[1] )
		self.setTempData("plantCenterPos",self.plantCenterPos)
		self.setTempData("plantRadius",self.plantRadius)

	def initFromStream(self, data):
		QuestTask.initFromStream( self, data )
		if self.param.get("plantCenterPos",None) != None:
			self.plantCenterPos = self.param["plantCenterPos"]
		if self.param.get("plantRadius",None) != None:
			self.plantRadius = self.param["plantRadius"]

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self.data = data
		self.searchSkillID = int(data["param1"].split(":")[1])
		self.plantSkillID = int(data["param1"].split(":")[2])

	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			self._progress += 1
			return True
		else:
			return False

class QuestTaskJSZZThirdStage( QuestTask ):
	"""
	金树种子第三阶段
	"""
	quest_event =  [ QuestEventDefine.EVENT_EVENT_TRIGGER ]

	def __init__(self):
		QuestTask.__init__(self)
		self.data = {}
		self.planeScriptID = ""
		self.planeRadius = 0.0

	def setPlaneData( self, spaceScriptID ):
		"""
		进入位面的数据
		"""
		spaceScriptIDs = self.data["param1"].split("|")
		if spaceScriptID not in spaceScriptIDs:
			KBEDebug.ERROR_MSG("QuestTaskJSZZThirdStage spaceScriptID = %s not in param1"%(spaceScriptID)  )
			return
		index = spaceScriptIDs.index( spaceScriptID )
		planeScriptIDs = self.data["param2"].split("|")
		self.planeScriptID = planeScriptIDs[index]

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self.data = data
		self.planeRadius = float(data["param3"])

	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			self._progress += 1
			return True
		else:
			return False

class QuestTaskPlayerTitle( QuestTask ):
	"""玩家使用某称号"""

	quest_event = [ QuestEventDefine.EVENT_EVENT_TRIGGER ]

	def __init__(self):
		QuestTask.__init__(self)
		self.titleID = 0

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self.titleID = int(data["param1"])

	def updateProgress(self, player, eventID, param):
		if not self.isDone() and self.titleID == player.title:
			self._progress += 1
			return True
		else:
			return False

class QuestTaskTalkWithWhisper( QuestTask ):
	"""与传话任务NPC对话"""

	quest_event = [ QuestEventDefine.EVENT_TALK_WITH_NPC ]

	def __init__(self):
		QuestTask.__init__(self)

	def resetProgress(self, player):
		"""任务目标重置"""
		self._progress = 0
		self.setTempData("isComplete", 0)

	def isDone(self):
		""""""
		if self.getTempData("isComplete"):
			return True
		return self._goal != 0 and self._progress >= self._goal

	def setDone(self):
		"""设置为完成状态"""
		self.setTempData("isComplete", 1)

	def initFromConfig(self, data):
		QuestTask.initFromConfig(self, data)
		self.rootQuestID = int(data["param1"])

	def updateProgress(self, player, eventID, param):
		if self.isDone():return False
		datas = WhisperQuestConfig.Datas
		if self.rootQuestID in datas and (self._progress+ 1) in datas[self.rootQuestID]:
			data = datas[self.rootQuestID][self._progress]
			if data["npcID"] == int(param):
				player.client.StartWhisperQuest(self.rootQuestID, self._id, data["npcSoundID"], data["startSoundID"], data["dialogue"] )
			
		return False

class QuestBuildDongFu( QuestTask ):
	"""建造洞府"""
	
	quest_event = [ QuestEventDefine.EVENT_BUILD_DONGFU ]

	def __init__(self):
		QuestTask.__init__(self)
	
	def updateProgress(self, player, eventID, param):
		if not self.isDone():
			self._progress += 1
			return True
		else:
			return False