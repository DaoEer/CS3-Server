# -*- coding: utf-8 -*-
#
import datetime

import KBEngine
from KBEDebug import *

import Math
import csdefine
import Extra.Extend as Extend
from Functions import Functor
from Extra.SpaceConfigMgr import g_spaceConfigMgr
from Extra.XiuWeiLoader import g_xiuWeiLoader


CALLBACK_TIME = 3
# ------------------------------------------------
# base classes of task
# ------------------------------------------------
def findNPCByScriptID(role, scriptID):
	"""
	"""
	for e in role.entitiesInRange(200, cnd = lambda entity : True if entity.entityFlag!=csdefine.ENTITY_FLAG_ROLE else False):
		if e.scriptID == scriptID: return e
	return None
	
def parsePos(nagivateData):
	"""
	"""
	if nagivateData.find("(") != -1:
		data = nagivateData[1:-1]
		posStr = data.replace(' ', ',')
		return eval(posStr)
	return None
		
class Task:
	"""
	"""
	def __init__(self, questID, config):
		self.questID = questID
		self.id = config["id"]
		self.name = config["name"]
		self.goal = config["goal"]		#目标数目
		self.priority = config["priority"]	#优先级
		self.navigateData = config["navigateData"]	#导航数据
		self.hasNagivate = []
		self.progress = 0	#任务进度
		self.callbackID = 0
		self.counter = 0
		
	def __str__(self):
		return self.__class__.__name__

	def __repr__(self):
		return self.__str__()
		
	def doBeforeBegine(self, role):
		"""
		"""
		pass
		
	def do(self, role):
		self.counter += 1
		self.resetCallBack(role)
		#INFO_MSG("[%d][%d::%d##%d] %s do" %(role.id, self.questID, self.id, self.progress, self))
		
	def updateProgress(self, role, progress):
		"""
		更新进度
		"""
		self.progress = progress
		if self.isDone(): self.done(role)
		
	def resetCallBack(self, role):
		if self.callbackID:
			#ERROR_MSG("ROLE[%d] cancel callback[%d], %s" %(role.id, self.callbackID, self))
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
	
	def isDone(self):
		"""
		是否完成
		"""
		return self.goal != 0 and self.progress >= self.goal
		
	def nagivateToNPC(self, role, spaceID, npcScriptID, pos):
		"""
		"""
		if not npcScriptID and pos is None:
			role.outputMsg("Quest[%d]:task[%d] nagivateData error" %(self.questID, self.id))
			return
		
		pos = g_spaceConfigMgr.getNPCPointBySpaceID(spaceID, npcScriptID) if pos is None else pos
		if pos is None:
			self.hasNagivate.append(npcScriptID)
			self.callback(CALLBACK_TIME, self.do, role)
			return
		
		_spaceID = role.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if _spaceID != spaceID:
			role.GMCommand(role, "goto", "{} {} {} {}".format(spaceID, pos[0], pos[1], pos[2]))
			return
		
		position = Extend.Unreal2KBEnginePosition(pos)
		if (role.position - position).length > 2:
			role.moveToPos(position)
			self.callback(CALLBACK_TIME, self.do, role)
			return
		
		if npcScriptID: 
			self.hasNagivate.append(npcScriptID)
		else:
			self.hasNagivate.append(pos)
		
		self.callback(CALLBACK_TIME, self.do, role)
		
	def callback(self, t, fun, *args):
		self.resetCallBack(args[0])
		self.callbackID = KBEngine.callback(t, Functor(self.onCallBack, fun, *args))
		#ERROR_MSG("ROLE[%d] add callback[%d], %s" %(args[0].id, self.callbackID, self))
		
	def onCallBack(self, fun, *args):
		"""
		"""
		self.callbackID = 0
		if fun: fun(*args)
		
	def done(self, role):
		"""
		"""
		self.resetCallBack(role)
		role.outputMsg("Quest[%d]:task[%d] has done" %(self.questID, self.id))

