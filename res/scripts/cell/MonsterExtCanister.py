# -*- coding: utf-8 -*-


#python
#engine
import KBEngine
#script
import Monster


class MonsterExtCanister( Monster.Monster ):
	"""
	火油罐
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )

	def onAddEnemy( self, entityID ):
		"""
		重载此方法，添加敌人时不会进入战斗状态
		"""
		self.onEnemyListChange( entityID )

	def CELL_operationCanister( self, srcEntityID ):
		"""
		操作火油罐
		"""
		if self.ammo <= 0:
			return
		if self.cdEndTime:
			return

		self.allClients.CLIENT_OnOperationCanister( self.cdEndTime, self.ammo )
		self.loadingBattery()
		self.useSkillToEntity( self.getScript().skillID,self.id )
		self.ammo -= 1
	
	def loadingBattery( self ):
		"""
		加载火药
		"""
		if self.ammo > 0:
			self.cdEndTime = self.getScript().loadCD
			self.addTimerCallBack(self.cdEndTime,"onLoadingBatteryFinish",())

	def onLoadingBatteryFinish( self ):
		"""
		"""
		self.cdEndTime = 0.0
