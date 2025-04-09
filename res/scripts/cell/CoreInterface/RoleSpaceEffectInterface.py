# -*- coding: utf-8 -*-

import KBEDebug
from ConfigObject.SpaceEffect.SpaceEffectLoader import g_spaceEffectLoader

#------------------------------------------------------------------------------------------------
# 目前支持两种动态效果（此接口支持第一种）
#1、玩家的客户端动态效果，此效果只作用于玩家个人，根据玩家的不同条件显示，还有镜头添加动态效果
#2、空间的客户端动态效果，此效果作用于此空间的所有玩家，一般由策划配置添加
#------------------------------------------------------------------------------------------------

class RoleSpaceEffectInterface:
	"""
	玩家空间动态效果接口
	"""
	def __init__( self ):
		pass

	def onEnterSpaceNotify( self, packArgs ):
		"""
		进入空间
		"""
		spaceEntity = self.getCurrentSpace()
		
		newEffectList = g_spaceEffectLoader.getSpaceEffectCheck( self )
		if newEffectList:
			self.effectList = newEffectList
			self.refreshSpaceEffectCheck( spaceEntity )
			
		# 虽然旧的效果，客户端在跳转场景时，会清理！但是进\出位面无法清理，还是需要手动清理一下
		elif self.effectList:
			self.effectList = []
			self.refreshSpaceEffectCheck( spaceEntity )

	def onLeaveSpaceNotify( self, reason, dstSpaceScriptID, packArgs ):
		"""
		离开空间
		"""
		pass

	def onLoginSpace( self ):
		"""
		登陆地图
		"""
		spaceEntity = self.getCurrentSpace()
		self.effectList = g_spaceEffectLoader.getSpaceEffectCheck( self )
		self.refreshSpaceEffectCheck( spaceEntity )
		
	#------------根据玩家任务状态改变天空盒子-------------------------------------------------
	def questStatusChangeSkyBox( self ):
		""""""
		spaceEntity = self.getCurrentSpace()
		newEffectList = g_spaceEffectLoader.getSpaceEffectCheck( self )
		
		# 获取镜头添加的效果
		for id in list( self.effectList ):
			if g_spaceEffectLoader.checkSpaceEffect( spaceEntity, self, id ) and not id in newEffectList:
				newEffectList.append( id )
		if self.effectList != newEffectList:
			self.effectList = newEffectList
			self.refreshSpaceEffectCheck( spaceEntity )
		
	def replaceSpaceEffect( self, delEffeclList, addEffectList ):
		"""
		替换玩家效果
		"""
		for id in delEffeclList:
			if id in self.effectList:
				self.effectList.remove(id)
		self.effectList.extend( addEffectList )
		
		spaceEntity = self.getCurrentSpace()
		self.refreshSpaceEffectCheck( spaceEntity )

	def ChangeFlySpaceEffect(self, srcEntityID, newEffectList):
		"""
		exposed method
		飞行时改变空间效果
		"""
		eList = list(self.effectList)
		eList.append(int(newEffectList))
		self.client.OnUpdataEffectData(eList)
		
	def refreshSpaceEffectCheck( self, spaceEntity ):
		"""
		刷新空间效果
		"""
		eList = list( self.effectList )
		eList.extend( spaceEntity.spaceEffectList )
		self.client.OnUpdataEffectData( eList )							# 第一、二种，同时通知客户端



