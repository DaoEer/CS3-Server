# -*- coding: utf-8 -*-


"""
usage:
	怪物基类

attribute:
	modelNumber

member function:
	getModelNumber
	setModelNumber

callback:
	pass

"""


#python
#engine
import KBEngine
import KBEDebug
#script
import MonsterExtBattery
import time
import csarithmetic
import csdefine
import Const
import Functions


class MonsterExtBatteryRocket( MonsterExtBattery.MonsterExtBattery ):
	"""
	火箭车（引导）
	"""
	def __init__( self ):
		MonsterExtBattery.MonsterExtBattery.__init__( self )
		
	def CELL_cancelOperationBattery( self, srcEntityID ):
		"""
		<exposed method>
		玩家取消操作炮台
		"""
		if self.guidTimer == 0:
			MonsterExtBattery.MonsterExtBattery.CELL_cancelOperationBattery( self, srcEntityID )
		
	def CELL_projectRocketBattery( self, srcEntityID, yaw ):
		"""
		<exposed method>
		火箭车开炮
		"""
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return
		if self.guidTimer == 0:			# 第一发火箭
			if self.ammo <= 0:
				KBEDebug.ERROR_MSG("Can not project battery(entityID:%d)!as ammo no emought!"%self.id)
				return
			if self.cdEndTime:
				KBEDebug.INFO_MSG("Can not project battery(entityID:%d)!as cd not cool!"%self.id)
				return
			if self.operatorID != srcEntityID:
				KBEDebug.ERROR_MSG("Illegal Operation(%d)!as real operator(%d)"%(operatorID, self.operatorID))
				return
			operator = KBEngine.entities.get( srcEntityID )
			if operator is None:
				return
			
		self.guidTimer += 1
		self.allClients.CLIENT_OnProjectRocketBattery( self.guidTimer, yaw )
		
		object = self.getScript()
		if self.guidTimer == object.guidTimer:			# 最后一发火箭
			self.ammo -= 1
			self.loadingBattery()
		
	
	def loadingBattery( self ):
		"""装载火炮"""
		MonsterExtBattery.MonsterExtBattery.loadingBattery( self )
		self.guidTimer = 0