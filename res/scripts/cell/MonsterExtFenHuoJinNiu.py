# -*- coding: utf-8 -*-
import KBEDebug
import Monster
import csdefine

class MonsterExtFenHuoJinNiu( Monster.Monster ):
	"""
	环任务副本 焚火金牛怪
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def onAddEnemy( self, entityID ):
		"""
		重载此方法，添加敌人时不会进入战斗状态
		"""
		self.onEnemyListChange( entityID )

	def getSpeed( self ):
		"""
		获取速度
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			return spaceEntity.getRunSpeed()

	def getMaxSpeed( self ):
		"""
		获取速度上限
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			return spaceEntity.getMaxSpeed()

	def getAccSpeed( self ):
		"""
		获取加速度
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			return spaceEntity.getAccSpeed()

	def getCenterPos( self ):
		"""
		获取位置
		"""
		spaceEntity = self.getCurrentSpace()
		if spaceEntity:
			return spaceEntity.getCenterPos()

	def moveStartFHJN( self, position ):
		"""
		移动
		"""
		self.destPosition = position
		self.moveStart( csdefine.MOVE_TYPE_NAVIGATE_POINT, self.getSpeed(), True, ( position, 0.0, True, 0 ) )
		