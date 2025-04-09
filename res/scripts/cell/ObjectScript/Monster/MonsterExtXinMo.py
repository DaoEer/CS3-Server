# -*- coding: utf-8 -*-
#############
#心魔怪物脚本
#############

import ObjectScript.Monster.Monster as Monster
class MonsterExtXinMo( Monster.Monster ):
	def __init__( self ):
		Monster.Monster.__init__( self )

	def initData( self, configData ):
		"""
		初始化数据
		@param configData: dict
		"""
		Monster.Monster.initData( self, configData )
		self.attrSkill = []


	def copySkills( self, entity, targetEntity ):
		"""
		设置技能列表
		"""
		for skillID in targetEntity.attrSkills:
			if skillID not in entity.attrSkills:
				entity.attrSkills.append( skillID )


	


