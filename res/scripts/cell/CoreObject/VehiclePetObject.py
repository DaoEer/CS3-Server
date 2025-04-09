# -*- coding: utf-8 -*-

"""
用于宠物类型的基本类型
"""


#python
import csconst
import csdefine
#engine
import KBEngine
from KBEDebug import *

#script
import CoreObject.GameObject as GameObject

from CoreInterface import NPCAmbulantInterface
from CoreInterface import VehiclePetAIInterface
from CoreInterface import VehiclePetCombatInterface

class VehiclePetObject(
		GameObject.GameObject,
		NPCAmbulantInterface.NPCAmbulantInterface,
		VehiclePetCombatInterface.VehiclePetCombatInterface,
		VehiclePetAIInterface.VehiclePetAIInterface
		 ):
	"""
	玩家宠物基类
	"""
	def __init__( self ):
		GameObject.GameObject.__init__( self )
		VehiclePetCombatInterface.VehiclePetCombatInterface.__init__( self )
		NPCAmbulantInterface.NPCAmbulantInterface.__init__( self )
		VehiclePetAIInterface.VehiclePetAIInterface.__init__( self )

	def doEnterSpace( self ):
		"""
		进入一个空间调用
		"""
		VehiclePetCombatInterface.VehiclePetCombatInterface.doEnterSpace( self )

	def doLeaveSpace( self ):
		"""
		离开一个空间调用（在doEnterSpace之后）
		"""
		VehiclePetCombatInterface.VehiclePetCombatInterface.doEnterSpace( self )
		
	def setSelfEntityFlag(self):
		"""
		virtual method
		"""
		self.setEntityFlag( csdefine.ENTITY_FLAG_VEHICLEPET )

	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_VEHICLEPET)

	def behIsOptimize(self, bedType, behDescribe):
		"""
		是否采用优化的方案，目前暂时没有确定是判断逻辑
		:return: bool
		"""
		return False
		
	def initSpeed( self ):
		"""
		override
		"""
		self.setSpeed(  (self.speed * csconst.RunRatio) / 100.0 )
		
	def setSpeed( self,  val ):
		"""
		设置移动速度
		"""
		if self.moveSpeed != val:
			self.moveSpeed = val
	
	def getLevel( self ):
		"""
		"""
		return self.level
	
	def onOwnerAddEnemy( self, enemyID ):
		VehiclePetAIInterface.VehiclePetAIInterface.onOwnerAddEnemy( self, enemyID )
	
	def stopMovingForType( self, moveType ):
		"""
		停止移动，使用移动等级
		"""
		pass				# 现在 ai都改到客户端了
	
	def moveStart( self, mScriptID, mSpeed, misUpdateSpeed, mArgs  = () ):
		NPCAmbulantInterface.NPCAmbulantInterface.moveStart( self, mScriptID, mSpeed, misUpdateSpeed, mArgs )

	def onMoveOver( self, controllerID, userData ):
		"""
		virtual method
		移动结束，但似乎不管移动是否成功，都调用此函数
		@param controllerID		:	移动控制器ID
		@type  controllerID     :	int
		"""
		NPCAmbulantInterface.NPCAmbulantInterface.doMoveOver( self, controllerID, userData )


