# -*- coding: utf-8 -*-
import KBEDebug
import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffPLMJCarrierUI( BuffHold ):
	"""
	CST-6262 蟠龙秘境 显示龙鳞载具UI
	"""
	def __init__( self):
		BuffHold.__init__( self )
		self.carrierBuffID = 0 #龙鳞载具BuffID
		self.buffID = 0 # 免伤BuffID

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.carrierBuffID = int(dictDat["Param1"])
		self.buffID = int( dictDat["Param2"] )

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return BuffHold.addBuffCheck( self, caster, receiver )
	
	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_ROLE_PLMJ_CARRIER, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_ROLE_PLMJ_CARRIER, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_ROLE_PLMJ_CARRIER:
			if pDict.get("isMount",0):
				receiver.addBuff( receiver,self.carrierBuffID )
				receiver.addBuff( receiver,self.buffID )
			else:
				receiver.removeBuffByID( self.carrierBuffID )
				receiver.removeBuffByID( self.buffID )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.CLIENT_ShowPLMJCarrierUI()

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		receiver.client.CLIENT_HidePLMJCarrierUI()
		BuffHold.doEnd( self, receiver, buffData, reason )
