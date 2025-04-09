# -*- coding: utf-8 -*-
import KBEMath
import KBEngine
import KBEDebug
import Math
import math
import csarithmetic
import csdefine
import Functions
import ItemTypeEnum
import BuffDataType

class CSkillInterface( object ):
	def __init__( self ):
		object.__init__( self )


	def cSkill_onClientActorCreate(self, srcEntityID):
		"""
		<define method>
		客户端被创建出来
		"""
		pass

#-----------------------------------客户端技能效果结算--------------------------------------------------
	def cReceiveDamage(self, srcEntityID,  casterID, skillID, damageType, damage, isCritical, isParry, deadEffect, actForbid ):
		"""
		<Exposed Method>
		客户端申请接受伤害
		"""
		self.receiveDamage(casterID, skillID, damageType, damage, bool(isCritical), bool(isParry), deadEffect, actForbid)

	def cSkillSetHP(self, srcEntityID,  value):
		"""
		<Exposed Method>
		设置MP
		"""
		self.setHP( value )

	def cSkillCreateEntityByScriptID(self, srcEntityID, scriptID, position, direction):
		"""
		<Exposed Method>
		客户端技能申请创建entity
		"""
		Pos = KBEMath.Unreal2KBEnginePosition( position )
		Dir = KBEMath.Unreal2KBEnginePosition( direction )
		self.createEntityByScriptID(scriptID, Pos, Dir, {"spawnPos": Pos, "spawnDir":Dir})

	def cSkillGangQiDamage(self, srcEntityID, casterID, skillGangQiValue, skillGangQiRadio):
		"""
		<Exposed Method>
		客户端技能接受罡气伤害
		"""
		caster = KBEngine.entities.get( casterID, None)
		if not caster:
			return

		gangQiDamage = caster.getGangQiDamage( self, skillGangQiRadio, skillGangQiValue )
		self.recvGangQiDamage( gangQiDamage )

#------------------------------------客户端持有效果结算--------------------------------------------------	
	def cSkillAddActCounters(self, srcEntityID, actList):
		"""
		<Exposed Method>
		添加动作限制字
		"""
		self.actCounterIncList( actList )

	def cSkillRemoveActCounters(self, srcEntityID, actList):
		"""
		<Exposed Method>
		移除动作限制字
		"""
		self.actCounterDecList( actList )

	def cSkillAddEffectState(self, srcEntityID, effectState):
		"""
		<Exposed Method>
		客户端技能添加效果状态
		"""
		self.effectStateInc( effectState )

	def cSkillRemoveEffectState(self, srcEntityID, effectState):
		"""
		<Exposed Method>
		客户端技能移除效果状态
		"""
		self.effectStateDec( effectState )


	def cSkillEffectAddAttr(self, srcEntityID, propertiesList, attrPercent, attrValue):
		"""
		<Exposed Method>
		战斗属性增益/减益
		"""
		for properties in propertiesList:
			if properties in ItemTypeEnum.PROPERTYIDTOSTR:
				temp = {}
				if attrPercent:
					temp.update({"_percent": {properties: attrPercent}})
				if attrValue:
					temp.update({"_value": {properties: attrValue}})

				self.setBuffProperties(temp)
				self.calcAttachProperties()

#------------------------------------客户端技能扩展脚本结算--------------------------------------------------
	def cSkillClientCharge(self, srcEntityID, desPosition, direction, casterMoveSpeed, ischangeDirection):
		"""
		<Exposed Method>
		冲锋技能冲锋结算
		"""
		if ischangeDirection:
			self.changeDirection(KBEMath.Unreal2KBEngineDirection(direction), csdefine.REASON_CHANGE_DIR_FORCE)
		dstPos = KBEMath.Unreal2KBEnginePosition(desPosition)
		raycastList = self.navmeshRaycast( self.position, dstPos )
		if raycastList:
			dstPos = raycastList[0]
		if self.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			self.client.CLIENT_RoleChargePosition(desPosition, casterMoveSpeed)
		else:
			self.chargeToPosition( dstPos, casterMoveSpeed, 0.1 )	

	def cSkillClientJump(self, srcEntityID, desPosition, moveSpeed, delayTime ):
		"""
		<Exposed Method>
		跳扑技能结算
		"""
		dstPos = KBEMath.Unreal2KBEnginePosition(desPosition)
		if delayTime > 0.05:
			self.addTimerCallBack(delayTime, "skillJumpPosition", (dstPos, moveSpeed, 0.1))
		else:
			self.skillJumpPosition( dstPos, moveSpeed, 0.1)		

	def cSkillStopMove(self, srcEntityID, type):
		"""
		<Exposed Method>
		客户端技能停止移动
		"""	
		self.stopMoving(type)

	def cSkillOnDodgeSkillHit(self, srcEntityID, casterID):
		"""
		结算闪避
		"""
		self.allClients.onDodgeSkillHit(casterID)