class QuestTaskGetTo(Task):
	"""
	到达某地
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.spaceID = config["param1"]
		self.position = Extend.StrToPosition(config["param2"])
		self.hasMove = False
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		
		spaceID = role.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if spaceID != self.spaceID:
			role.GMCommand(role, "goto", "{} {} {} {}".format(self.spaceID, self.position[0], self.position[1], self.position[2]))
			return
		
		pos = Extend.Unreal2KBEnginePosition(self.position)
		if (role.position - pos).length <= 2:
			if self.hasMove:
				role.cell.broadcastQuestEvent(str(self.questID), str(self.id))
				role.outputMsg("broadcastQuestEvent")
				self.callback(CALLBACK_TIME, self.do, role)
				return
			
			#到达后先移动下，防止某些行为被禁止
			pos = Extend.calRandomWalkPos(Math.Vector3(pos[0], pos[1], pos[2]), 1.0)
		
		role.moveToPos(pos)
		self.hasMove = True
		self.callback(CALLBACK_TIME, self.do, role)
		
class QuestTaskTalkWithNPC(Task):
	"""
	对话
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.talkNpc = config["param1"]
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		
		if self.navigateData:
			data = self.navigateData.split("#")
			if self.talkNpc not in self.hasNagivate:
				self.nagivateToNPC(role, data[1], self.talkNpc, parsePos(data[0]))
				return

		npc = findNPCByScriptID(role, self.talkNpc)
		if npc is None:
			#ERROR_MSG("Quest:%d, %d, NOT found npc[%s]" %(self.questID, self.id, self.talkNpc))
			role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
			return
	
		if (role.position - npc.position).length > 2:
			role.moveToPos(npc.position)
			self.callback(CALLBACK_TIME, self.do, role)
			return
		
		npc.cell.talkWith("","")
		role.cell.triggerQuestDialogWithNPC(npc.scriptID)
		role.outputMsg("talkWith & triggerQuestDialogWithNPC {}".format(npc.scriptID))
	
OUT_TIME = 3 * 60	
class QuestTaskKillMonster(Task):
	"""
	杀怪
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.monsters = config["param1"].split("|") if config["param1"] else []
		self.temp = []
		self.npc = None
		self.centerPos = None
		self.istimeout = False
		self.timeoutTimerID = 0
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		
		#配置错误的话，直接设置完成
		if len(self.monsters) <= 0:
			role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
			return
		
		pos = None
		spaceID = role.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if self.navigateData:	#如果有导航数据的话，那么在导航地图中查找，否则在当前地图
			data = self.navigateData.split("#")
			spaceID = data[1]
			pos = parsePos(data[0])
			
		if not self.temp: self.temp = list(self.monsters)
		if not self.npc:self.npc = self.temp.pop(0)
		
		if self.npc not in self.hasNagivate:
			self.nagivateToNPC(role, spaceID, self.npc, pos)
		else:
			#如果当前没有目标的话，查找一下目标
			if not role.ai.attackTarget:
				target = findNPCByScriptID(role, self.npc)
				
				if not target:
					role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
				else:
					if self.istimeout:	#超时的话，直接设置任务目标完成
						role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
						return
					
					#ERROR_MSG("role[%d] find TARGET" %(role.id))
					self.resetCallBack(role)
					role.ai.attackTarget = target
					role.ai.callback(1)
					
					#超时处理，防止长时间卡死在这个战斗逻辑里
					if self.timeoutTimerID > 0: 
						KBEngine.cancelCallback(self.timeoutTimerID)
						self.timeoutTimerID = 0
					self.timeoutTimerID = KBEngine.callback(OUT_TIME, Functor(self.onTimeOut, role))
				self.npc  = None
			else:
				ERROR_MSG("Quest:%d, %d ROLE has target[%d:%s] [%s]" %(self.questID, self.id, role.ai.attackTarget.id, ai.attackTarget.scriptID, self.npc))
	
	def done(self, role):
		Task.done(self, role)
		if self.timeoutTimerID: 
			KBEngine.cancelCallback(self.timeoutTimerID)
			self.timeoutTimerID = 0
		
	def onTimeOut(self, role):
		role.ai.attackTarget = None
		self.istimeout = True
		self.timeoutTimerID = 0
	
class QuestTaskEventTrigger(Task):
	"""
	触发类任务目标
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
	
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		
		if self.navigateData:	#根据导航数据来找到NPC
			data = self.navigateData.split("#")
			if g_spaceConfigMgr.getSpaceCfgByScriptID(data[1]):
				pos = parsePos(data[0])
				if pos is None:
					if data[0] not in self.hasNagivate:
						self.nagivateToNPC(role, data[1], data[0], None)
						return
				else:
					if pos not in self.hasNagivate:
						self.nagivateToNPC(role, data[1], '', pos)
						return
		
		role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
		
