# -*- coding: utf-8 -*-

import KBEDebug
from ConfigObject.SpaceEffect.SpaceEffectLoader import g_spaceEffectLoader


#------------------------------------------------------------------------------------------------
# 目前支持两种动态效果（此接口支持第二种）
#1、玩家的客户端动态效果，此效果只作用于玩家个人，根据玩家的不同条件显示，还有镜头添加动态效果
#2、空间的客户端动态效果，此效果作用于此空间的所有玩家，一般由策划配置添加
#------------------------------------------------------------------------------------------------

class SpaceEffectInterface:
	"""
	空间添加的动态效果接口
	"""
	def __init__( self ):
		pass

	def addSpaceEffects( self, effectList ):
		"""
		增加空间效果
		"""
		if effectList:
			self.spaceEffectList.extend( effectList )
			for playerEntity in self._spaceRoles:
				playerEntity.refreshSpaceEffectCheck( self )
			
	def replaceSpaceEffects( self, effectList ):
		"""
		替换空间效果
		"""
		self.spaceEffectList = effectList
		for playerEntity in self._spaceRoles:
			playerEntity.refreshSpaceEffectCheck( self )

	def removeSpaceEffects( self, effectList ):
		"""
		移除空间效果
		"""
		if effectList:
			for id in effectList:
				if id in self.spaceEffectList:
					self.spaceEffectList.remove(id)
					
			for playerEntity in self._spaceRoles:
				playerEntity.refreshSpaceEffectCheck( self )
		