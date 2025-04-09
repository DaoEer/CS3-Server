# -*- coding: utf-8 -*-
#
import Math
import Const
import KBEngine
import csconst
import FightRuleMgr
from KBEDebug import *
from VehiclePetFormulas import formulas
import CoreObject.VehiclePetObject as VehiclePetObject

class VehiclePet( VehiclePetObject.VehiclePetObject ):
	"""
	"""
	def __init__(self):
		VehiclePetObject.VehiclePetObject.__init__(self)
		self.isInPending = 0
		self.onEnterFree()
		
		ownerEntity = self.getOwnerEntity()
		if ownerEntity and ownerEntity.hasEffectState(csdefine.EFFECT_STATE_PROTECT):
			self.addVehicePetProtect()

	def getOwnerEntity( self ):
		owner = KBEngine.entities.get( self.baseOwner.id )
		if owner and  self.spaceID == owner.spaceID and owner.isReal(): #不在一个地图，默认为找不到
			return owner
			
		return None
		
	def statusMessage(self, statusMessageType, *statusMessageArg):
		"""
		<Define method>
		@param statusMessageType : 消息类型
		@type  statusMessageType : UINT16
		@param statusMessageArg : 消息内容可变参数列表
		@type  statusMessageArg : 元组
		"""
		owner = self.getOwnerEntity()
		if owner:
			owner.statusMessage(statusMessageType, statusMessageArg)
		else:
			if self.baseOwner:
				self.baseOwner.statusMessage(statusMessageType, statusMessageArg)
				
	def setStep( self, step ):
		"""设置介次"""
		self.step = step
		self.level = formulas.getLevelByStep( self.step )
		self.calcAttachProperties( )
	
	def setExp( self, exp ):
		"""设置经验"""
		self.exp = exp

	def reqTeleportToOwner( self ):
		"""
		请求传送到主人身边
		"""
		if self.baseOwner:
			self.baseOwner.petReqTeleport( self.base )
	
	def onTeleportToOwner( self, spaceCell, position ):
		"""
		define method
		传送到主人身边回调
		"""
		oldSpaceID = self.spaceID
		oldSpaceScriptID = self.getCurrentSpaceData( Const.SPACE_DATA_SCRIPT_ID )
		self.teleport( spaceCell, Math.Vector3(position), self.direction )
		self.afterTeleportToOwner( oldSpaceID, oldSpaceScriptID )
	
	def afterTeleportToOwner( self, oldSpaceID, oldSpaceScriptID ):
		"""
		define method
		传送完毕回调
		"""
		if oldSpaceID != self.spaceID:
			newSpaceScriptID = self.getCurrentSpaceData( Const.SPACE_DATA_SCRIPT_ID )
			self.triggerSkillEvent( csdefine.SKILL_EVENT_SPACE_CHANGE, self.id, { "OldSpaceID" : oldSpaceScriptID, "NewSpaceID" :newSpaceScriptID,"isInNewSpace":1 if oldSpaceScriptID == newSpaceScriptID else 0  } )
	
	def isOwner( self, checkID ):
		"""
		判断ID是否是主人ID
		"""
		return  self.baseOwner and self.baseOwner.id == checkID
		
	def updatePetAttr( self, key, value ):
		"""
		<Define method>
		幻兽的数据更新
		"""
		if key in csconst.VPATTR_SAVE_SELF:return					# 保存到幻兽身上的属性就不需要通过玩家来更新
		
		if self.get( key ) and self.get(key) != value:
			VehiclePetObject.VehiclePetObject.__setattr__( self, key, value )

	def onEnterDead( self ):
		"""
		virtual method
		进入死亡状态
		"""
		self.addTimerCallBack( Const.VPET_DELAY_DEAD_TIME , "delayDestroy", () )
			
	def delayDestroy( self ):
		"""
		死亡延迟销毁
		客户端死亡表现
		"""
		if self.baseOwner:
			self.baseOwner.withdrawPet( csdefine.PET_WITHDRAW_DEATH )
			
	def addVehicePetProtect( self ):
		"""
		添加保护，进入未决状态（CST-2315）
		"""
		self.changeState(csdefine.ENTITY_STATE_PEAD)
		self.isInPending = 1

	def removeVehicePetProtect( self ):
		"""
		移除保护，退出未决状态（CST-2315）
		"""
		self.changeState(csdefine.ENTITY_STATE_FREE)
		self.isInPending = 0

	def onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry ):
		"""
		virtual method
		接受伤害回调
		"""
		VehiclePetObject.VehiclePetObject.onReceiveDamage( self, casterID, skillID, damageType, damage, finalDamage, isCritical, isParry )
		self.addDamageList( casterID, damage )

	def onSetPetControlledBy( self, srcEntityID ):
		"""
		在玩家视野范围内才设置controlledBy
		"""
		ownerEntity = self.getOwnerEntity()
		if ownerEntity:
			self.controlledBy = ownerEntity.base
			
	def addEnemy( self, entityID ):
		"""
		<define method>
		procedure method.
		@description
		添加一个敌人到战斗列表ss
		"""
		VehiclePetObject.VehiclePetObject.addEnemy( self, entityID )
		owner = self.getOwnerEntity()
		target = KBEngine.entities.get( entityID )
		if owner and target:
			FightRuleMgr.g_fightMgr.buildEnemyRelation( owner, target )
