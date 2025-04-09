# -*- coding: utf-8 -*-
import KBEngine
import KBEDebug
import Math, random

import csdefine
import KST_Config
import Extra.Extend as Extend
from PlayerAI.Base.AIBase import AIBase
from PlayerAI.State.AI_System import CPetAISys
from PlayerAI.State.AI_Attack import CRoleAttack
from PlayerAI.State.AI_Dead import CDeadToRevive
from PlayerAI.State.AI_Run import CRunForFindTarget
from PlayerAI.State.CStateInterface import eAIState

class RoleFightAIBase(AIBase):
	"""
	"""
	def __init__(self):
		AIBase.__init__(self)
		
		self.attackTarget = None #攻击目标
		self.allowAttackFlag = False
		self.walkRadius = 10
		self.spawnPosition = None
		
		self.actionStatus[eAIState.Pet] = CPetAISys(self)
		self.actionStatus[eAIState.Attack] = CRoleAttack(self)
		self.actionStatus[eAIState.Dead] = CDeadToRevive(self)
		self.actionStatus[eAIState.Run] = CRunForFindTarget(self)
		
	def onEnterSpace(self):
		"""
		"""
		self.spawnPosition = Math.Vector3(self.owner.position)
		self.owner.eventObj.registerEvent("Event_OnHPChanged", self)
		self.owner.eventObj.registerEvent("Event_OnMPChanged", self)
	
	def onLeaveSpace(self):
		self.owner.eventObj.unregisterEvent("Event_OnHPChanged", self)
		self.owner.eventObj.unregisterEvent("Event_OnMPChanged", self)
		
	def onSetSpaceData(self):
		"""
		"""
		AIBase.onSetSpaceData(self)
		if not self.enterDefaultMap:
			self.enterDefaultSpace()
			return
			
		#进入战斗地图
		spaceScriptID = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if spaceScriptID != self.fightSpace[0]:
			self.owner.GMCommand(self.owner, "goto", "{} {}".format(self.fightSpace[0], self.fightSpace[1]))
			return
		
		self.owner.GMCommand(self.owner, "set_level", "35")
		self.owner.GMCommand(self.owner, "addSkill", str(self.owner.firstUseSkillID))
		
		self.think()
		#延时30S才允许攻击，让玩家或者MOSTER散开一些
		KBEngine.callback(30, self.allowAttack)
		
	def think(self):
		"""
		"""
		#召唤宠物
		if KST_Config.pet and self.owner.currentPetUID == 0:
			self.changeAIState(eAIState.Pet)
			return
		
		if self.attackTarget == None:
			self.changeAIState(eAIState.Run)
		else:
			self.changeAIState(eAIState.Attack)
	
	def allowAttack(self):
		self.allowAttackFlag = True
		
	def findTarget(self):
		"""
		"""
		return None
		

class RoleFightRoleAI(RoleFightAIBase):
	"""
	"""
	def __init__(self):
		RoleFightAIBase.__init__(self) 
		self.walkRadius = KST_Config.rolevsrole_fight_radius
		
		spaces = []
		for k,v in KST_Config.rolevsrole_fight_map.items():
			if v[1] : spaces.append(v[0])
		if len(spaces) <= 0:
			KBEDebug.ERROR_MSG("SPACE Error")
			return
		
		self.fightSpace = random.choice(spaces)
		
	def onEnterSpace(self):
		"""
		"""
		RoleFightAIBase.onEnterSpace(self)
		self.owner.firstUseSkillID = KST_Config.rolevsrole_fight_skill
		
		#进入战斗地图
		spaceScriptID = self.owner.clientapp.getSpaceData("SPACE_SCRIPT_ID")
		if spaceScriptID == self.fightSpace[0]:
			#设置玩家关系规则 （与其他玩家都是敌对关系）
			self.owner.GMCommand(self.owner, "setRoleSpaceRelationRule", "4")
			return
		
	def findTarget(self):
		"""
		获取范围内离自己最近的一个玩家
		"""
		if not self.allowAttackFlag:
			return None
			
		result = None
		minDist = -1

		for e in self.owner.entitiesInRange( 5, cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_ROLE and Extend.checkCanAttack( entity ) and Extend.checkInCenter(entity, self.spawnPosition, self.walkRadius) and not entity.hasFlag( csdefine.ROLE_FLAG_WATCHER ) else False ):
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
		
class RoleFightMonsterAI(RoleFightAIBase):
	"""
	"""
	def __init__(self):
		RoleFightAIBase.__init__(self)
		self.walkRadius = KST_Config.rolevsmonster_fight_radius
		self.fightSpace = KST_Config.rolevsmonster_fight_map
		
	def onEnterSpace(self):
		RoleFightAIBase.onEnterSpace(self)
		self.owner.firstUseSkillID = KST_Config.relevsmonster_fight_skill
		self.owner.eventObj.registerEvent("Event_OnMonsterDead", self)
		
	def onLeaveSpace(self):
		RoleFightAIBase.onLeaveSpace(self)
		self.owner.eventObj.unregisterEvent("Event_OnMonsterDead", self)
	
	def onMonsterDead(self, scriptID, id):
		"""
		"""
		self.owner.GMCommand(self.owner, "clone", scriptID)
		
	def findTarget(self):
		"""
		获取范围内离自己最近的一个怪物
		"""
		if not self.allowAttackFlag:
			return None
			
		result = None
		minDist = -1

		for e in self.owner.entitiesInRange( 5, cnd = lambda entity : True if entity.entityFlag==csdefine.ENTITY_FLAG_MONSTER and Extend.checkCanAttack( entity ) and Extend.checkInCenter(entity, self.spawnPosition, self.walkRadius) else False ):
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

AIBase.setClass("RoleFightRoleAI", RoleFightRoleAI)
AIBase.setClass("RoleFightMonsterAI", RoleFightMonsterAI)	