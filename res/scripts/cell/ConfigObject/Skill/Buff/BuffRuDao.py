# -*- coding: utf-8 -*-

import csdefine
import KBEDebug
#engine
import KBEngine
#cell
from ConfigObject.Skill.Buff.BuffStackable import BuffStackable


class BuffRuDao( BuffStackable ):
	"""
	入道BUFF（CST-4246 九字真言）
	"""
	def __init__( self ):
		BuffStackable.__init__( self )
		
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffStackable.init( self, dictDat )
	
	def addBuffCheck( self, caster, receiver ):
		"""
		添加检测
		"""
		if receiver.getEntityFlag() == csdefine.ENTITY_FLAG_ROLE: #此buff只给玩家加
			return BuffStackable.addBuffCheck( self, caster, receiver )

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffStackable.doBegin( self, receiver, buffData )
		receiver.client.OnNotifyJZZYRuDaoBuff(True)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		receiver.client.OnNotifyJZZYRuDaoBuff(False)
		BuffStackable.doEnd( self, receiver, buffData,reason )
