# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffHold import BuffHold


class BuffAddExtraSkillBar( BuffHold ):
	"""
	新增额外技能快捷栏
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.skillIDStr = ""
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		if len( dictDat["Param1"].strip() ):
			self.skillIDStr = dictDat["Param1"].strip()

	
	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffAddExtraSkillBar ):		#移除其他同类buff
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
		if len(self.skillIDStr):
			receiver.client.ShowBuffExtraSkillBar( self.skillIDStr )
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		if self.skillIDStr:
			receiver.client.ShowBuffExtraSkillBar( self.skillIDStr )
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		if len(self.skillIDStr):
			receiver.client.CloseBuffExtraSkillBar()