#------------------------------------客户端技能消耗结算--------------------------------------------------	
	def cSkillSetMP(self, srcEntityID,  value):
		"""
		<Exposed Method>
		设置MP
		"""
		self.setMP( value )

	def cSkillRecvGangQi(self, srcEntityID,  value):
		"""
		<Exposed Method>
		消耗罡气
		"""
		self.recvGangQiDamage( value )

	def cSkillRequireItem(self, srcEntityID, itemID, amount):
		"""
		<Exposed Method>
		消耗物品
		"""
		itemList = caster.getItemInstsByID( itemID )
		self.removeItemListByAmount(itemList, amount, csdefine.ITEM_REMOVE_BY_SKILL)


#------------------------------------技能的效果广播(暂定方案)--------------------------------------------------	
	def broadcastCSkillToPosition(self, srcEntityID, skillID, isInstantSkill, PosX, PosY, PosZ, actionID, beginTime, continuousId, casterID):
		"""
		<Exposed Method>
		广播对位置正式施法
		"""
		if self.otherClients:
			self.otherClients.CastCSkillToPosition(skillID, isInstantSkill, PosX, PosY, PosZ, actionID, beginTime, continuousId, casterID, srcEntityID)

	def broadcastCSkillToTarget(self, srcEntityID, skillID, isInstantSkill, targetID, actionID, beginTime, continuousId, casterID):
		"""
		<Exposed Method>
		广播对目标正式施法
		"""
		if self.otherClients:
			self.otherClients.CastCSkillToTarget(skillID, isInstantSkill, targetID, actionID, beginTime, continuousId, casterID, srcEntityID)

	def broadcastCSkillInterrupted(self, srcEntityID, skillID, reason, actionIndex):
		"""
		<Exposed Method>
		广播技能中断
		"""
		if self.otherClients:
			self.otherClients.SkillInterrupted(skillID, reason, actionIndex)

	def broadcastBeHitPlayEffect(self, srcEntityID, casterID, targetID, actionIndex, actionID, effectID, soundID, beginTime):
		"""
		<Exposed Method>
		广播受击播放动作光效
		"""
		if self.otherClients:
			self.otherClients.BeHitPlayEffect(casterID, targetID, actionIndex, actionID, effectID, soundID, beginTime)

	def broadcastHoldEffectPlayEffect(self, srcEntityID, casterID, effectIndex , actionIndex, actionID, effectID, soundID, beginTime):
		"""
		<Exposed Method>
		广播持有效果HoldEffectPlayEffect播放动作光效声音
		"""
		if self.otherClients:
			self.otherClients.HoldEffectPlayEffect(casterID, effectIndex , actionIndex, actionID, effectID, soundID, beginTime)

	def broadcastHoldEffectEndEffect(self, srcEntityID, effectIndex, actionIndex):
		"""
		<Exposed Method>
		广播持有效果HoldEffectPlayEffect结束
		"""
		if self.otherClients:
			self.otherClients.HoldEffectEndEffect(effectIndex, actionIndex)

	def broadcastPlayBuffEffect(self, srcEntityID, index, casterID, actionIndex, actionID, beginTime, effectID, soundID):
		"""
		<Exposed Method>
		广播开始Buff效果
		"""
		if self.otherClients:
			self.otherClients.PlayBuffEffect(index, casterID, actionIndex, actionID, beginTime, effectID, soundID)

	def broadcastAddBuff(self, srcEntityID, buffIndex, buffID, buffScript, casterID, buffTotalTime, endTime, layer):
		"""
		<Exposed Method>
		广播添加buff
		"""
		pass

	def broadcastRemoveBuff(self, srcEntityID, buffIndex):
		"""
		<Exposed Method>
		广播移除buff
		"""
		pass

	def broadcastOnResetBuffEndTime(self, srcEntityID, buffIndex, buffTime):
		"""
		<Exposed Method>
		广播重置buff结束时间
		"""
		if self.otherClients:
			self.otherClients.OnResetBuffEndTime( buffIndex, buffTime )

	def broadcastOnBuffLayerChange(self, srcEntityID, buffIndex, layer):
		"""
		<Exposed Method>
		buff层数变化
		"""	
		if self.allClients:
			self.allClients.OnBuffLayerChange( buffIndex, layer )		

