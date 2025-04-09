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
#python
import math
import random
import Math
#engine
import KBEngine
import KBEMath
#cell
import Const
from ConfigObject.Skill.Buff.BuffHit import BuffHit
#common
import csdefine
import csarithmetic
import KBEDebug
import csstatus

class BuffHitBack( BuffHit ):
	"""
	受击击退buff（受击动作、光效、音效,击退位移）
	"""
	def __init__( self ):
		BuffHit.__init__( self )
		self._actionID = ""
		self._moveTime = 0.0
		self._distMin = 0.0				# 击退最小距离 单位（m）
		self._distMax = 0.0
		self._actionBeginTime = 0.0
		self._endActionID = ""
		self._getUpActionID = []
		self._getUpActionBeginTime = []
		self._getUpActionDelayTime = 0.0
		self._directionType = csdefine.BUFF_HIT_TYPE_CASTER_DIRECTION
		self._hitBackType = csdefine.BUFF_HIT_TYPE_CASTER_FORWARD
	
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
				self._actionBeginTime = float( actionInfos[1] )
		
		if dictDat["Param2"]:
			getUpActionInfos = dictDat["Param2"].split(":")
			self._endActionID = getUpActionInfos[0]
			self._getUpActionID.append(getUpActionInfos[0])
			if len( getUpActionInfos ) >= 2:
				self._getUpActionBeginTime.append( getUpActionInfos[1] )
			else:
				self._getUpActionBeginTime.append( "0.0" )
		
		if dictDat["Param3"]:
			infos = dictDat["Param3"].split("|")
			self._moveTime = float(infos[0])
			if len( infos )>= 2:
				self._getUpActionDelayTime = float( infos[1] )
			
		if dictDat["Param4"]:
			dist = dictDat["Param4"].split("|")
			if len( dist ) >= 2:
				self._distMin = float( dist[0] )
				self._distMax = float( dist[1] )
			else:
				if dictDat["Param4"].startswith("|"):
					self._distMin = 0.0
					self._distMax = float( dist[0] )
				else:
					self._distMin = float( dist[0] )
					self._distMax = float( dist[0] )
			
		if dictDat["Param5"]:
			hitType = dictDat["Param5"].split("|")
			self._directionType = int( hitType[0] )
			if len( hitType ) >= 2:
				self._hitBackType = int( hitType[1] )
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if not receiver.canMoveCheck( True ):
			return False
		#casterID = caster.id
		#if receiver.curHitBackCasterID != 0 and receiver.curHitBackCasterID != casterID:	# 不同玩家同时攻击一个怪物时，只表现一个玩家的击退，不叠加表现。
		#	return False
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
		#if self._actForbid == csdefine.ACTION_FORBID_BE_HIT_BACK and receiver.isInGangQiArmor():	# CST-2229:若玩法设定是“战斗玩法”（ActForbid＝ForbidBeHitback），且目标单位处于“罡气气盈/气短状态”，则击退Buff被替换成格挡Buff
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
		from ConfigObject.Skill.Buff.BuffPull import BuffPull
		from ConfigObject.Skill.Buff.BuffRise import BuffRise
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffHitBack ) or isinstance( buff, BuffPull ) or isinstance( buff, BuffRise ):		#移除其他同类buff
				receiver.removeBuffByID( buffData.buffID )

		BuffHit.receiveSuccess( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		receiver.effectStateInc( csdefine.EFFECT_STATE_HIT_BACK )
		receiver.curHitBackCasterID = buffData.casterID
		self.doHitBack( receiver, buffData )
		BuffHit.doBegin( self, receiver, buffData )

	def doHitBack( self, receiver, buffData ):
		"""
		击退
		"""
		caster = KBEngine.entities.get( buffData.casterID, None )
		#目标朝向扩展
		if caster and not receiver.hasFlag(csdefine.FLAG_CANT_ROTATE):
			recvDir = Math.Vector3(receiver.direction)
			if self._directionType == csdefine.BUFF_HIT_TYPE_CASTER_DIRECTION:
				recvDir.z = caster.direction.z
				#receiver.direction.z = caster.direction.z
			elif self._directionType == csdefine.BUFF_HIT_TYPE_CASTER_RDIRECTION:
				recvDir.z = caster.direction.z + math.pi
			elif self._directionType == csdefine.BUFF_HIT_TYPE_CATORE_DIRECTION:
				if receiver.position.z == caster.position.z and receiver.position.x == caster.position.x:
					recvDir.z = caster.direction.z
				else:
					recvDir.z = csarithmetic.getYawByVector3(receiver.position-caster.position)
			elif self._directionType == csdefine.BUFF_HIT_TYPE_CATORE_RDIRECTION:
				if receiver.position.z == caster.position.z and receiver.position.x == caster.position.x:
					recvDir.z = receiver.direction.z
				else:
					recvDir.z = csarithmetic.getYawByVector3(caster.position-receiver.position)
			elif self._directionType == csdefine.BUFF_HIT_TYPE_RECEIVER_DIRECTION:
				recvDir.z = receiver.direction.z
			elif self._directionType == csdefine.BUFF_HIT_TYPE_RECEIVER_RDIRECTION:
				recvDir.z += math.pi
			receiver.changeDirection(recvDir, csdefine.REASON_CHANGE_DIR_FORCE)
		
		if caster:
			casterID = caster.id
			yaw = caster.getYaw()
			# 击退朝向扩展
			if self._hitBackType == csdefine.BUFF_HIT_TYPE_CASTER_FORWARD:
				yaw = caster.getYaw()
			elif self._hitBackType == csdefine.BUFF_HIT_TYPE_CASTER_REAR:
				yaw = caster.getYaw() + math.pi
			elif self._hitBackType == csdefine.BUFF_HIT_TYPE_CATORE_FORWARD:
				if receiver.position.z == caster.position.z and receiver.position.x == caster.position.x:
					yaw = caster.getYaw()
				else:
					yaw = csarithmetic.getYawByVector3( receiver.position - caster.position )
			elif self._hitBackType == csdefine.BUFF_HIT_TYPE_CATORE_REAR:
				if receiver.position.z == caster.position.z and receiver.position.x == caster.position.x:
					yaw = receiver.getYaw()
				else:
					yaw = csarithmetic.getYawByVector3( caster.position - receiver.position )
			elif self._hitBackType == csdefine.BUFF_HIT_TYPE_RECEIVER_FORWARD:
				yaw = receiver.getYaw()
			elif self._hitBackType == csdefine.BUFF_HIT_TYPE_RECEIVER_REAR:
				yaw = receiver.getYaw() + math.pi
				
		else:
			casterID = 0
			yaw = receiver.getYaw() + math.pi
		
		pos = receiver.position
		if self._moveTime <= 0:
			dest = Math.Vector3(0,0,0)
			moveSpeed = 0.0
		else:
			backDistance = random.random() * ( self._distMax - self._distMin ) + self._distMin
			moveSpeed = backDistance/self._moveTime
			dest = Math.Vector3( backDistance * math.sin( yaw ), 0, backDistance * math.cos( yaw ) )
			pos = Math.Vector3(receiver.position + dest)
			raycastList = receiver.navmeshRaycast( receiver.position, pos )
			if raycastList:	
				pos = raycastList[0]
			
		if moveSpeed > 0:
			if receiver.parent:
				pos = receiver.parent.positionWorldToLocal( pos )
			if not receiver.controlledBy:
				receiver.moveBack( pos, moveSpeed )
		else:
			if receiver.parent:
				pos = receiver.parent.positionWorldToLocal(pos)
			else:
				pos = receiver.position
	
		uPos = KBEMath.KBEngine2UnrealPosition( pos )
		if not receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and receiver.controlledBy:
			receiver.allClients.CLIENT_ControlledOnBeHitBack(uPos[0], uPos[1], uPos[2], moveSpeed, self._actionID, self._actionBeginTime, casterID )
			receiver.direction = receiver.direction
		elif receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) or not receiver.controlledBy:
			receiver.allClients.OnBeHitBackNew(uPos[0], uPos[1], uPos[2], self._id, moveSpeed, self._actionID, self._actionBeginTime, casterID )
		
		#被击飞后起身
		if self._endActionID:
			receiver.addHitFlyTimer( self._getUpActionDelayTime, casterID , self._getUpActionID, "", "", self._getUpActionBeginTime )
			
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.effectStateDec( csdefine.EFFECT_STATE_HIT_BACK )
		if not receiver.hasEffectState( csdefine.EFFECT_STATE_HIT_BACK ):
			receiver.curHitBackCasterID = 0
			self.endHitBack( receiver, buffData )
		BuffHit.doEnd( self, receiver, buffData,reason )

	def endHitBack( self, receiver, buffData ):
		"""
		"""
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.initSpeed()
		else:
			if not receiver.controlledBy:
				receiver.stopMoving( csdefine.MOVE_TYPE_HIT_BACK  )			
		receiver.delHitFlyTimer()

		if not receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ) and receiver.controlledBy:
			receiver.allClients.CLIENT_ControlledEndHitBack(buffData.casterID,self._actionID, self._endActionID)
		else:
			receiver.allClients.OnEndHitBack(buffData.casterID,self._actionID, self._endActionID)

		if not receiver.controlledBy:#由客户端控制的角色不需要设置位置了，位置会每帧往服务器发，所以客户端主控的角色不需要设置位置
			if buffData.getTempData( "HitBackPostion" ) != None:
				receiver.position = buffData.getTempData( "HitBackPostion" )
			else:
				receiver.position = receiver.position
	