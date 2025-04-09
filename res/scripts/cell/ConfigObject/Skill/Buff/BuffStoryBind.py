
# -*- coding: utf-8 -*-
import KBEDebug
import csdefine
import KBEngine
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffStoryBind( BuffHold ):
	"""
	镜头buff：buff开始时播镜头，镜头结束时结束buff（CST-1813）
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self._bindStoryID = ""
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._bindStoryID = dictDat["Param1"]
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		return BuffHold.addBuffCheck( self, caster, receiver )

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffStoryBind ):
				receiver.removeBuffByID( buffData.buffID )
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.effectStateInc(csdefine.EFFECT_STATE_SHOW)
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.client.StartBuffPlayStory( self._bindStoryID, 1, buffData.index )

	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.effectStateDec(csdefine.EFFECT_STATE_SHOW)
		if receiver.isEntityFlag( csdefine.ENTITY_FLAG_ROLE ):
			receiver.client.StopBuffStory( buffData.index )
	
	def registerEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.registerEvent( self, receiver, buffData )
		receiver.registerBuffEvent( csdefine.SKILL_EVENT_STORY_END, buffData.index )
	
	def unRegisterEvent( self, receiver, buffData ):
		"""
		virtual method
		"""
		BuffHold.unRegisterEvent( self, receiver, buffData )
		receiver.unRegisterBuffEvent( csdefine.SKILL_EVENT_STORY_END, buffData.index )
	
	def triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict ):
		"""
		virtual member
		触发技能事件
		"""
		if eventType == csdefine.SKILL_EVENT_STORY_END:
			if pDict.get( "storyID", "" ) == self._bindStoryID and pDict.get( "buffIndex", -1 ) == buffData.index:
				receiver.removeBuff( buffData.index )
		BuffHold.triggerBuffEvent( self, receiver, eventType, triggerID, buffData, pDict )