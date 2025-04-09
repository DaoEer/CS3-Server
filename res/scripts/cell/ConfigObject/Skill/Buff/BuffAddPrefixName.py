# -*- coding: utf-8 -*-

from ConfigObject.Skill.Buff.BuffHold import BuffHold
import csdefine
import KBEDebug

class BuffAddPrefixName( BuffHold ):
	"""
	增加前缀名字
	"""
	def __init__( self ):
		BuffHold.__init__( self )
		self.prefixName = ""
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self.prefixName = dictDat["Param1"]

	def receiveSuccess( self, caster, receiver ):
		"""
		通过了免疫、替换等等等的拦截，真正要加buff了
		"""
		for buffData in list(receiver.getAttrBuffs().values()):
			buff = caster.getBuff( buffData.buffID )
			if isinstance( buff, BuffAddPrefixName ):
				receiver.removeBuffByID( buffData.buffID, csdefine.BUFF_END_RESON_BY_REPLACE )
		BuffHold.receiveSuccess( self, caster, receiver )
	
	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		buffData.setTempData("recordPrefixName", receiver.getPrefixName())
		receiver.setPrefixName(self.prefixName)

	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		buffData.setTempData("recordPrefixName",receiver.getPrefixName())
		receiver.setPrefixName(self.prefixName)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.setPrefixName( buffData.getTempData("recordPrefixName") )

