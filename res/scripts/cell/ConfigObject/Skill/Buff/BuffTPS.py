# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffTPS( BuffHold ):
	"""
	TPS模式
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._conflictPriority = csdefine.BUFF_CONFLICT_PRIORITY_FUC
		self.addConflictType(csdefine.BUFF_CONFLICT_TYPE_MODE)
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() != csdefine.ENTITY_FLAG_ROLE:
			return False
		return BuffHold.addBuffCheck( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.EnterModelTPS()
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )

	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.client.LeaveModelTPS()
		BuffHold.doEnd( self, receiver, buffData,reason )



	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_STATE_CHANGE, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_STATE_CHANGE, buffData.index )


	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_STATE_CHANGE:
			newState = pDict["newState"]
			if newState == csdefine.ENTITY_STATE_DEAD:
				receiver.client.LeaveAimStatus()
			elif csdefine.ENTITY_STATE_FREE:
				receiver.client.EnterAimStatus()

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )