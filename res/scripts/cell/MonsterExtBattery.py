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
import Monster
import time
import csarithmetic
import csdefine
import Const
import Functions


class MonsterExtBattery( Monster.Monster ):
	"""
	炮台
	"""
	def __init__( self ):
		Monster.Monster.__init__( self )
		
	def setSelfEntityFlagExt(self):
		"""
		virtual method
		"""
		self.setEntityFlagExt(csdefine.ENTITY_FLAG_EXT_MONSTER_EXT_BATTERY)
		
	def onAddEnemy( self, entityID ):
		"""
		重载此方法，添加敌人时不会进入战斗状态
		"""
		self.onEnemyListChange( entityID )
		#将第一进入敌人列表的entity作为攻击目标
		if len(self.enemyList) == 1:
			self.setTargetID(entityID)
		
	def CELL_operationBattery( self, srcEntityID ):
		"""
		<exposed method>
		玩家操作炮台
		"""
		self.beginOperationBattery( srcEntityID )
	
	def beginOperationBattery( self, operatorID ):
		"""
		开始操作炮台
		"""
		operator = KBEngine.entities.get( operatorID )
		if operator is None:
			return
		if self.operatorID:					
			# 因为除了玩家，其他entity也可以操作。其他entity销毁了，没有取消炮台操作。所以如果操作ID无效，直接忽视
			srcOperator = KBEngine.entities.get( self.operatorID )
			if srcOperator:
				KBEDebug.ERROR_MSG("Cannot operation battery(entityID:%d)!as has operatorID(%d)"%(self.id, self.operatorID))
				return
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return
		try:
			space = self.getCurrentSpace()
			space.recordOpterationMachine(self.id)
		except:
			KBEDebug.INFO_MSG("This use in SpaceCopyAtackCityWar!")
		
		self.operatorID = operatorID
		if operator.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			object = self.getScript()
			operator.clientEntity(self.id).CLIENT_OnSelfOpertionBattery(self.ammo, str(self.cdEndTime))
		else:
			if not self.ammo:					# 没有弹药了
				operator.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (self.id, self.scriptID, "NoAmmo"), self)
			if not self.cdEndTime:				# 已经装好炮弹
				self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (operator.id, operator.scriptID, "ReadyFire"), operator)
	
	def CELL_cancelOperationBattery( self, srcEntityID ):
		"""
		<exposed method>
		玩家取消操作炮台
		"""
		self.cancelOperationBattery( srcEntityID )
		
	def cancelOperationBattery( self, operatorID ):
		"""取消炮台操作"""
		if self.operatorID == operatorID:
			self.operatorID = 0
			try:
				space = self.getCurrentSpace()
				space.removeOpterationMachine(self.id)
			except:
				KBEDebug.INFO_MSG("This use in SpaceCopyAtackCityWar!")
	
	def canAutoFire( self ):
		"""能否自动开火（npc操作）"""
		operator = KBEngine.entities.get( self.operatorID )
		if not operator:
			return False
		if self.ammo <= 0:
			return False
		if self.cdEndTime:
			return False
		return True
	
	def CELL_projectBattery( self, srcEntityID, yaw, batteryPitch ):
		"""
		<exposed method>
		玩家开炮
		"""
		if self.isState(csdefine.ENTITY_STATE_DEAD):
			return
		if self.ammo <= 0:
			KBEDebug.ERROR_MSG("Can not project battery(entityID:%d)!as ammo no emought!"%self.id)
			return
		if self.cdEndTime:
			KBEDebug.INFO_MSG("Can not project battery(entityID:%d)!as cd not cool!"%self.id)
			return
		if self.operatorID != srcEntityID:
			KBEDebug.ERROR_MSG("Illegal Operation(%d)!as real operator(%d)"%(srcEntityID, self.operatorID))
			return
		operator = KBEngine.entities.get( srcEntityID )
		if operator is None:
			return
		self.ammo -= 1
		self.loadingBattery()
		self.allClients.CLIENT_OnProjectBattery( yaw, batteryPitch )
	
	def npcProjectBattery( self, skillID, targetID ):
		"""NPC开炮"""
		self.ammo -= 1
		self.useSkillToEntity(skillID, targetID)
		
		self.loadingBattery()
	
	def loadingBattery( self ):
		"""装载火炮"""
		if self.ammo <= 0:					# 没有弹药了
			operator = KBEngine.entities.get( self.operatorID )
			if operator and operator.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
				operator.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (self.id, self.scriptID, "NoAmmo"), self)
		else:
			object = self.getScript()
			self.cdEndTime = Functions.getTime(object.loadCD)
			self.addTimerCallBack(object.loadCD, "onLoadingBatteryFinish", () )
		
	def onLoadingBatteryFinish( self ):
		"""完成火炮装载"""
		self.cdEndTime = 0
		operator = KBEngine.entities.get( self.operatorID )
		if operator and operator.isEntityFlag( csdefine.ENTITY_FLAG_MONSTER ):
			self.monsterAITriggerEvent(csdefine.ENTITY_EVENT_COMMAND, (operator.id, operator.scriptID, "ReadyFire"), operator)



