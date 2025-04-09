# -*- coding: utf-8 -*-

from ConfigObject.Skill.Buff.BuffHold import BuffHold
import csdefine

class BuffItemGrey( BuffHold ):
	"""
	置灰物品
	"""
	def __init__( self ):
		BuffHold.__init__( self )
	
	def init( self, dictDat ):
		"""
		virtual method;
		读取buff配置
		@param dictDat: 配置数据
		@type  dictDat: python dict
		"""
		BuffHold.init( self, dictDat )
		self._itemID = int(dictDat["Param1"])

	def doBegin( self, receiver, buffData ):
		"""
		效果开始
		"""
		BuffHold.doBegin( self, receiver, buffData )
		receiver.client.CLIENT_GreyItem(self._itemID)
		itemList = receiver.getItemInstsByID( self._itemID )
		for item in itemList:
			item.setLock( True )
	
	def doReload( self, receiver, buffData ):
		"""
		上线重新加载buff
		"""
		BuffHold.doReload( self, receiver, buffData )
		receiver.client.CLIENT_GreyItem(self._itemID)
	
	def doEnd( self, receiver, buffData,reason ):
		"""
		效果结束
		"""
		BuffHold.doEnd( self, receiver, buffData,reason )
		receiver.client.CLIENT_ClearGreyItem(self._itemID)
		itemList = receiver.getItemInstsByID( self._itemID )
		for item in itemList:
			item.setLock( False )