class QuestTaskGetItem(Task):
	"""
	获取物品
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.itemID = config["param1"]
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)

		if self.navigateData:	#根据导航数据来找到NPC
			data = self.navigateData.split("#")
			pos = parsePos(data[0])
			if pos is None:	#如果不是坐标，那么应该是npcID
				npcList = data[0].split("|")
				for id in npcList:
					if id in self.hasNagivate:
						continue
					
					self.nagivateToNPC(role, data[1], id, None)
					return
			else:	
				if pos not in self.hasNagivate:
					self.nagivateToNPC(role, data[1], '', pos)
					return
		
		role.GMCommand(role, "addItem", "{} 1".format(self.itemID ))

#幻兽蛋ID
PET_ITEM_ID = 204010001	
class QuestPetTaskBase(Task):
	"""
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.hasAddPetItem = False
		
	def conjurePet(self, role):
		"""
		召唤宠物
		"""
		if role.currentPetUID<= 0:
			if role.isInitPets:
				if len(role.petCages) <= 0:
					if not self.hasAddPetItem:
						role.GMCommand(role, "addItem", str(PET_ITEM_ID))
						self.callback(CALLBACK_TIME, self.do, role)
						self.hasAddPetItem = True
						return
				
					_items = role.items
					for itemOrder, item in _items.items():
						if item.id == PET_ITEM_ID:
							role.cell.CELL_useItem( str(item.uid), str(role.id) )
							role.outputMsg("CELL_useItem {}".format(item.uid))
							break
					
					self.callback(CALLBACK_TIME, self.do, role)
					return

				role.GMCommand(role, "clearPetSleep")
				for k, v in role.petCages.items():
					role.cell.conjurePet(str(k)) #召唤宠物
					role.outputMsg("conjurePet {}".format(k))
					return
		
class QuestTaskMountPet(QuestPetTaskBase):
	"""
	骑宠
	"""
	def __init__(self, questID, config):
		QuestPetTaskBase.__init__(self, questID, config)
		
	def do(self, role):
		if self.isDone():return
		QuestPetTaskBase.do(self, role)
		
		if role.currentPetUID <= 0:
			self.conjurePet(role)
			self.callback(CALLBACK_TIME + CALLBACK_TIME, self.do, role)
		else:
			role.cell.transformPet()
			role.outputMsg("transformPet")
			self.callback(CALLBACK_TIME + CALLBACK_TIME, self.do, role)
	
	def done(self, role):
		QuestPetTaskBase.done(self, role)
		role.cell.withdrawPet()
		role.outputMsg("withdrawPet")
		
class QuestTaskConjurePet(QuestPetTaskBase):
	"""
	幻兽出战
	"""
	def __init__(self, questID, config):
		QuestPetTaskBase.__init__(self, questID, config)
		
	def do(self, role):
		if self.isDone():return
		QuestPetTaskBase.do(self, role)
		
		#召唤幻兽
		if role.currentPetUID <= 0:
			self.conjurePet(role)
			self.callback(CALLBACK_TIME + CALLBACK_TIME, self.do, role)
			return
		else:
			role.cell.withdrawPet()
			role.outputMsg("withdrawPet")
			self.callback(CALLBACK_TIME + CALLBACK_TIME, role)
			
class QuestUseCommitItem(Task):
	"""
	使用物品达成任务目标
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.itemID = config["param1"]
		self.hasAddItem = False
		self.hasUseItem = False
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		
		#因为服务器那边有可能会禁止使用物品
		if self.hasUseItem:
			role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
			return
		
		_items = role.items
		for itemOrder, item in _items.items():
			if item.id == int(self.itemID):
				self.hasUseItem = True
				role.cell.CELL_useItem( str(item.uid), str(role.id) )
				role.outputMsg("CELL_useItem")
				self.callback(CALLBACK_TIME, self.do, role)
				return
		
		#添加物品
		if not self.hasAddItem:
			role.GMCommand(role, "addItem", self.itemID)
			self.hasAddPetItem = True
		
		self.callback(CALLBACK_TIME, self.do, role)
		
class QuestTaskPlayerLevel(Task):
	"""
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.level = config["param1"]
		
	def doBeforeBegine(self, role):
		"""
		"""
		if self.isDone(): return
		#设置等级
		role.GMCommand(role, "setLevel", "{}".format(str(int(self.level) - 1)))
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		
		role.GMCommand(role, "setLevel", self.level)
		
