# -*- coding: utf-8 -*-
import random

import KBEngine
import KBEDebug

import csdefine
import KST_Config
import Extra.Extend as Extend

from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_Run import CRun
from PlayerAI.State.AI_Attack import CAttack
from PlayerAI.State.AI_Dead import CDeadToRevive
from PlayerAI.State.AI_Teleport import CTeleport
from PlayerAI.State.CStateInterface import eAIState
from PlayerAI.State.AI_System import CNull, CPetAISys, CTeamAISys
from Extra.SpaceConfigMgr import g_spaceConfigMgr

class SpaceAI( AIBase ):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.actionStatus[eAIState.NULL] = CNull(self)
		self.actionStatus[eAIState.Run] = CRun(self)
		self.actionStatus[eAIState.Pet] = CPetAISys(self)
		self.actionStatus[eAIState.Teleport] = CTeleport(self)
		self.actionStatus[eAIState.Team] = CTeamAISys(self)
		self.actionStatus[eAIState.Dead] = CDeadToRevive(self)
		self.actionStatus[eAIState.Attack] = CAttack(self)
		
		self.callbackID = 0
		self.attackTarget = None
		
		self.space_test = None
		spaces = []
		for k,v in KST_Config.space_maps.items():
			if v[1] : spaces.append((k, v[0]))
		if len(spaces) <= 0:
			KBEDebug.ERROR_MSG("Space error")
			return
		
		self.space_test = random.choice(spaces)
		
	def onEnterSpace(self):
		"""
		"""
		self.owner.eventObj.registerEvent("Event_OnHPChanged", self)
		self.owner.eventObj.registerEvent("Event_OnMPChanged", self)

	def onLeaveSpace(self):
		"""
		"""
		self.reset()
		self.owner.eventObj.unregisterEvent("Event_OnHPChanged", self)
		self.owner.eventObj.unregisterEvent("Event_OnMPChanged", self)
		
	def reset(self):
		"""
		"""
		if self.callbackID > 0:
			KBEngine.cancelCallback(self.callbackID)
			self.callbackID = 0
		self.changeAIState(eAIState.NULL)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.space_test:
			KBEDebug.ERROR_MSG("space map set error")
			return

		if not self.enterDefaultMap:
			self.owner.GMCommand(self.owner, "set_level", "35")
			self.enterDefaultSpace()
			return

		self.think()
		
	def think(self):
		"""
		"""
		#获取测试地图相关设置
		spaceConfig = g_spaceConfigMgr.getSpaceCfgByScriptID(self.space_test[1])
		if not spaceConfig:
			KBEDebug.ERROR_MSG("get space[%s] cofing error" %(self.spaceScriptID))
			return

		#先在大地图集合
		currentSpace = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if currentSpace == KST_Config.default_map[0]:
			#召唤宠物
			if KST_Config.pet and self.owner.currentPetUID == 0:
				self.changeAIState(eAIState.Pet)
				return

			#地图需何种方式进入
			belongType = list(map(int, spaceConfig.get("belongType", "1").split("|")))	
			if KST_Config.space_first_belongType in belongType:
				belongType = KST_Config.space_first_belongType
			else:
				belongType = random.choice(belongType)
				
			if int(belongType) == csdefine.SPACE_BELONG_TEAM:	#组队	
				if self.owner.teamID == 0:
					self.changeAIState(eAIState.Team)
					return
			elif belongType == csdefine.SPACE_BELONG_TONG: 		#加入帮会
				if self.owner.tongDBID == 0:
					self.changeAIState(eAIState.Tong)
					return

			#延时不等的时间进入，防止创建的副本都挤在一个cell中
			#这里延时久一点，实测中发现第二次申请进入副本时，可能碰上上次副本销毁，导致进入失败
			self.callbackID = KBEngine.callback(random.randint(10, 15), self.onCallBack)
		elif currentSpace == self.space_test[1]:
			if self.attackTarget:
				self.changeAIState(eAIState.Attack)
			else:
				self.changeAIState(eAIState.Run)
		else:
			self.enterDefaultMap = False
			self.enterDefaultSpace()
		
	def onCallBack(self):
		self.callbackID = 0
		self.changeAIState(eAIState.Teleport)
	
	def enterDefaultSpace( self ):
		"""
		"""
		if not self.enterDefaultMap:
			self.enterDefaultMap = True
			spaceScriptID = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
			if spaceScriptID != self.spaceInfo[0]:
				#这里修改进入的坐标没别的意思，就是选择进入相同地图的玩家传送到一起，好组队进副本
				times = int(self.space_test[0] / 2)
				remainder = self.space_test[0] % 2
				uepos = self.spaceInfo[1].split(" ")
				pos = "{} {} {}".format(str(int(uepos[0]) + 800*times), str(int(uepos[1]) + 800*remainder), uepos[2])
				self.owner.GMCommand(self.owner, "goto", "{} {}".format(self.spaceInfo[0], pos))
				return
			else:
				KBEngine.callback(3, self.onSetSpaceData)
		
	def findTarget(self):
		"""
		获取范围内离自己最近的一个怪物
		"""	
		result = None
		minDist = -1

		for e in self.owner.entitiesInRange( 10, cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_MONSTER and Extend.checkCanAttack( entity, self.owner ) else False ):
			dstToEntity = self.owner.position.distTo( e.position )
			if minDist == -1:
				minDist = dstToEntity
				result = e
				if minDist == 0:
					break
			
			if dstToEntity < minDist:
				dstToEntity = minDist
				result = e
		
		self.attackTarget = result
		return result
		
AIBase.setClass("SpaceAI", SpaceAI)