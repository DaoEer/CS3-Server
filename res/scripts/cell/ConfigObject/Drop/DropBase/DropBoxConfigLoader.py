# -*- coding- : utf-8 -*-

import KBEDebug
import Singleton


class DropBoxConfigLoader( Singleton.Singleton ):
	"""
	掉落宝箱配置
	DropBox.json
	"""
	def __init__( self ):
		"""
		"""
		self._datas = {}
		
	def init( self, config ):
		"""
		"""
		self._datas.clear()
		
		for c in config:
			if c["Name"] in self._datas:
				KBEDebug.ERROR_MSG( "DropBoxConfigLoader:init error, key(%s) has exists" %(c["Name"]))
				continue
				
			self._datas[c["Name"]] = c
		
	def getDropBoxConfig( self, dropboxname ):
		"""
		获取指定宝箱配置
		"""
		config = self._datas.get(dropboxname, None)
		return config
		
		
g_dropBoxConfigLoader = DropBoxConfigLoader()
	
