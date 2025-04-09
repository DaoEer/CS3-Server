# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffHSBZModelTPS( BuffHold ):
	"""
	轮回秘境 - 幻兽捕捉射击模式
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.skillID = 0 #对应释放的技能
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.skillID = int( dictDat["Param1"] )
		
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffYCJMDTPS ):		#移除其他同类buff
				receiver.removeBuffByID( buffData.buffID )
		
		BuffHold.receiveSuccess( self, caster, receiver )
	
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
		if receiver.getClient():
			receiver.client.EnterHSBZModelTPS( self.skillID )
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		if receiver.getClient():
			receiver.client.LeaveHSBZModelTPS()
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
				pass
			elif csdefine.ENTITY_STATE_FREE:
				pass

		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )