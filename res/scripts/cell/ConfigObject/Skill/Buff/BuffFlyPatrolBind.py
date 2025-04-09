# -*- coding: utf-8 -*-

import csdefine
import KBEngine
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffFlyPatrolBind( BuffHold ):
	"""
	飞行传送buff：buff开始时开始飞行，飞行结束时结束buff（CST-1813）
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._flyPatrolID = ""
		self._model = ""
		self._FlyModleId = ""
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._flyPatrolID = dictDat["Param1"]
		self._model = dictDat["Param2"]
		self._FlyModleId = dictDat["Param3"]
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.withdrawPetByReason( csdefine.PET_WITHDRAW_FLYTELEPORT )
			receiver.breakFalling()
			receiver.allClients.FlyPatrol( self._flyPatrolID, self._model, self._FlyModleId )
	
	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_STOP_FLY, buffData.index )
	
	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_STOP_FLY, buffData.index )
	
	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_STOP_FLY:
			if pDict.get( "flyPatrolID", "" ) == self._flyPatrolID:
				receiver.removeBuff( buffData.index )
				self.doInterrupt( receiver, buffData )				# 触发中断
		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )