# -*- coding: utf-8 -*-

import csdefine
from ConfigObject.Skill.Buff.BuffHold import BuffHold

class BuffQTE( BuffHold ):
	"""
	QTE操作Buff（客户端判断qte是否成功）
	"""
	def __init__( self):
		BuffHold.__init__(self)
		self._qteTypes = ""
		self._triggerSkillId = 0	#QTE成功触发技能ID
		self._failedSkillId = 0		#QTE失败触发技能ID

	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._qteTypes = dictDat["Param1"]	
		if dictDat["Param2"]:
			self._triggerSkillId = int(dictDat["Param2"])
		if dictDat["Param3"]:
			self._failedSkillId = int(dictDat["Param3"])

	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff目前只适用于玩家
			return BuffHold.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""	
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffQTE ):
				receiver.removeBuffByID( buffData.buffID )

		BuffHold.receiveSuccess( self, caster, receiver )


	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_QTE, buffData.index )

	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_QTE, buffData.index )

	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_QTE:
			if "isSucceed" not in pDict:
				receiver.removeBuffByIndex( buffData.index )
				self.doInterrupt( receiver, buffData )
			else:
				_isSucceed = pDict.get( "isSucceed")
				if _isSucceed and self._triggerSkillId:
					receiver.useSkillToEntity( self._triggerSkillId, buffData.casterID )
				elif not _isSucceed and self._failedSkillId:
					receiver.useSkillToEntity( self._failedSkillId, buffData.casterID )
		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.OnStartBuffQTE( self._qteTypes )

	def doEnd( self, receiver, buffData, reason ):
		"""
		效果结束
		"""
		receiver.client.OnEndBuffQTE(self._qteTypes)
		BuffHold.doEnd( self, receiver, buffData, reason )