#------------------------------------buff-------------------------------------------------------------------	
	def synClientAddBuff(self, srcEntityID, index, buffID, holdTime, endTime, casterID , casterIsSelf, layer, className):
		"""
		<Exposed Method>
		同步添加buff数据到服务器
		"""
		self.refreshAttrClientBuffs()

		newBuffData = BuffDataType.BuffDataType()
		newBuffData.index = index
		newBuffData.buffID = buffID
		newBuffData.holdTime = holdTime
		newBuffData.endTime = endTime
		newBuffData.casterID = casterID
		newBuffData.casterIsSelf = casterIsSelf
		newBuffData.layer = layer
		newBuffData.className = className
		self.attrBuffs[index ] = newBuffData

		self.attrBuffs.upClientData( self )

	def synClientRemoveBuff(self, srcEntityID, buffIndex):
		"""
		<Exposed Method>
		同步移除buff数据到服务器
		"""
		if buffIndex in self.attrBuffs:
			self.attrBuffs.pop(buffIndex)
			self.attrBuffs.upClientData( self )

	def refreshAttrClientBuffs(self):
		"""
		刷新客户端buff数据
		"""
		removeList = []
		for idx, buffData in self.attrBuffs.items():
			if buffData.holdTime >0 and buffData.endTime <= Functions.getTime():
				removeList.append( idx )

		for idx in removeList :
			self.attrBuffs.pop( idx )

#------------------------------------客户端buff扩展脚本结算--------------------------------------------------
	def cSkillChangeDirection(self, srcEntityID, direction, changeReason):
		"""
		<Exposed Method>
		客户端技能改变朝向
		"""
		sdirection = KBEMath.Unreal2KBEngineDirection( direction )
		self.changeDirection(sdirection, changeReason)

	def cSkillDoHitBack(self, srcEntityID, casterID, moveSpeed, desPosition, actionID, actionBeginTime):
		"""
		<Exposed Method>
		客户端技能开始击退
		"""
		moveSpeed /= 100
		pos = KBEMath.Unreal2KBEnginePosition(desPosition)
		distance = self.position.distTo(pos)
		raycastList = self.navmeshRaycast( self.position, pos )
		if raycastList:	
			pos = raycastList[0]
		if moveSpeed > 0:
			if self.parent:
				pos = self.parent.positionWorldToLocal( pos )
			if not self.controlledBy:
				self.moveBack( pos, moveSpeed )
		else:
			pos = self.position

		uPos = KBEMath.KBEngine2UnrealPosition( pos )
		if not self.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and self.controlledBy:
			self.allClients.CLIENT_ControlledOnBeHitBack(uPos[0], uPos[1], uPos[2], moveSpeed, actionID, actionBeginTime, casterID )
			self.direction = self.direction
		elif self.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) or not self.controlledBy:
			self.allClients.OnBeHitBackNew(uPos[0], uPos[1], uPos[2], 0, moveSpeed, actionID, actionBeginTime, casterID )


	def cSkillOnEndHitBack(self, srcEntityID, casterID, actionID, endActionID):
		"""
		<Exposed Method>
		客户端技能结束击退
		"""
		if self.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			self.initSpeed()
		else:
			if not self.controlledBy:
				self.stopMoving( csdefine.MOVE_TYPE_HIT_BACK  )			

		if not self.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and self.controlledBy:
			self.allClients.CLIENT_ControlledEndHitBack(casterID, actionID, endActionID)
		else:
			self.allClients.OnEndHitBack(casterID, actionID, endActionID)
		self.position = self.position


	def cSkillAddSeverBuff(self, srcEntityID, casterID, buffID):
		"""
		<Exposed Method>
		客户端技能通知添加服务器buff
		"""
		caster = KBEngine.entities.get( casterID, None )
		if caster:
			self.addBuff(caster, buffID)