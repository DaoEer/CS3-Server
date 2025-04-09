# -*- coding: utf-8 -*-


"""
usage:
	技能加载类

attribute:
	pass

member function:
	pass

callback:
	pass

"""

import KBEngine
#cell
import ConfigObject.Skill.SkillBase.Skill as Skill
import ConfigObject.Skill.SkillBase.CombatSkill as CombatSkill
#common
import Singleton
import KBEDebug
import LoadModule
import SmartImport
import csconst
import json
import HotUpdate
import csdefine

CLIENT_SKILL_NAME = ["SkillClient", "CombatSkillClient", "InstantSkillClient", "SkillClientCharge", "SkillClientJump", "SkillClientSing"]

def utf16ToJsonCfg( path ):
	allPath = csconst.CONFIG_PATCH + path
	fileObject = open( allPath, encoding="utf16" )
	jsFileObj = json.loads( fileObject.read() )
	fileObject.close()
	return jsFileObj

class SkillLoader( Singleton.Singleton ):
	def __init__( self ):
		self._skills = {}

	def __getitem__( self, skillID ):
		return self._skills.get( skillID, None )
			
	def reloadConfig( self ):
		"""
		技能热更新支持
		"""
		for id,e in KBEngine.entities.items():					#热更新前，取消掉持续效果
			if not e.isReal():
				continue
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or e.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				if e.isCastingSkill():
					skill = self[ e.castingSkillID ]
					skill.removeHoldEffect( e )

		HotUpdate.reloadByPath("Skill.SkillReceiverDefine")
		HotUpdate.reloadByPath("Skill.SkillCasterDefine")
		self._skills.clear()
		self.loadAllSkill()

		for id,e in KBEngine.entities.items():					#热更新后，重新加上持续效果
			if not e.isReal():
				continue
			if e.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE or e.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
				if e.isCastingSkill():
					skill = self[ e.castingSkillID ]
					if skill:
						skill.addHoldEffect( e )

		if self._skills:
			return True
		return False

	def loadAllSkill( self ):
		"""
		加载所有技能
		"""
		skillDatas=[]
		skillDatas = utf16ToJsonCfg("Skill/SkillConfigs/SkillTable.json")
		self.loadSkillConfig(skillDatas)
		
		skillDatas = utf16ToJsonCfg("Skill/SkillConfigs/SkillTableTest.json")
		self.loadSkillConfig(skillDatas, True)
		
		skillDatas = utf16ToJsonCfg("Skill/SkillConfigs/PassiveSkillTable.json")
		self.loadSkillConfig(skillDatas)
		
	def loadSkillConfig( self, skillDatas, isAllowedRepeat=False ):
		for data in skillDatas:
			skillID = int( data["Name"] )
			skillType = data["SkillType"]
			
			# 客户端技能不需要加载到服务器
			if skillType in CLIENT_SKILL_NAME:
				continue
			try:
				skillClass = SmartImport.smartImport( "ConfigObject.Skill.Skill." + skillType + ":" + skillType )
			except:
				skillClass = SmartImport.smartImport( "ConfigObject.Skill.SkillBase." + skillType + ":" + skillType )
			
			skillInstance = skillClass()
			skillInstance.init( data )
			self.register( skillID, skillInstance, isAllowedRepeat )

	def register( self, skillID, skill, isAllowedRepeat=False ):
		if not isAllowedRepeat and skillID in self._skills:
			KBEDebug.ERROR_MSG( "skillID(%d) is repeat use!!"%skillID)
			return
		self._skills[ skillID ] = skill


g_skills = SkillLoader()
g_skills.loadAllSkill()


