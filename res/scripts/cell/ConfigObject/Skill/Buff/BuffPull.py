# -*- coding: utf-8 -*-


"""
usage:
	buff

attribute:
	pass

member function:
	pass

callback:
	pass

"""

#engine
import KBEngine
#cell
import Const
from ConfigObject.Skill.Buff.BuffHit import BuffHit
#common
import csdefine
import math
import csarithmetic
import Math
import KBEMath
import KBEDebug
import csstatus



class BuffPull( BuffHit ):
	"""
	拉扯Buff
	"""
	def __init__( self ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHit.__init__( self )
		self._actionID = ""
		
		self._dist = 0.0
		self._speed = 0.0
		self._actionBeginTime = 0.0
		self._endActionID = ""
		self._getUpActionID = []
		self._getUpActionBeginTime = []
		self._getUpActionDelayTime = 0.0

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHit.init( self, dictDat )
		if dictDat["Param1"]:
			actionInfos = dictDat["Param1"].split(":")
			self._actionID = actionInfos[0]
			if len( actionInfos ) >= 2:
				self._actionBeginTime = float(actionInfos[1])

		if dictDat["Param2"]:
			getUpActionInfos = dictDat["Param2"].split(":")
			self._endActionID = getUpActionInfos[0]
			self._getUpActionID.append(getUpActionInfos[0])
			if len( getUpActionInfos ) >=  2:
				self._getUpActionBeginTime.append( getUpActionInfos[1] )
			else:
				self._getUpActionBeginTime.append( "0.0" )
			
		if dictDat["Param3"]:
			pullInfo = dictDat["Param3"].split("|")
			self._speed = float(pullInfo[0])
			self._getUpActionDelayTime = float( pullInfo[1] )
			
		if dictDat["Param4"]:
			self._dist = float(dictDat["Param4"])

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if not receiver.canMoveCheck( True ):
			return False

		return BuffHit.addBuffCheck( self, caster, receiver )

	def receive( self, caster, receiver ):
		"""
		用于给目标施加一个buff，所有的buff的接收都必须通过此接口，
		此接口必须判断接收者是否为realEntity，

		@param   caster: 施法者
		@type    caster: Entity
		@param receiver: 受击者，None表示不存在
		@type  receiver: Entity
		"""
		if not self.addBuffCheck( caster, receiver ):
			return False
		
		#罡气格挡击退
		#if self._actForbid == csdefine.ACTION_FORBID_BE_HIT_BACK and receiver.isInGangQiArmor():	# CST-2229:若玩法设定是“战斗玩法”（ActForbid＝ForbidBeHitback），且目标单位处于“罡气气盈/气短状态”，则拉扯Buff被替换成格挡Buff
		#	receiver.addBuff( caster, Const.BUFF_GANG_QI_BLOCK )
		#	return False
		
		#替换效果
		if self._replaceCondition.valid( caster, receiver, True ) == csstatus.SKILL_GO_ON:
			for effect in self._replaceEffectList:
				if effect.canEffect( self, caster, receiver ):
					effect.onReceive( self, caster, receiver )
			return False
		
		self.receiveSuccess( caster, receiver )
		return True

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		from ConfigObject.Skill.Buff.BuffHitBack import BuffHitBack
		from ConfigObject.Skill.Buff.BuffRise import BuffRise
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffPull ) or isinstance( buff, BuffHitBack ) or isinstance( buff, BuffRise ):		#移除其他同类buff
				receiver.removeBuffByID( buffData.buffID )

		BuffHit.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		receiver.effectStateInc( csdefine.EFFECT_STATE_HIT_BACK )
		receiver.curHitBackCasterID = buffData.casterID
		self.doPull(receiver,buffData)
		BuffHit.doBegin( self, receiver, buffData )

	def doPull( self, receiver, buffData ):
		"""
		拉扯
		"""
		caster = KBEngine.entities.get( buffData.casterID, None )
		if caster:
			casterID = caster.id
			direction = Math.Vector3(0,0,csarithmetic.getYawByVector3(caster.position-receiver.position))
			receiver.changeDirection(direction, csdefine.REASON_CHANGE_DIR_FORCE)
			yaw = csarithmetic.getYawByVector3( caster.position - receiver.position )
			dist = caster.position.flatDistTo( receiver.position )
			dist = dist - self._dist
		else:
			casterID = 0
			yaw = receiver.getYaw() + math.pi
			dist = 0.0
		if dist > 0.0:
			dest = Math.Vector3( dist * math.sin( yaw ), 0, dist * math.cos( yaw ) )
		else:
			dest = Math.Vector3(0,0,0)
		
		dstPos = receiver.position+dest
		raycastList = receiver.navmeshRaycast( receiver.position, dstPos )
		if raycastList:	
			dstPos = raycastList[0]
		if self._speed > 0:
			if receiver.parent:
				dstPos = receiver.parent.positionWorldToLocal( dstPos )
			
			moveTime = dist / self._speed
			if not receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
				receiver.moveBack( dstPos, self._speed )
		else:
			moveTime = 0
		
		dstPos = Math.Vector3( KBEMath.KBEngine2UnrealPosition( dstPos ) )
		receiver.allClients.OnPull(dstPos.x, dstPos.y, dstPos.z, self._speed, self._actionID, self._actionBeginTime, casterID )

		if self._getUpActionDelayTime > moveTime:
			delayUpTime = self._getUpActionDelayTime
		else:
			delayUpTime = moveTime
		#起身
		if self._endActionID:
			receiver.addHitFlyTimer( delayUpTime, casterID , self._getUpActionID, "", "", self._getUpActionBeginTime )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.effectStateDec( csdefine.EFFECT_STATE_HIT_BACK )
		if not receiver.hasEffectState( csdefine.EFFECT_STATE_HIT_BACK ):
			receiver.curHitBackCasterID = 0
			self.endPull( receiver,buffData )
		BuffHit.doEnd( self, receiver, buffData,reason )

	def endPull( self, receiver, buffData ):
		"""
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.initSpeed()
		else:
			receiver.stopMovingForType( csdefine.SYSTEM_MOVE )
		receiver.delHitFlyTimer()
		receiver.allClients.EndPull(buffData.casterID,self._endActionID)
	