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


	def ChangeModel( self, entity, targetEntity ):
		"""
		改变自身模型
		"""
		entity.modelNumber = targetEntity.modelNumber
		entity.headModel = targetEntity.headModel
		entity.cloakModel = targetEntity.cloakModel
		entity.bodyModel = targetEntity.bodyModel
		entity.hairModel = targetEntity.hairModel
		entity.adornModel = targetEntity.adornModel
		entity.suitsModel = targetEntity.suitsModel
		entity.hatModel = targetEntity.hatModel
		entity.coatModel = targetEntity.coatModel
		entity.handModel = targetEntity.handModel
		entity.waistModel = targetEntity.waistModel
		entity.pantsModel = targetEntity.pantsModel
		entity.shoesModel = targetEntity.shoesModel
		entity.necklaceModel = targetEntity.necklaceModel
		entity.rringModel = targetEntity.rringModel
		entity.weaponModel = targetEntity.weaponModel
		entity.fabaoModel = targetEntity.fabaoModel
		entity.skeletalWeaponModel = targetEntity.skeletalWeaponModel


	def copySkills( self, entity, targetEntity ):
		"""
		设置技能列表
		"""
		for skillID in targetEntity.attrSkills:
			if skillID not in entity.attrSkills:
				entity.attrSkills.append( skillID )


	


