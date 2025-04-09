# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffControlXianzhou( BuffHold ):
	"""
	仙舟渡劫 -- 控制仙舟
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.xianZhouScriptID = ""

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.xianZhouScriptID = dictDat["Param1"]

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffControlXianzhou ):	#移除其他同类buff
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
		entitylist = self.getEntityRecord( self.xianZhouScriptID )
		if len( entitylist ) == 0: return
		entity = KBEngine.entities.get( entitylist[0] )
		receiver.client.EnterControlXianZhou()
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )

	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.client.LeaveControlXianZhou()
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