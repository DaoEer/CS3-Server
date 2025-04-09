# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import csstatus
import Math
import KBEMath
import Functions
import KBEDebug
from ConfigObject.Skill.Buff.BuffGuest import BuffGuest

class BuffBeCapture( BuffGuest ):
	"""
	被俘虏buff
	"""

	def __init__( self ):
		BuffGuest.__init__( self )
		self._slot = ""
		self._position = Math.Vector3(0,0,0)
		self._direction = Math.Vector3(0,0,0)

	def addBuffCheck( self, caster, receiver ):
		"""
		检测buff是可以替换
		如能替换就在此处移除buff效果
		"""
		if caster.id == receiver.id:
			return False
		from ConfigObject.Skill.Buff.BuffCapture import BuffCapture
		tempBuffDataList = list(receiver.getAttrBuffs().values())
		for buffData in tempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffBeCapture ) or isinstance( buff, BuffCapture ):
				return False
		casterTempBuffDataList = list(caster.getAttrBuffs().values())
		for buffData in casterTempBuffDataList:
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffBeCapture ):
				return False		
		return BuffGuest.addBuffCheck( self, caster, receiver )

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffGuest.init( self, dictDat )
		self._slot = dictDat["Param2"]
		if dictDat["Param3"]:
			posStrList = dictDat["Param3"].split("|")
			self._position =  Math.Vector3( float( posStrList[0] ), float( posStrList[1] ), float( posStrList[2] ) )

		if dictDat["Param4"]:
			dirStrList = dictDat["Param4"].split("|")
			self._direction =  Math.Vector3( float( dirStrList[0] ), float( dirStrList[1] ), float( dirStrList[2] ) )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffGuest.doBegin( self, receiver, buffData )
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			receiver.monsterAIStop()
			receiver.addFlag(csdefine.FLAG_CLOSE_COLLISION)
			receiver.stopMovingForType(csdefine.SYSTEM_MOVE)
			caster = KBEngine.entities.get( buffData.casterID, None )
			timer = receiver.addTimerRepeat( 0.1, "synPositionToTarget", (caster,) )
			buffData.setTempData("BeCaptureTimer",timer)

		receiver.allClients.BeCapture( receiver.id, buffData.casterID, self._slot, self._position, self._direction )
		receiver.effectStateInc( csdefine.EFFECT_STATE_HIT_BACK )
		receiver.actCounterInc( csdefine.ACTION_FORBID_BE_HIT_BACK )
			
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.allClients.BeReleased(receiver.id,)
		if receiver.hasEffectState(csdefine.EFFECT_STATE_HIT_BACK):
			receiver.effectStateDec( csdefine.EFFECT_STATE_HIT_BACK )
		if receiver.actionForbidSign( csdefine.ACTION_FORBID_BE_HIT_BACK):
			receiver.actCounterDec( csdefine.ACTION_FORBID_BE_HIT_BACK )
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_MONSTER:
			receiver.removeFlag(csdefine.FLAG_CLOSE_COLLISION)
			receiver.monsterAIReStart()
			receiver.popTimer( buffData.getTempData("BeCaptureTimer") )
			
		BuffGuest.doEnd( self, receiver, buffData,reason )

	def onClientActorCreate( self, receiver, buffData, srcEntityID ):
		"""
		virtual method
		receiver在某客户端被创建出来
		"""
		if srcEntityID == receiver.id:
			clientEntity = receiver.client
		else:
			playerEntity = KBEngine.entities.get( srcEntityID )
			if not playerEntity:
				return
			clientEntity = playerEntity.clientEntity( receiver.id )

		clientEntity.BeCapture( receiver.id, buffData.casterID, self._slot, self._position, self._direction )
			