class QuestTaskLearnSkill(Task):
	"""
	学习技能
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.skillID = int(config["param1"])
		
	def doBeforeBegine(self, role):
		"""
		"""
		if self.isDone(): return
		role.GMCommand(role, "removeSkill", str(self.skillID))
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)

		if self.navigateData:	#根据导航数据来找到NPC
			data = self.navigateData.split("#")
			if data[0] not in self.hasNagivate:
				self.nagivateToNPC(role, data[1], data[0], None)
				return

			npc = findNPCByScriptID(role, data[0])
			if npc is None:
				#ERROR_MSG("Quest:%d, %d, NOT found npc[%s]" %(self.questID, self.id, data[0]))
				role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
				return
			
			if (role.position - npc.position).length > 2:
				role.moveToPos(npc.position)
				self.callback(CALLBACK_TIME, self.do, role)
				return
	
		role.GMCommand(role, "addSkillForQuest", str(self.skillID))
		
class QuestTaskUseSkill(Task):
	"""
	使用技能
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.skillID = int(config["param1"])
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		
		if self.navigateData:	#根据导航数据来找到NPC
			data = self.navigateData.split("#")
			if data[0] not in self.hasNagivate:
				self.nagivateToNPC(role, data[1], data[0], None)
				return

			npc = findNPCByScriptID(role, data[0])
			if npc is None:
				#ERROR_MSG("Quest:%d, %d, NOT found npc[%s]" %(self.questID, self.id, data[0]))
				role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
				return
			
			if (role.position - npc.position).length > 2:
				role.moveToPos(npc.position)
				self.callback(CALLBACK_TIME, self.do, role)
				return
		
		role.cell.useSkillToEntityFC( self.skillID, role.id )
		role.outputMsg("useSkillToEntityFC")
	
class QuestTaskXiuweiLevel(Task):
	"""
	升级修为
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.level = int(config["param1"])
		
		xiuwei = g_xiuWeiLoader.getXiuWeiByLevel(self.level)
		if xiuwei is None:
			ERROR_MSG("NOU found xiuwei level[%d]" %(self.level))
			return
			
		self.xiuwei = xiuwei
		
	def doBeforeBegine(self, role):
		"""
		"""
		if self.isDone(): return
		role.GMCommand(role, "setXiuwei", "{}".format(str(int(self.xiuwei["xiuwei"])-100)))
		
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		
		if role.level < self.xiuwei["playerLevel"]:
			role.GMCommand(role, "setLevel", str(self.xiuwei["playerLevel"]))
		role.GMCommand(role, "setXiuwei", str(self.xiuwei["xiuwei"]))
		
class QuestTaskEnterChuanChengCopy(Task):
	"""
	进入传承副本
	"""
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
		self.callback(CALLBACK_TIME, self.do, role)
		
class QuestTaskEnterPotentialCopy(Task):
	"""
	进入传承副本
	"""
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		role.GMCommand(role, "completeTask", "{} {} {}".format(self.questID, self.id, self.goal))
		self.callback(CALLBACK_TIME, self.do, role)
		
class QuestTaskPlayerTitle(Task):
	"""
	玩家使用某称号
	"""
	def __init__(self, questID, config):
		Task.__init__(self, questID, config)
		self.titleID = int(config["param1"])
		
	def doBeforeBegine(self, role):
		"""
		"""
		if self.isDone(): return
		#先移除
		role.GMCommand(role, "removeTitle", "{}".format(self.titleID))
	
	def do(self, role):
		if self.isDone():return
		Task.do(self, role)
		role.GMCommand(role, "addTitle", "{}".format(self.titleID))
		role.cell.CELL_selectTitle(self.titleID)
		role.outputMsg("CELL_selectTitle")
		
		