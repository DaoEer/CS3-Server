# -*- coding: utf-8 -*-
import KBEngine
import csdefine
import csstatus
from ConfigObject.Skill.Buff.BuffHost import BuffHost

class BuffCapture( BuffHost ):
	"""
	俘虏buff
	"""

	def __init__( self ):
		BuffHost.__init__( self )

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHost.init( self, dictDat )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHost.doBegin( self, receiver, buffData )
		receiver.actCounterInc( csdefine.ACTION_FORBID_BE_HIT_BACK )
		spaceEntity = receiver.getCurrentSpace()
		if spaceEntity:		# CST-4132 图腾挂上玩家通知
			if receiver.isInSpaceCopy() or receiver.isInSpacePlane():
				spaceEntity.getScript().onConditionChange( spaceEntity, "BUFFCAPTURE", spaceEntity.id, "CAPTURE", "" )

	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.actCounterDec( csdefine.ACTION_FORBID_BE_HIT_BACK )
		BuffHost.doEnd( self, receiver, buffData,reason )	