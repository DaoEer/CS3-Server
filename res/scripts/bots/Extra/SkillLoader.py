# -*- coding: utf-8 -*-
#
"""
"""
import csconst
import json
import Singleton

import KBEngine
import KBEDebug

def utf16ToJsonCfg( path ):
	allPath = csconst.CONFIG_PATCH + path
	fileObject = open( allPath, encoding="utf16" )
	jsFileObj = json.loads( fileObject.read() )
	fileObject.close()
	return jsFileObj
	
class SkillLoader( Singleton.Singleton ):
	"""
	"""
	def __init__( self ):
		self._skills = {}

	def loadSkill( self ):
		"""
		"""
		skillDatas = utf16ToJsonCfg("Skill/SkillConfigs/SkillTable.json")
		self.loadSkillConfig(skillDatas)
		
		skillDatas = utf16ToJsonCfg("Skill/SkillConfigs/PassiveSkillTable.json")
		self.loadSkillConfig(skillDatas)
		
	def loadSkillConfig( self, datas ):
		"""
		"""
		for data in datas:
			skillID = int(data["Name"])
			if skillID in self._skills:
				KBEDebug.ERROR_MSG( "skillID(%d) is repeat use!!"%skillID)
				continue
			
			self._skills[skillID] = data
			
	def getSkillData(self, skillID):
		"""
		"""
		return self._skills.get(skillID, None)
		
		
g_skills = SkillLoader()
g_skills.loadSkill()