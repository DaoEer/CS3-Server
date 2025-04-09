# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster
import KBEDebug
from ConfigObject.SpaceCopyYXLMMonsterDataLoader import g_spaceCopyYXLMMonsterDataLoader
import ItemSystemExp
import csconst
import csdefine
import ECBProximityDefine

class MonsterExtYXLMSoldier( Monster.Monster ):
	"""
	英雄联盟 小兵
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_YXLMSoldier)

	def addExp( self, value ):
		"""
		增加经验
		"""
		levelYXLM = self.levelYXLM
		if levelYXLM > csconst.MONSTERYXLM_MAX_LEVEL:
			return
		allExp = self.exp + value
		#最大值
		maxExp = g_spaceCopyYXLMMonsterDataLoader.getMonsterMaxExpByLevel( self.scriptID, self.levelYXLM )
		if maxExp == -1:
			return
		if not maxExp:
			KBEDebug.ERROR_MSG("maxExp is none (levelYXLM = %i)"%self.levelYXLM)
			return
		while allExp >= maxExp:
			levelYXLM += 1
			allExp -= maxExp
			maxExp = g_spaceCopyYXLMMonsterDataLoader.getMonsterMaxExpByLevel( self.scriptID, levelYXLM )
			if not maxExp or maxExp < 0:
				break
		if levelYXLM > csconst.MONSTERYXLM_MAX_LEVEL:
			levelYXLM = csconst.MONSTERYXLM_MAX_LEVEL
			allExp = g_spaceCopyYXLMMonsterDataLoader.getMonsterMaxExpByLevel( self.scriptID, levelYXLM )
		self.exp = allExp
		self.setlevelYXLM( levelYXLM )

	def setlevelYXLM( self, newLevel ):
		"""
		设置副本新的等级
		"""
		if newLevel == self.levelYXLM:
			return

		self.levelYXLM = newLevel
		self.onLevelYXLMUp()

	def onLevelYXLMUp( self ):
		"""
		升级
		"""
		self.calcAttachProperties()
		spaceEntity = self.getCurrentSpace()
		self.monsterAISendCommand(self.id,"LevelUp")
		if spaceEntity and self.levelYXLM == csconst.MONSTERYXLM_MAX_LEVEL:
			spaceEntity.getScript().onConditionChange( spaceEntity,"",spaceEntity.scriptID,"LevelUp",str(self.way) + "|" + str(self.getCamp()))
	
	def getBaseProperties(self):
		"""
		通过配置获取基础属性数值
		@return: dict {propertyID: value}
		"""
		if self.levelYXLM == 1:
			return ItemSystemExp.g_SpaceCopyYXLMMonsterPropertyValueCfg_1.getData( self.profession, self.attrLevel, self.level)
		elif self.levelYXLM == 2:
			return ItemSystemExp.g_SpaceCopyYXLMMonsterPropertyValueCfg_2.getData( self.profession, self.attrLevel, self.level)
		elif self.levelYXLM == 3:
			return ItemSystemExp.g_SpaceCopyYXLMMonsterPropertyValueCfg_3.getData( self.profession, self.attrLevel, self.level)

	def monsterAIReTriggerNearTrap( self ):
		"""
		"""
		if not self.isReady() or self.inDestroying():
			return
		
		entityList = self.entitiesInRangeExt( csdefine.RE_TRIGGER_NEAR_TRAP_RANGE, "MonsterExtYXLMSoldier" )
		entityList.extend(self.entitiesInRangeExt( csdefine.RE_TRIGGER_NEAR_TRAP_RANGE, "MonsterExtYXLMTower" ))
		for entity in entityList:
			if not entity.isReal() or entity.inDestroying() or not entity.monsterAIIsStart(): #被传送/被销毁/AI没启动 都不需要触发陷阱
				continue
			entity.beReTriggerTrap( self, ECBProximityDefine.PROXIMITY_AI_ATTACK_1 )
			entity.beReTriggerTrap( self, ECBProximityDefine.PROXIMITY_AI_INITIATIVE_1 )
		self.allClients.CLIENT_PlayerReTriggerTrap()
